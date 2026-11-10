# Export STEP versions of the printable parts into step/, matching stl/ exactly (same print
# orientation and position), from the designers' FreeCAD sources. Run after scripts/export_stls.py:
#
#   /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_steps.py
#
# Each source solid is fitted to its STL by point-cloud registration (24 axis-aligned starts,
# refined with ICP); a part is only written when 95% of points sampled on the STL lie within
# FIT_LIMIT of the placed STEP surface (STL facets approximate large curved covers to about 0.06 mm). Mirrored STLs get
# mirrored STEPs. Parts that exist only as STL upstream (robjk's extended servo mount and M3
# bearing pin) have no STEP.
import itertools
import os

import FreeCAD
import Mesh
import numpy as np
import Part
from scipy.spatial import cKDTree

ROOT = os.path.abspath(os.environ.get("SPOT_ROOT", os.getcwd()))
STL = os.path.join(ROOT, "stl")
OUT = os.path.join(ROOT, "step")
KOOBA = os.path.join(ROOT, "reference", "kooba", "files")
ROBJK = os.path.join(ROOT, "reference", "robjk", "files")
FIT_LIMIT = 0.1  # mm: 95th percentile distance from STL surface samples to the placed STEP surface

# (stl path relative to stl/, source FCStd, object labels to use or None for the visible roots, mirrored copy?)
PARTS = [
    ("chassis/Inner_Shoulder.stl", f"{KOOBA}/Inner_Shoulder.FCStd", None, False),
    ("chassis/Outer_Shoulder.stl", f"{KOOBA}/Outer_Shoulder.FCStd", None, False),
    ("chassis/Chassis_Side.stl", f"{KOOBA}/Chassis_Side.FCStd", None, False),
    ("chassis/Top_Shoulder.stl", f"{KOOBA}/Top_Shoulder.FCStd", None, False),
    ("chassis/Bottom_Shoulder.stl", f"{KOOBA}/Bottom_Shoulder.FCStd", None, False),
    ("chassis/LiPo_Mountingbracket_Front.stl", f"{KOOBA}/LiPo_Mountingbracket_Front.FCStd", None, False),
    ("chassis/LiPo_Mountingbracket_Middle.stl", f"{KOOBA}/LiPo_Mountingbracket_Middle.FCStd", None, False),
    ("chassis/LiPo_Mountingbracket_Rear.stl", f"{KOOBA}/LiPo_Mountingbracket_Rear.FCStd", None, False),
    ("shoulders/Shoulder_Joint_Servo_Cap_Extended.stl", f"{ROBJK}/Limb_Top_Shell_mod.FCStd", ["Shoulder_Joint_Servohorn_Cap"], False),
    ("shoulders/Shoulder_Cover.stl", f"{ROBJK}/Limb_Top_Shell_mod.FCStd", ["Shoulder Cover"], False),
    ("shoulders/Shoulder_Joint_Ball_Bearing_Pin.stl", f"{KOOBA}/Shoulder_Joint_Ball_Bearing_Pin.FCStd", None, False),
    ("legs/Limb_Top_Shell_with_BB_hole.stl", f"{ROBJK}/Limb_Top_Shell_mod.FCStd", ["Limb_Top_Shell"], True),
    ("legs/Limb_Bottom_Shell.stl", f"{KOOBA}/Limb_Bottom_Shell.FCStd", ["Limb_Bottom_Shell"], True),
    ("legs/Limb_Ball_Bearing_Mount_long_v4.stl", f"{KOOBA}/Limb_Ball_Bearing_Mount_long_v4.FCStd", None, True),
    ("legs/Limb_Servohorn_Mount_long_v4.stl", f"{KOOBA}/Limb_Servohorn_Mount_long_v4.FCStd", None, True),
    ("legs/Wrist.stl", f"{KOOBA}/Wrist.FCStd", None, True),
    ("legs/Wrist_Counterpart.stl", f"{KOOBA}/Wrist__Counterpart.FCStd", None, True),
    ("legs/Foot_Tip.stl", f"{KOOBA}/Foot_Tip.FCStd", None, False),
    ("hull/Top_Cover_Split_Front.stl", f"{KOOBA}/Top_Cover_Split_Front.FCStd", None, False),
    ("hull/Top_Cover_Split_Rear_with_OLED.stl", f"{KOOBA}/Top_Cover_Split_Rear_with_OLED.FCStd", None, False),
    ("hull/Bottom_Cover_Split_Front.stl", f"{KOOBA}/Bottom_Cover_Split_Front.FCStd", ["Bottom_Cover_Split_Front"], False),
    ("hull/Bottom_Cover_Split_Rear.stl", f"{KOOBA}/Bottom_Cover_Split_Rear.FCStd", ["Bottom_Cover_Split_Rear"], False),
    ("hull/Rear_Cover_Shell_Long.stl", f"{KOOBA}/Rear_Cover_Shell_Long.FCStd", None, False),
    ("hull/Rear_Cover_Plate.stl", f"{KOOBA}/Rear_Cover_Plate.FCStd", None, False),
    ("head/Front_Cover_Optimized.stl", f"{KOOBA}/Front_Cover_Optimized.FCStd", None, False),
    ("head/Sensormount.stl", f"{KOOBA}/sensormount_esp32_cam.FCStd", None, False),
    ("head/Cameramount_ESP32_CAM.stl", f"{KOOBA}/cameramount_esp32_cam.FCStd", None, False),
    ("head/Cameramount_ESP32_CAM_Counterpiece.stl", f"{KOOBA}/cameramount_esp32_cam_counterpiece.FCStd", None, False),
    ("optional/servo-horns/Servohorn_6_B_Star.stl", f"{KOOBA}/Servohorn_6_B_Star.FCStd", None, False),
    ("optional/rear-cover-medium/Rear_Cover_Shell_Medium.stl", f"{ROBJK}/Rear_Cover_Shell_Medium.FCStd", ["Rear_Cover_Shell_medium"], False),
    ("optional/rear-cover-medium/Rear_Cover_Plate_Medium.stl", f"{ROBJK}/Rear_Cover_Shell_Medium.FCStd", ["Rear_Cover_Plate_medium"], False),
]


