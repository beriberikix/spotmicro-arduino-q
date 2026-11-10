# Build the printable STL set in stl/ from the project CAD and the upstream parts.
# Run with freecadcmd from the repository root, after scripts/fetch-references.sh and the
# manual Thingiverse downloads (see README.md):
#
#   /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_stls.py
#
# Each entry: (folder, source, output name, normal copies, mirrored copies, material, infill, note).
# A part with mirrored copies is also written as <name>_mirrored.stl (mirrored across X).
# Quantities and infill follow Kubina's parts list; robjk's parts replace the matching Kooba parts.
import os
import shutil

import FreeCAD
import Mesh
import MeshPart

ROOT = os.path.abspath(os.environ.get("SPOT_ROOT", os.getcwd()))  # freecadcmd does not set __file__
REF = os.path.join(ROOT, "reference")
OUT = os.path.join(ROOT, "stl")

KOOBA = "kooba/files/"
ROBJK = "robjk/files/"
STAND = "leika/helper_stand/"
PLATE = "cad:UnoQ_Mountingplate"
SENSORMOUNT = "cad:Sensormount_DualCam"
CARRIER_TEST = "cad:Carrier_Mount_Test"
SZBK07_TEST = "cad:SZBK07_Mount_Test"

PARTS = [
    # Chassis
    ("chassis", KOOBA + "Inner_Shoulder.stl", "Inner_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Outer_Shoulder.stl", "Outer_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Chassis_Side.stl", "Chassis_Side", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Top_Shoulder.stl", "Top_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Bottom_Shoulder.stl", "Bottom_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "LiPo_Mountingbracket_Front.stl", "LiPo_Mountingbracket_Front", 1, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "LiPo_Mountingbracket_Middle.stl", "LiPo_Mountingbracket_Middle", 1, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "LiPo_Mountingbracket_Rear.stl", "LiPo_Mountingbracket_Rear", 1, 0, "PLA", "20%", ""),
    ("electronics", PLATE, "UnoQ_Mountingplate", 1, 0, "PLA", "20%", "New: UNO Media Carrier + UNO Q + servo shield stack, SZBK07, GY-521"),
    # Shoulder joints (robjk reinforced)
    ("shoulders", ROBJK + "Shoulder_Joint_Servomount_extended_BB.stl", "Shoulder_Joint_Servomount_extended_BB", 2, 2, "PLA", "20%", "robjk"),
    ("shoulders", ROBJK + "Shoulder_Joint_Servo_Cap_Extended.stl", "Shoulder_Joint_Servo_Cap_Extended", 4, 0, "PLA", "20%", "robjk"),
    ("shoulders", ROBJK + "Shoulder_Cover.stl", "Shoulder_Cover", 4, 0, "PLA", "20%", "robjk; symmetric, no mirrored copy"),
    ("shoulders", ROBJK + "Shoulder_Joint_Ball_Bearing_Pin_M3x8.stl", "Shoulder_Joint_Ball_Bearing_Pin_M3x8", 4, 0, "PLA", "20%", "robjk; runs in the shoulder-cover bearing, M3x8 into the upper-leg shell"),
    ("shoulders", KOOBA + "Shoulder_Joint_Ball_Bearing_Pin.stl", "Shoulder_Joint_Ball_Bearing_Pin", 8, 0, "PLA", "20%", "4 for the shoulder joints, 4 for the legs"),
    # Legs
    ("legs", ROBJK + "Limb_Top_Shell_with_BB_hole.stl", "Limb_Top_Shell_with_BB_hole", 2, 2, "PLA", "20%", "robjk; replaces Limb_Top_Shell"),
    ("legs", KOOBA + "Limb_Bottom_Shell.stl", "Limb_Bottom_Shell", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Limb_Ball_Bearing_Mount_long_v4.stl", "Limb_Ball_Bearing_Mount_long_v4", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Limb_Servohorn_Mount_long_v4.stl", "Limb_Servohorn_Mount_long_v4", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Wrist.stl", "Wrist", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Wrist__Counterpart.stl", "Wrist_Counterpart", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Foot_Tip.stl", "Foot_Tip", 4, 0, "TPU", "20%", ""),
    # Hull
    ("hull", KOOBA + "Top_Cover_Split_Front.stl", "Top_Cover_Split_Front", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Top_Cover_Split_Rear_with_OLED.stl", "Top_Cover_Split_Rear_with_OLED", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Bottom_Cover_Split_Front.stl", "Bottom_Cover_Split_Front", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Bottom_Cover_Split_Rear.stl", "Bottom_Cover_Split_Rear", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Rear_Cover_Shell_Long.stl", "Rear_Cover_Shell_Long", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Rear_Cover_Plate.stl", "Rear_Cover_Plate", 1, 0, "PLA", "100%", ""),
    # Head
    ("head", KOOBA + "Front_Cover_Optimized.stl", "Front_Cover_Optimized", 1, 0, "PLA", "100%", ""),
    ("head", SENSORMOUNT, "Sensormount_DualCam", 1, 0, "PLA", "20%", "New: Kooba's sensor mount, holding two Raspberry Pi Camera Module 2s"),
    # Optional
    ("optional/servo-horns", KOOBA + "Servohorn_6_B_Star.stl", "Servohorn_6_B_Star", 12, 0, "PLA", "20%", "Only if your servos lack FSH6S-type horns"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Shell_Medium.stl", "Rear_Cover_Shell_Medium", 1, 0, "PLA", "100%", "robjk; shorter alternative to Rear_Cover_Shell_Long"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Plate_Medium.stl", "Rear_Cover_Plate_Medium", 1, 0, "PLA", "100%", "robjk; pairs with Rear_Cover_Shell_Medium; OLED and 2x GX16 cut-outs"),
    ("optional/helper-stand", STAND + "2x_stand_top.stl", "Stand_Top", 2, 0, "PLA", "20%", "stefi01"),
    ("optional/helper-stand", STAND + "2x_stand_bottom.stl", "Stand_Bottom", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "2x_stand_brace.stl", "Stand_Brace", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "4x_stand_feet.stl", "Stand_Feet", 4, 0, "PLA", "20%", "Nova-SM2"),
    # Fit tests: the board-stack and regulator mounts from the electronics plate, on a light frame
    ("optional/test-prints", CARRIER_TEST, "Carrier_Mount_Test", 1, 0, "PLA", "20%", "Media Carrier pads, hooks and snap clips from the electronics plate"),
    ("optional/test-prints", SZBK07_TEST, "SZBK07_Mount_Test", 1, 0, "PLA", "20%", "SZBK07 posts from the electronics plate"),
]

def export_body(dest, fcstd, label, step_dest):
    """Mesh a PartDesign body of this project in its file's assembled position (Kooba's print
    orientation for the head parts; flat for the plates) and write its STEP alongside."""
    doc = FreeCAD.openDocument(os.path.join(ROOT, "cad", fcstd), hidden=True)
    body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body" and o.Label == label][0]
    shape = body.Shape.copy()
    shape.Placement = body.getGlobalPlacement()
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False).write(dest)
    os.makedirs(os.path.dirname(step_dest), exist_ok=True)
    shape.exportStep(step_dest)
    FreeCAD.closeDocument(doc.Name)


def export_mount_test(dest, which, base=2.0, bar=7.0):
    """Cut the real carrier pads and clips (or SZBK07 posts) out of the electronics plate and join them
    with a thin frame, so their positions, heights and pilot holes can be checked in a short print."""
    import math
    import Part
    doc = FreeCAD.openDocument(os.path.join(ROOT, "cad", "UnoQ_Mountingplate.FCStd"), hidden=True)
    body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body" and o.Label == "UnoQ Mountingplate Base"][0]
    P = doc.getObject("Params")
    V = FreeCAD.Vector
    top = 5.0
    if which == CARRIER_TEST:
        sk = doc.getObject("UnoQ_Standoffs_Sketch")  # the carrier pads
        pads = [(g.Center.x, g.Center.y) for g in sk.Geometry]
        cutters = [Part.makeCylinder(P.Standoff_D / 2 + 0.01, P.Standoff_H + 0.01, V(x, y, top)) for x, y in pads]
        clips = []
        for o in doc.Objects:
            if o.TypeId == "PartDesign::Pad" and o.Label.startswith(("Carrier_Hook", "Carrier_Snap")):
                b = o.Profile[0].Shape.BoundBox
                clips.append(((b.XMin + b.XMax) / 2, b.YMin))
                cutters.append(Part.makeBox(b.XLength + 0.02, P.Clip_W + 0.02, b.ZMax - top + 0.01,
                                            V(b.XMin - 0.01, b.YMin - P.Clip_W / 2 - 0.01, top)))
        pts, holes, post_d = pads + clips, [], P.Standoff_D
    else:
        pts = [(P.Buck_CX + sx * P.Buck_SX / 2, P.Buck_CY + sy * P.Buck_SY / 2) for sx in (-1, 1) for sy in (-1, 1)]
        cutters = [Part.makeCylinder(P.Buck_Post_D / 2 + 0.01, P.Buck_H + 0.01, V(x, y, top)) for x, y in pts]
        holes, post_d = pts, P.Buck_Post_D
    posts = body.Shape.common(Part.makeCompound(cutters))
    posts.translate(V(0, 0, base - top))
    cx = sum(x for x, _ in pts) / len(pts)
    cy = sum(y for _, y in pts) / len(pts)
    ring = sorted(pts, key=lambda q: math.atan2(q[1] - cy, q[0] - cx))
    pieces = []
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        b = Part.makeBox(math.hypot(x2 - x1, y2 - y1), bar, base, V(0, -bar / 2, 0))
        b.rotate(V(0, 0, 0), V(0, 0, 1), math.degrees(math.atan2(y2 - y1, x2 - x1)))
        b.translate(V(x1, y1, 0))
        pieces.append(b)
    pieces += [Part.makeCylinder(max(bar, post_d) / 2 + 1, base, V(x, y, 0)) for x, y in pts]
    frame = pieces[0].fuse(pieces[1:]).removeSplitter()
    if holes:
        frame = frame.cut(Part.makeCompound([Part.makeCylinder(P.Buck_Screw_D / 2, base + 1, V(x, y, -0.5)) for x, y in holes]))
    shape = frame.fuse(posts).removeSplitter()
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False).write(dest)
    FreeCAD.closeDocument(doc.Name)


