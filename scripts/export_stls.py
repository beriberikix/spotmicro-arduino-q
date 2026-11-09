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
    ("electronics", PLATE, "UnoQ_Mountingplate", 1, 0, "PLA", "20%", "New: UNO Q, PCA9685, GY-521, Pololu D24V150F6"),
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
    ("head", KOOBA + "sensormount_esp32_cam.stl", "Sensormount", 1, 0, "PLA", "20%", "Holds the two HC-SR04s"),
    ("head", KOOBA + "cameramount_esp32_cam.stl", "Cameramount_ESP32_CAM", 1, 0, "PLA", "20%", "ESP32-CAM mount, kept until a UNO Q camera mount exists"),
    ("head", KOOBA + "cameramount_esp32_cam_counterpiece.stl", "Cameramount_ESP32_CAM_Counterpiece", 1, 0, "PLA", "20%", "As above"),
    # Optional
    ("optional/servo-horns", KOOBA + "Servohorn_6_B_Star.stl", "Servohorn_6_B_Star", 12, 0, "PLA", "20%", "Only if your servos lack FSH6S-type horns"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Shell_Medium.stl", "Rear_Cover_Shell_Medium", 1, 0, "PLA", "100%", "robjk; shorter alternative to Rear_Cover_Shell_Long"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Plate_Medium.stl", "Rear_Cover_Plate_Medium", 1, 0, "PLA", "100%", "robjk; pairs with Rear_Cover_Shell_Medium; OLED and 2x GX16 cut-outs"),
    ("optional/helper-stand", STAND + "2x_stand_top.stl", "Stand_Top", 2, 0, "PLA", "20%", "stefi01"),
    ("optional/helper-stand", STAND + "2x_stand_bottom.stl", "Stand_Bottom", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "2x_stand_brace.stl", "Stand_Brace", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "4x_stand_feet.stl", "Stand_Feet", 4, 0, "PLA", "20%", "Nova-SM2"),
]

def export_plate(dest):
    doc = FreeCAD.openDocument(os.path.join(ROOT, "cad", "UnoQ_Mountingplate.FCStd"), hidden=True)
    body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body" and o.Label == "UnoQ Mountingplate Base"][0]
    shape = body.Shape.copy()
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False).write(dest)
    shape.exportStep(os.path.join(ROOT, "cad", "export", "UnoQ_Mountingplate.step"))
    FreeCAD.closeDocument(doc.Name)


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
            export_plate(dest)
        else:
            Mesh.Mesh(os.path.join(REF, src)).write(dest)  # rewrite as binary STL
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
        "",
        "Sources and licenses: Kooba's SpotMicroESP32 and robjk's reinforced shoulders (CC BY, Thingiverse",
        "thing:4559827 and thing:4937631), the helper stand from Leika (stefi01, CC BY 4.0; Nova-SM2, MIT), and",
        "`electronics/UnoQ_Mountingplate.stl` (this project, CC BY-SA 4.0). See ../NOTICE.md.",
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
