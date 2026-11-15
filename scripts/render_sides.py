# -*- coding: utf-8 -*-
"""Render the "which one?" pictures for parts that come in normal and mirrored versions.

Run in the FreeCAD GUI:
    exec(open("/path/to/spotmicro-arduino-q/scripts/render_sides.py").read())
Each part is drawn as it lies on the table after printing (print position), seen from the front and above, in a
manual-style look: light faces, black sharp edges, and the feature that tells the versions apart in orange. Writes
site/public/renders/sides/<key>-{normal,mirrored}.png (800x600) and <key>-{normal,mirrored}-zoom.png (400x400, the
orange area). Uses the unlabelled meshes from git (UNLABELLED_REF) so the pictures match parts printed before the
side labels were added.
"""
import math
import os
import subprocess
import tempfile

import numpy as np
import FreeCAD
import FreeCADGui as Gui
import Mesh
import Part

_SCRIPTS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(
    os.environ.get("SPOT_ROOT", "/Users/jberi/code/robotics/spot-unoq"), "scripts")
REPO = os.path.dirname(_SCRIPTS)
OUT = os.path.join(REPO, "site", "public", "renders", "sides")
UNLABELLED_REF = "9b21b99"  # a commit with the STLs as printed before the side labels
# key: (STL path, orange box in normalised coordinates of the normal part: x0, x1, y0, y1; y = 0 is the edge
# towards the viewer). The mirrored part gets the mirrored box.
SPEC = {
    "wrist": ("legs/Wrist", (0, 0.17, 0, 1)),
    "wrist-counterpart": ("legs/Wrist_Counterpart", (0, 0.45, 0, 0.4)),
    "bearing-plate": ("legs/Limb_Ball_Bearing_Mount_long_v4", (0, 0.5, 0.62, 1)),
    "horn-plate": ("legs/Limb_Servohorn_Mount_long_v4", (0.5, 1, 0.62, 1)),
    "top-shell": ("legs/Limb_Top_Shell_with_BB_hole", (0, 0.3, 0, 1)),
    "bottom-shell": ("legs/Limb_Bottom_Shell", (0, 0.3, 0, 1)),
    "shoulder-mount": ("shoulders/Shoulder_Joint_Servomount_extended_BB", (0, 0.25, 0, 1)),
}
DIRECTION = (0.0, 0.75, -0.66)  # camera: from the front (-Y) and above
LIGHT, ORANGE, INK = (0.95, 0.95, 0.95), (0.96, 0.55, 0.15), (0.08, 0.08, 0.08)


def unlabelled(path, tmp):
    dest = os.path.join(tmp, os.path.basename(path))
    with open(dest, "wb") as f:
        f.write(subprocess.check_output(["git", "-C", REPO, "show", f"{UNLABELLED_REF}:stl/{path}"]))
    return Mesh.Mesh(dest)


def sharp_edges(m, angle=28):
    pts, faces = m.Topology
    P = np.array([(p.x, p.y, p.z) for p in pts])
    F = np.array(faces)
    N = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
    edges = {}
    for fi, (a, b, c) in enumerate(F):
        for e in ((a, b), (b, c), (c, a)):
            edges.setdefault((min(e), max(e)), []).append(fi)
    cos = math.cos(math.radians(angle))
    return Part.makeCompound([Part.LineSegment(FreeCAD.Vector(*P[a]), FreeCAD.Vector(*P[b])).toShape()
                              for (a, b), fs in edges.items() if len(fs) != 2 or np.dot(N[fs[0]], N[fs[1]]) < cos])