# robjk exported these two in their assembled position, not lying the way they print. These
# rotations are the ones Bambu Studio's auto-orient chose for them (and that slice with no
# floating-region warning). Rows give where the part's X, Y and Z axes go.
PRINT_ROTATION = {
    "Shoulder_Joint_Servo_Cap_Extended": ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    "Shoulder_Cover": ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
}


def to_print_position(path, name):
    """Apply any print rotation, then centre the part in X/Y and put its lowest point at Z = 0."""
    m = Mesh.Mesh(path)
    if name in PRINT_ROTATION:
        r = PRINT_ROTATION[name]
        mat = FreeCAD.Matrix()
        mat.A11, mat.A12, mat.A13 = r[0][0], r[1][0], r[2][0]
        mat.A21, mat.A22, mat.A23 = r[0][1], r[1][1], r[2][1]
        mat.A31, mat.A32, mat.A33 = r[0][2], r[1][2], r[2][2]
        m.transform(mat)
    b = m.BoundBox
    m.translate(-(b.XMin + b.XMax) / 2, -(b.YMin + b.YMax) / 2, -b.ZMin)
    m.write(path)


def mirrored(src, dest):
    m = Mesh.Mesh(src)
    mat = FreeCAD.Matrix()
    mat.A11 = -1
    m.transform(mat)
    m.flipNormals()  # a reflection reverses facet winding
    if m.Volume < 0:
        m.flipNormals()
    m.write(dest)


