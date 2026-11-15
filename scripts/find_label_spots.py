# -*- coding: utf-8 -*-
"""Find where to engrave the side labels on parts that come in normal and mirrored versions.

Run in the FreeCAD GUI (it opens the assembly through guide_render_lib):
    exec(open("/path/to/spotmicro-arduino-q/scripts/find_label_spots.py").read())

For each part it:
1. registers the printable STL (print position) onto the front-left leg's copy in cad/SpotUnoQ.FCStd (PCA, then ICP);
2. lists spots where the label box fits on a face that is horizontal as printed: an upward face, or the bed face
   (anything else would put the letters on a wall and add overhangs);
3. scores each spot by shooting 24 rays over the hemisphere above it in the assembled robot: a spot is hidden when
   every ray hits a part within 250 mm.
It prints the most central fully hidden spot per face; scripts/export_stls.py LABELS holds the chosen ones (upward
faces preferred, since bed-face letters need short bridges).
"""
import math
import os
import sys
from collections import defaultdict

import numpy as np
import FreeCAD
import Mesh

_SCRIPTS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(
    os.environ.get("SPOT_ROOT", "/Users/jberi/code/robotics/spot-unoq"), "scripts")
sys.path.insert(0, _SCRIPTS)
import guide_render_lib as G  # noqa: E402

REPO = os.path.dirname(_SCRIPTS)
STL = os.path.join(REPO, "stl")
# front-left leg object -> (normal STL, label box w x h in mm)
PARTS = {
    "LL_Body054": ("legs/Wrist", (7, 9)),
    "LL_Body011": ("legs/Wrist_Counterpart", (9, 9)),
    "LL_Body051": ("legs/Limb_Ball_Bearing_Mount_long_v4", (9, 9)),
    "LL_Body041": ("legs/Limb_Servohorn_Mount_long_v4", (9, 9)),
    "robjk_shell_FL": ("legs/Limb_Top_Shell_with_BB_hole", (9, 9)),
    "LL_Body060": ("legs/Limb_Bottom_Shell", (9, 9)),
    "robjk_servomount_FL": ("shoulders/Shoulder_Joint_Servomount_extended_BB", (18, 8)),
}


def global_mesh(S, name):
    for o, path in S.items:
        if o.Name != name:
            continue
        par = FreeCAD.Placement()
        for n in path:
            par = par.multiply(S.doc.getObject(n).Placement)
        if o.TypeId == "Mesh::Feature":
            m = o.Mesh.copy()
            m.Placement = par.multiply(o.Placement)
            return m
        s = o.Shape.copy()
        s.Placement = par.multiply(s.Placement)
        return Mesh.Mesh(s.tessellate(0.2))


def surface_points(m, n, seed):
    P = np.array([f.Points for f in m.Facets])
    A = np.array([f.Area for f in m.Facets])
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(A), n, p=A / A.sum())
    r1, r2 = np.sqrt(rng.random(n)), rng.random(n)
    T = P[idx]
    return (1 - r1)[:, None] * T[:, 0] + (r1 * (1 - r2))[:, None] * T[:, 1] + (r1 * r2)[:, None] * T[:, 2]


def register(stl_mesh, asm_mesh):
    """Rotation R and translation t taking STL coordinates to the assembly."""
    import itertools
    A, B = surface_points(asm_mesh, 1500, 1), surface_points(stl_mesh, 1500, 2)

    def nearest(a, b):
        return ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)

    ca, cb = A.mean(0), B.mean(0)
    ea = np.linalg.eigh(np.cov((A - ca).T))[1]
    eb = np.linalg.eigh(np.cov((B - cb).T))[1]
    best = None
    for s in itertools.product([1, -1], repeat=3):
        R = ea @ np.diag(s) @ eb.T
        e = np.sqrt(nearest((B[::3] - cb) @ R.T + ca, A).min(1)).mean()
        if best is None or e < best[0]:
            best = (e, R)
    R = best[1]
    t = ca - R @ cb
    for _ in range(15):  # ICP
        Bt = B @ R.T + t
        C = A[nearest(Bt, A).argmin(1)]
        mb, mc = Bt.mean(0), C.mean(0)
        U, _, Vt = np.linalg.svd((Bt - mb).T @ (C - mc))
        dR = Vt.T @ np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]) @ U.T
        R, t = dR @ R, dR @ (t - mb) + mc
    return R, t