def subdivide(m, maxlen=1.2):
    """Split triangles until no edge is longer than maxlen, so the orange area has a clean border."""
    pts, faces = m.Topology
    P = [np.array((p.x, p.y, p.z)) for p in pts]
    F = [tuple(f) for f in faces]
    for _ in range(8):
        long = {(min(e), max(e)) for a, b, c in F for e in ((a, b), (b, c), (c, a))
                if np.linalg.norm(P[e[0]] - P[e[1]]) > maxlen}
        if not long:
            break
        mid = {}

        def midpoint(a, b):
            k = (min(a, b), max(a, b))
            if k not in mid:
                P.append((P[a] + P[b]) / 2)
                mid[k] = len(P) - 1
            return mid[k]

        out = []
        for a, b, c in F:
            es = [(a, b), (b, c), (c, a)]
            ls = [(min(e), max(e)) in long for e in es]
            n = sum(ls)
            if n == 0:
                out.append((a, b, c))
            elif n == 3:
                ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
                out += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
            elif n == 1:
                i = ls.index(True)
                x, y = es[i]
                z = (a, b, c)[(i + 2) % 3]
                mm = midpoint(x, y)
                out += [(x, mm, z), (mm, y, z)]
            else:
                i = ls.index(False)
                x, y = es[i]
                z = (a, b, c)[(i + 2) % 3]
                m1, m2 = midpoint(y, z), midpoint(z, x)
                out += [(x, y, m1), (x, m1, m2), (m2, m1, z)]
        F = out
    r = Mesh.Mesh()
    r.addFacets([[tuple(P[i]) for i in f] for f in F])
    return r


def split(m, box, mirrored):
    b = m.BoundBox
    x0, x1, y0, y1 = box
    if mirrored:
        x0, x1 = 1 - x1, 1 - x0
    hi, lo = [], []
    for f in m.Facets:
        cx = sum(p[0] for p in f.Points) / 3
        cy = sum(p[1] for p in f.Points) / 3
        fx, fy = (cx - b.XMin) / b.XLength, (cy - b.YMin) / b.YLength
        (hi if x0 <= fx <= x1 and y0 <= fy <= y1 else lo).append(f.Points)
    return Mesh.Mesh(lo), Mesh.Mesh(hi)


def render(doc, view, lo, hi, edges, path, zoom):
    for o in list(doc.Objects):
        doc.removeObject(o.Name)
    a = doc.addObject("Mesh::Feature", "lo")
    a.Mesh = lo
    a.ViewObject.ShapeColor = LIGHT
    b = doc.addObject("Mesh::Feature", "hi")
    b.Mesh = hi
    b.ViewObject.ShapeColor = ORANGE
    for o in (a, b):
        o.ViewObject.Lighting = "Two side"
    e = doc.addObject("Part::Feature", "edges")
    e.Shape = edges
    e.ViewObject.LineColor = INK
    e.ViewObject.LineWidth = 3
    doc.recompute()
    view.setCameraType("Orthographic")
    view.setViewDirection(DIRECTION)
    if zoom:  # frame the orange area only
        a.ViewObject.Visibility = e.ViewObject.Visibility = False
        view.fitAll()
        a.ViewObject.Visibility = e.ViewObject.Visibility = True
        cam = view.getCameraNode()
        cam.height.setValue(cam.height.getValue() * 1.15)
    else:
        view.fitAll()
    w, h, size = (1000, 1000, "400:400") if zoom else (1600, 1200, "800:600")
    raw = path + ".raw.png"
    view.saveImage(raw, w, h, "White")
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-vf", f"scale={size}:flags=lanczos",
                           "-pix_fmt", "rgb24", path])
    os.remove(raw)


def main():
    os.makedirs(OUT, exist_ok=True)
    doc = FreeCAD.newDocument("Sides")
    view = Gui.getDocument(doc.Name).ActiveView
    with tempfile.TemporaryDirectory() as tmp:
        for key, (stl, box) in SPEC.items():
            for version, suffix in (("normal", ""), ("mirrored", "_mirrored")):
                m = unlabelled(stl + suffix + ".stl", tmp)
                lo, hi = split(subdivide(m), box, version == "mirrored")
                edges = sharp_edges(m)
                for zoom in (False, True):
                    render(doc, view, lo, hi, edges, os.path.join(OUT, f"{key}-{version}{'-zoom' if zoom else ''}.png"), zoom)
                FreeCAD.Console.PrintMessage(f"rendered {key} {version}\n")
    FreeCAD.closeDocument(doc.Name)


main()