def main():
    if os.path.isdir(OUT):
        for entry in os.listdir(OUT):
            path = os.path.join(OUT, entry)
            if os.path.isdir(path):
                shutil.rmtree(path)
    rows = []
    for folder, src, name, n, m, mat, infill, note in PARTS:
        d = os.path.join(OUT, folder)
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, name + ".stl")
        if src == PLATE:
            export_body(dest, "UnoQ_Mountingplate.FCStd", "UnoQ Mountingplate Base",
                        os.path.join(ROOT, "step", "electronics", "UnoQ_Mountingplate.step"))
        elif src == SENSORMOUNT:
            export_body(dest, "Sensormount_DualCam.FCStd", "Sensormount_DualCam",
                        os.path.join(ROOT, "step", "head", "Sensormount_DualCam.step"))
        elif src in (CARRIER_TEST, SZBK07_TEST):
            export_mount_test(dest, src)
        else:
            Mesh.Mesh(os.path.join(REF, src)).write(dest)  # rewrite as binary STL
        to_print_position(dest, name)
        files = [f"{folder}/{name}.stl"]
        if m:
            mirrored(dest, os.path.join(d, name + "_mirrored.stl"))
            files.append(f"{folder}/{name}_mirrored.stl")
        rows.append((folder, name, n, m, mat, infill, note, files))
        print("wrote", *files)
    # MIT requires the license text to travel with redistributed copies.
    shutil.copy(os.path.join(ROOT, "licenses", "Nova-SM2-MIT.txt"),
                os.path.join(OUT, "optional", "helper-stand", "LICENSE-Nova-SM2.txt"))
    write_readme(rows)


def write_readme(rows):
    lines = [
        "# Printable parts",
        "",
        "Generated by `scripts/export_stls.py`; do not edit by hand.",
        "Print every part without supports at 0.2 mm layers. Quantities are per robot.",
        "`_mirrored` files are the left-hand copies of parts that come in pairs.",
        "Every part is in its print orientation, centred, with its lowest point at Z = 0.",
        "",
        "Sources and licenses: Kooba's SpotMicroESP32 and robjk's reinforced shoulders (CC BY, Thingiverse",
        "thing:4559827 and thing:4937631), the helper stand from Leika (stefi01, CC BY 4.0; Nova-SM2, MIT), and",
        "`electronics/UnoQ_Mountingplate.stl` and `head/Sensormount_DualCam.stl` (this project, modified from Kooba,",
        "CC BY-SA 4.0). See ../NOTICE.md.",
        "",
    ]
    current = None
    total = 0
    for folder, name, n, m, mat, infill, note, files in rows:
        if folder != current:
            lines += ["", f"## {folder}", "", "| File | Normal | Mirrored | Material | Infill | Notes |", "| ---- | ------ | -------- | -------- | ------ | ----- |"]
            current = folder
        links = " · ".join(f"[{os.path.basename(f)}]({f})" for f in files)
        lines.append(f"| {links} | {n} | {m or '-'} | {mat} | {infill} | {note} |")
        if not folder.startswith("optional"):
            total += n + m
    lines += ["", f"Required prints: {total} parts.", ""]
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("\n".join(lines))


main()