def spots(m, box, step=3.0, res=0.5):
    """(x, y, z, +1 up / -1 bed, rotation) where a box-sized label fits on a horizontal face."""
    planes = defaultdict(list)
    for f in m.Facets:
        if abs(f.Normal.z) > 0.999:
            planes[(1 if f.Normal.z > 0 else -1, round(sum(p[2] for p in f.Points) / 3, 1))].append(f.Points)
    b = m.BoundBox
    xs, ys = np.arange(b.XMin, b.XMax, res), np.arange(b.YMin, b.YMax, res)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    out = []
    for (sg, z), tris in planes.items():
        if sg < 0 and z > 0.05:
            continue  # downward faces off the bed would need support
        mask = np.zeros(X.shape, bool)
        for (x1, y1, _), (x2, y2, _), (x3, y3, _) in tris:
            d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if abs(d) < 1e-9:
                continue
            i0, i1 = np.searchsorted(xs, [min(x1, x2, x3), max(x1, x2, x3)])
            j0, j1 = np.searchsorted(ys, [min(y1, y2, y3), max(y1, y2, y3)])
            sx, sy = X[i0:i1, j0:j1], Y[i0:i1, j0:j1]
            a = ((y2 - y3) * (sx - x3) + (x3 - x2) * (sy - y3)) / d
            c = ((y3 - y1) * (sx - x3) + (x1 - x3) * (sy - y3)) / d
            mask[i0:i1, j0:j1] |= (a >= -1e-6) & (c >= -1e-6) & (a + c <= 1 + 1e-6)
        I = np.pad(mask.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        for rot, (w, h) in ((0, box), (90, box[::-1])):
            hw, hh = int(np.ceil(w / 2 / res)), int(np.ceil(h / 2 / res))
            st = max(1, int(step / res))
            for i in range(hw, mask.shape[0] - hw, st):
                for j in range(hh, mask.shape[1] - hh, st):
                    if I[i + hw, j + hh] - I[i - hw, j + hh] - I[i + hw, j - hh] + I[i - hw, j - hh] >= 4 * hw * hh:
                        out.append((xs[i], ys[j], z, sg, rot))
            if box[0] == box[1]:
                break
    return out


def occluders(S, around, margin=60):
    bb = around.BoundBox
    bb.enlarge(margin)
    out = Mesh.Mesh()
    for o, path in S.items:
        if not o.Visibility:
            continue
        try:
            par = FreeCAD.Placement()
            for n in path:
                par = par.multiply(S.doc.getObject(n).Placement)
            if o.TypeId == "Mesh::Feature":
                m = o.Mesh.copy()
                m.Placement = par.multiply(o.Placement)
            else:
                s = o.Shape.copy()
                s.Placement = par.multiply(s.Placement)
                if not s.BoundBox.intersect(bb):
                    continue
                m = Mesh.Mesh(s.tessellate(0.5))
            if m.BoundBox.intersect(bb):
                out.addMesh(m)
        except Exception:  # links without geometry
            pass
    return out


def hemisphere(n=24):
    ga = math.pi * (3 - math.sqrt(5))
    return [(math.sqrt(1 - z * z) * math.cos(i * ga), math.sqrt(1 - z * z) * math.sin(i * ga), z)
            for i, z in ((i, 1 - (i + 0.5) / n) for i in range(n))]


def hidden_fraction(occ, p, nvec, rays):
    a = np.array([1, 0, 0]) if abs(nvec[0]) < 0.9 else np.array([0, 1, 0])
    u = np.cross(nvec, a)
    u /= np.linalg.norm(u)
    v = np.cross(nvec, u)
    o = p + 0.3 * nvec
    hits = 0
    for dx, dy, dz in rays:
        r = occ.nearestFacetOnRay(tuple(o), tuple(dx * u + dy * v + dz * nvec))
        if r and math.dist(list(r.values())[0], o) < 250:
            hits += 1
    return hits / len(rays)


def main(max_spots=50):
    S = G.Scene(os.path.join(REPO, "cad", "SpotUnoQ.FCStd"))
    rays = hemisphere()
    for name, (stl, box) in PARTS.items():
        m = Mesh.Mesh(os.path.join(STL, stl + ".stl"))
        asm = global_mesh(S, name)
        R, t = register(m, asm)
        occ = occluders(S, asm)
        cand = spots(m, box, step=1.0 if stl.endswith("/Wrist") else 3.0)
        if len(cand) > max_spots:
            cand = [cand[i] for i in sorted(np.random.default_rng(0).choice(len(cand), max_spots, replace=False))]
        by_face = defaultdict(list)
        for x, y, z, sg, rot in cand:
            f = hidden_fraction(occ, R @ np.array([x, y, z]) + t, R @ np.array([0, 0, sg]), rays)
            if f >= 1.0:
                by_face[("up" if sg > 0 else "bed", z)].append((x, y, rot))
        for face, pts in by_face.items():
            cx, cy = np.mean([p[0] for p in pts]), np.mean([p[1] for p in pts])
            x, y, rot = min(pts, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
            FreeCAD.Console.PrintMessage(f"{stl}: {face[0]} face z={face[1]}: {len(pts)} hidden spots, "
                                         f"most central ({x:.1f}, {y:.1f}) rot {rot}\n")
    S.reset()


main()
