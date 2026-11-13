# -*- coding: utf-8 -*-
"""Export a light glTF (.glb) of the assembly for the guide's 3D viewer.

Run in the FreeCAD GUI with guide_render_lib available (see scripts/render_guide.FCMacro):
    exec(open("/path/to/spotmicro-arduino-q/scripts/export_guide_glb.py").read())
Tessellates every visible part (minus covers, screws, nuts and dampeners) at TOLERANCE mm, merges the triangles by
colour into one mesh each, and writes site/public/models/spot-unoq.glb. Normals are smooth within each B-rep face and sharp
between faces.
"""
import json
import os
import re
import struct
import sys

import numpy as np
import FreeCAD
import Mesh

_SCRIPTS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(
    os.environ.get("SPOT_ROOT", "/Users/jberi/code/robotics/spot-unoq"), "scripts")
sys.path.insert(0, _SCRIPTS)
import guide_render_lib as G  # noqa: E402

REPO = os.path.dirname(_SCRIPTS)
OUT = os.path.join(REPO, "site", "public", "models", "spot-unoq.glb")
TOLERANCE = 0.5
MAX_TRIS = 5000           # parts with more triangles are decimated down to about this
SKIP = re.compile(r"Top_Cover|Bottom_Cover|Cover_Nuts|Top_and_Bottom|FPC|Nut|M2x|M3x|Dampener|Screws|wire|Gear|Part01[01]")


def tris(o, parents):
    """Triangles of `o` in global coordinates; `parents` is the App::Part placement above it."""
    if o.TypeId == "Mesh::Feature":
        m = o.Mesh.copy()
        m.Placement = parents.multiply(o.Placement)
        pts, faces = m.Topology
    else:
        s = o.Shape.copy()
        s.Placement = parents.multiply(s.Placement)
        # Face by face, so vertices aren't shared across edges: smooth normals then stay sharp at part edges.
        pts, faces = [], []
        for face in s.Faces:
            fp, ff = face.tessellate(TOLERANCE)
            base = len(pts)
            pts += fp
            faces += [(a + base, b + base, c + base) for a, b, c in ff]
    if not faces:
        return None, None
    if len(faces) > MAX_TRIS:
        m = Mesh.Mesh()
        m.addFacets([[tuple(pts[i]) for i in f] for f in faces])
        m.removeDuplicatedPoints()
        m.decimate(0.5, 1.0 - MAX_TRIS / len(faces))
        pts, faces = m.Topology
    return np.array([(p.x, p.y, p.z) for p in pts], np.float32), np.array(faces, np.uint32)


def main():
    S = G.Scene(os.path.join(REPO, "cad", "SpotUnoQ.FCStd"))
    groups = {}
    for o, path in S.items:
        if not o.Visibility or SKIP.search(o.Label) or SKIP.search(o.Name):
            continue
        parents = FreeCAD.Placement()
        for name in path:
            parents = parents.multiply(S.doc.getObject(name).Placement)
        try:
            v, f = tris(o, parents)
        except Exception:  # links with no geometry
            continue
        if v is None:
            continue
        key = S.default_colour(o)
        groups.setdefault(key, []).append((v, f))

    # FreeCAD Z-up mm -> glTF Y-up metres, head towards -Z
    def convert(v):
        return np.stack([v[:, 1], v[:, 2], -v[:, 0]], axis=1) / 1000.0

    bin_parts, views, accessors, meshes, materials, nodes = [], [], [], [], [], []
    offset = 0

    def add_view(data, target):
        nonlocal offset
        b = data.tobytes()
        pad = (-len(b)) % 4
        bin_parts.append(b + b"\0" * pad)
        views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(b), "target": target})
        offset += len(b) + pad
        return len(views) - 1

    for i, (rgb, items) in enumerate(groups.items()):
        vs, fs, base = [], [], 0
        for v, f in items:
            vs.append(v)
            fs.append(f + base)
            base += len(v)
        v = convert(np.concatenate(vs)).astype(np.float32)
        f = np.concatenate(fs).astype(np.uint32).ravel()
        tri = f.reshape(-1, 3)
        fn = np.cross(v[tri[:, 1]] - v[tri[:, 0]], v[tri[:, 2]] - v[tri[:, 0]])  # area-weighted face normals
        n = np.zeros_like(v)
        for k in range(3):
            np.add.at(n, tri[:, k], fn)
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        pv = add_view(v, 34962)
        accessors.append({"bufferView": pv, "componentType": 5126, "count": len(v), "type": "VEC3",
                          "min": v.min(0).tolist(), "max": v.max(0).tolist()})
        nv = add_view(n.astype(np.float32), 34962)
        accessors.append({"bufferView": nv, "componentType": 5126, "count": len(n), "type": "VEC3"})
        fv = add_view(f, 34963)
        accessors.append({"bufferView": fv, "componentType": 5125, "count": len(f), "type": "SCALAR"})
        shown = (0.42, 0.45, 0.50) if rgb == G.C_PRINT else rgb  # a bit darker than the renders: PBR lighting is brighter
        materials.append({"pbrMetallicRoughness": {"baseColorFactor": [*shown, 1.0],
                                                   "metallicFactor": 0.3 if rgb in (G.C_STEEL, G.C_HORN) else 0.0,
                                                   "roughnessFactor": 0.75}})
        meshes.append({"primitives": [{"attributes": {"POSITION": len(accessors) - 3, "NORMAL": len(accessors) - 2},
                                       "indices": len(accessors) - 1, "material": i}]})
        nodes.append({"mesh": i})

    blob = b"".join(bin_parts)
    gltf = {"asset": {"version": "2.0", "generator": "spotmicro-arduino-q export_guide_glb.py"},
            "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
            "materials": materials, "accessors": accessors, "bufferViews": views,
            "buffers": [{"byteLength": len(blob)}]}
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((-len(js)) % 4)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob)))
        fh.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        fh.write(struct.pack("<II", len(blob), 0x004E4942) + blob)
    FreeCAD.Console.PrintMessage(f"glb: {OUT} {os.path.getsize(OUT) / 1e6:.1f} MB, "
                                 f"{sum(a['count'] for a in accessors if a['type'] == 'SCALAR') // 3} triangles\n")
    S.reset()


main()