def source_shape(path, labels):
    doc = FreeCAD.openDocument(path, hidden=True)
    if labels:
        objs = [o for o in doc.Objects if o.Label in labels and hasattr(o, "Shape")]
    else:
        # visible top-level solids (a hidden "Template" body sits beside the printable one in some files)
        objs = [o for o in doc.Objects if hasattr(o, "Shape") and o.Visibility and not o.Shape.isNull()
                and o.Shape.Solids and not [p for p in o.InList if p.Document == doc]]
    shapes = []
    for o in objs:
        s = o.Shape.copy()
        parent = o.getGlobalPlacement().multiply(o.Placement.inverse())
        s.Placement = parent.multiply(s.Placement)
        shapes.append(s)
    FreeCAD.closeDocument(doc.Name)
    if not shapes:
        raise RuntimeError(f"no source solids in {os.path.basename(path)} for {labels}")
    return shapes[0] if len(shapes) == 1 else Part.makeCompound(shapes)


def sample_shape(shape, n, seed):
    v, f = shape.tessellate(0.2)
    return sample_triangles(np.array([[p.x, p.y, p.z] for p in v]), np.array(f), n, seed)


def sample_mesh(mesh, n, seed):
    pts = np.array([[p.x, p.y, p.z] for p in mesh.Points])
    tris = np.array([f.PointIndices for f in mesh.Facets])
    return sample_triangles(pts, tris, n, seed)


def sample_triangles(P, F, n, seed):
    a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
    area = np.linalg.norm(np.cross(b - a, c - a), axis=1) / 2
    rng = np.random.default_rng(seed)
    i = rng.choice(len(F), n, p=area / area.sum())
    r1 = np.sqrt(rng.random(n))[:, None]
    r2 = rng.random(n)[:, None]
    return (1 - r1) * a[i] + r1 * (1 - r2) * b[i] + r1 * r2 * c[i]


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0)
    U, _, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1
        R = Vt.T @ U.T
    return R, cb - R @ ca


def rotations():
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for row, (col, s) in enumerate(zip(perm, signs)):
                M[row, col] = s
            if np.linalg.det(M) > 0:
                yield M


def fit(src, dst):
    """Rigid transform taking src onto dst; returns (R, t, median distance)."""
    tree = cKDTree(dst)
    best = None
    for R in rotations():
        t = dst.mean(0) - R @ src.mean(0)
        for _ in range(40):
            Y = src @ R.T + t
            d, i = tree.query(Y)
            keep = np.argsort(d)[: int(len(d) * 0.9)]
            R2, t2 = kabsch(Y[keep], dst[i[keep]])
            R, t = R2 @ R, R2 @ t + t2
        d, _ = tree.query(src @ R.T + t)
        if best is None or np.median(d) < best[2]:
            best = (R, t, float(np.median(d)))
    return best


def matrix(R, t):
    return FreeCAD.Matrix(R[0, 0], R[0, 1], R[0, 2], t[0], R[1, 0], R[1, 1], R[1, 2], t[1],
                          R[2, 0], R[2, 1], R[2, 2], t[2], 0, 0, 0, 1)


def main():
    results = []
    for rel, src, labels, mirror in PARTS:
        shape = source_shape(src, labels)
        stl_mesh = Mesh.Mesh(os.path.join(STL, rel))
        R, t, _ = fit(sample_shape(shape, 4000, 1), sample_mesh(stl_mesh, 30000, 2))
        placed = shape.copy()
        placed.transformShape(matrix(R, t))
        # true point-to-surface distances from the STL to the placed solid
        dists = [placed.distToShape(Part.Vertex(FreeCAD.Vector(*p)))[0] for p in sample_mesh(stl_mesh, 200, 4)]
        med, back = float(np.median(dists)), float(np.percentile(dists, 95))
        ok = back <= FIT_LIMIT
        results.append((rel, med, back, ok))
        if not ok:
            print(f"SKIP {rel}: median {med:.3f} mm, 95th percentile {back:.3f} mm")
            continue
        dest = os.path.join(OUT, rel[:-4] + ".step")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        placed.exportStep(dest)
        written = [os.path.relpath(dest, ROOT)]
        if mirror:
            m = placed.mirror(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0))
            mdest = dest[:-5] + "_mirrored.step"
            m.exportStep(mdest)
            written.append(os.path.relpath(mdest, ROOT))
        print(f"wrote {' '.join(written)}  (median {med:.3f} mm, 95th pct {back:.3f} mm)")
    bad = [r for r in results if not r[3]]
    print(f"{len(results) - len(bad)} of {len(results)} parts written")


main()
