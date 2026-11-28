# Build the printable STL set in stl/ from the project CAD and the upstream parts.
# Run with freecadcmd from the repository root, after scripts/fetch-references.sh and the
# manual Thingiverse downloads (see README.md):
#
#   /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_stls.py
#
# Each entry: (folder, source, output name, normal copies, mirrored copies, material, infill, note).
# A part with mirrored copies is also written as <name>_mirrored.stl (mirrored across X).
# Quantities and infill follow Kubina's parts list; robjk's parts replace the matching Kooba parts.
import math
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
IMU_TEST = "cad:IMU_Mount_Test"
BATTERY_RAIL_SRC = "gen:battery_rail"
KOOBA_MOD = "mod:kooba"  # one of Kooba's covers, changed by KOOBA_MODS below

PARTS = [
    # Chassis
    ("chassis", KOOBA + "Inner_Shoulder.stl", "Inner_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Outer_Shoulder.stl", "Outer_Shoulder", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Chassis_Side.stl", "Chassis_Side", 2, 0, "PLA", "20%", ""),
    ("chassis", KOOBA + "Top_Shoulder.stl", "Top_Shoulder", 2, 0, "PLA", "20%", "2 mm longer than Kooba's (49.5 mm), for shoulder clearance"),
    ("chassis", KOOBA + "Bottom_Shoulder.stl", "Bottom_Shoulder", 2, 0, "PLA", "20%", "2 mm longer than Kooba's (49.5 mm), for shoulder clearance"),
    ("chassis", BATTERY_RAIL_SRC, "Battery_Rail", 2, 0, "PLA", "20%", "New: left and right of the 3S pack, two 20 mm hook-and-loop straps through their slots; replace Kooba's LiPo brackets"),
    ("electronics", PLATE, "UnoQ_Mountingplate", 1, 0, "PLA", "20%", "New: UNO Media Carrier + UNO Q + servo shield stack, SZBK07, Adafruit MPU-6050 (ribbed posts), carrier clamp posts and front stops"),
    # Shoulder joints (robjk reinforced)
    ("shoulders", ROBJK + "Shoulder_Joint_Servomount_extended_BB.stl", "Shoulder_Joint_Servomount_extended_BB", 2, 2, "PLA", "20%", "robjk; bearing-pin seat changed to M2"),
    ("shoulders", ROBJK + "Shoulder_Joint_Servo_Cap_Extended.stl", "Shoulder_Joint_Servo_Cap_Extended", 4, 0, "PLA", "20%", "robjk"),
    ("shoulders", ROBJK + "Shoulder_Cover.stl", "Shoulder_Cover", 4, 0, "PLA", "20%", "robjk; symmetric, no mirrored copy"),
    ("shoulders", KOOBA + "Shoulder_Joint_Ball_Bearing_Pin.stl", "Shoulder_Joint_Ball_Bearing_Pin", 12, 0, "PLA", "20%", "M2 bore, with an M2x8 and nut: 4 knees, 4 upper-leg shells, 4 shoulder servo mounts"),
    # Legs
    ("legs", ROBJK + "Limb_Top_Shell_with_BB_hole.stl", "Limb_Top_Shell_with_BB_hole", 2, 2, "PLA", "20%", "robjk; replaces Limb_Top_Shell; bearing-pin seat changed to M2"),
    ("legs", KOOBA + "Limb_Bottom_Shell.stl", "Limb_Bottom_Shell", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Limb_Ball_Bearing_Mount_long_v4.stl", "Limb_Ball_Bearing_Mount_long_v4", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Limb_Servohorn_Mount_long_v4.stl", "Limb_Servohorn_Mount_long_v4", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Wrist.stl", "Wrist", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Wrist__Counterpart.stl", "Wrist_Counterpart", 2, 2, "PLA", "20%", ""),
    ("legs", KOOBA + "Foot_Tip.stl", "Foot_Tip", 4, 0, "TPU", "20%", ""),
    # Hull
    ("hull", KOOBA_MOD, "Top_Cover_Split_Front", 1, 0, "PLA", "100%", "Seam flanges moved inwards, clear of the servo shield's terminal block"),
    ("hull", KOOBA_MOD, "Top_Cover_Split_Rear", 1, 0, "PLA", "100%", "From Top_Cover_Split_Rear_with_OLED: seam flanges moved to match the front half; OLED window, square opening and slits filled"),
    ("hull", KOOBA_MOD, "Bottom_Cover_Split_Front", 1, 0, "PLA", "100%", "Floor 6 mm lower, for a 3S pack"),
    ("hull", KOOBA_MOD, "Bottom_Cover_Split_Rear", 1, 0, "PLA", "100%", "Floor 6 mm lower, for a 3S pack"),
    ("hull", KOOBA + "Rear_Cover_Shell_Long.stl", "Rear_Cover_Shell_Long", 1, 0, "PLA", "100%", ""),
    ("hull", KOOBA + "Rear_Cover_Plate.stl", "Rear_Cover_Plate", 1, 0, "PLA", "100%", ""),
    # Head
    ("head", KOOBA_MOD, "Front_Cover_Optimized", 1, 0, "PLA", "100%", "Sensor screw bosses lowered 2.27 mm (nut pockets with them) to take the camera mount's ears"),
    ("head", SENSORMOUNT, "Sensormount_DualCam", 1, 0, "PLA", "20%", "New: Kooba's sensor mount, holding two Raspberry Pi Camera Module 2s, with four ears for the front cover's M3 screws"),
    # Optional
    ("optional/servo-horns", KOOBA + "Servohorn_6_B_Star.stl", "Servohorn_6_B_Star", 12, 0, "PLA", "20%", "Only if your servos lack FSH6S-type horns"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Shell_Medium.stl", "Rear_Cover_Shell_Medium", 1, 0, "PLA", "100%", "robjk; shorter alternative to Rear_Cover_Shell_Long"),
    ("optional/rear-cover-medium", ROBJK + "Rear_Cover_Plate_Medium.stl", "Rear_Cover_Plate_Medium", 1, 0, "PLA", "100%", "robjk; pairs with Rear_Cover_Shell_Medium; OLED and 2x GX16 cut-outs"),
    ("optional/helper-stand", STAND + "2x_stand_top.stl", "Stand_Top", 2, 0, "PLA", "20%", "stefi01; optional but recommended stand, hardware in ../BOM.md"),
    ("optional/helper-stand", STAND + "2x_stand_bottom.stl", "Stand_Bottom", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "2x_stand_brace.stl", "Stand_Brace", 2, 0, "PLA", "20%", "Nova-SM2"),
    ("optional/helper-stand", STAND + "4x_stand_feet.stl", "Stand_Feet", 4, 0, "PLA", "20%", "Nova-SM2"),
    # Fit tests: the board-stack and regulator mounts from the electronics plate, on a light frame
    ("optional/test-prints", CARRIER_TEST, "Carrier_Mount_Test", 1, 0, "PLA", "20%", "Media Carrier pads, clamp posts and front stops from the electronics plate"),
    ("optional/test-prints", SZBK07_TEST, "SZBK07_Mount_Test", 1, 0, "PLA", "20%", "SZBK07 posts from the electronics plate"),
    ("optional/test-prints", IMU_TEST, "IMU_Mount_Test", 1, 0, "PLA", "20%", "MPU-6050 posts and ribs, cut from the electronics plate at full thickness"),
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
    """Cut the real carrier pads, clamp posts and stops (or SZBK07 posts) out of the electronics plate and join them
    with a thin frame, so their positions, heights and pilot holes can be checked in a short print."""
    import math
    import Part
    doc = FreeCAD.openDocument(os.path.join(ROOT, "cad", "UnoQ_Mountingplate.FCStd"), hidden=True)
    body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body" and o.Label == "UnoQ Mountingplate Base"][0]
    P = doc.getObject("Params")
    V = FreeCAD.Vector
    top = 5.0
    if which == IMU_TEST:
        # the IMU posts, ribs and the full 5 mm plate under them: tests the fit and the posts' strength at their root
        b = doc.getObject("IMU_Ribs_Sketch").Shape.BoundBox
        m = 3.0
        cut = Part.makeBox(b.XLength + 2 * m, b.YLength + 2 * m, 50, V(b.XMin - m, b.YMin - m, -1))
        shape = body.Shape.common(cut).removeSplitter()
        MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False).write(dest)
        FreeCAD.closeDocument(doc.Name)
        return
    if which == CARRIER_TEST:
        sk = doc.getObject("UnoQ_Standoffs_Sketch")  # the carrier pads
        pads = [(g.Center.x, g.Center.y) for g in sk.Geometry]
        cutters = [Part.makeCylinder(P.Standoff_D / 2 + 0.01, P.Standoff_H + 0.01, V(x, y, top)) for x, y in pads]
        # the four clamp posts: an M3 screw and washer in each clamps the carrier's edge
        clips = [(g.Center.x, g.Center.y) for g in doc.getObject("Carrier_Clamp_Posts_Sketch").Geometry]
        cutters += [Part.makeCylinder(P.Clamp_D / 2 + 0.01, P.Standoff_H + P.Carrier_T, V(x, y, top)) for x, y in clips]
        stops = doc.getObject("Carrier_Stops")  # the two front stops that keep the carrier from sliding forwards
        for st in (stops.AddSubShape.Solids if stops else []):
            b = st.BoundBox
            clips.append(((b.XMin + b.XMax) / 2, (b.YMin + b.YMax) / 2))
            cutters.append(Part.makeBox(b.XLength + 0.02, b.YLength + 0.02, b.ZMax - top + 0.01,
                                        V(b.XMin - 0.01, b.YMin - 0.01, top)))
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


# Bearing-pin seats changed from M3 to M2. robjk's top shell and extended servo mount hold their bearing pin with an M3
# screw and nut, but an M3 cap head (5.5 mm) is wider than the 625ZZ's 5 mm bore, so the bearing can't slide over it.
# These fill the M3 hole and nut pocket and cut an M2 clearance hole and M2 nut pocket in the same place, so every pin
# is the M2-bore one with an M2x8 (head 3.8 mm) and nut, as on the knees. Positions are in the print position of the
# normal part (the mirrored copy is made from it afterwards).
# name: (pin axis; centre in the other two axes, in xyz order; outer face, back of the wall, inner face along the
#        axis; the axis the nut pocket's flats face)
M2_PIN_SEATS = {
    "Limb_Top_Shell_with_BB_hole": ("y", (32.2, 15.0), -18.26, -16.86, -14.51, "x"),
    "Shoulder_Joint_Servomount_extended_BB": ("x", (10.0, 15.0), -22.5, -21.0, -18.0, "y"),
}
M2_HOLE_D = 2.4   # M2 clearance
M2_NUT_AF = 4.3   # M2 nut is 4.0 mm across the flats, 1.6 mm thick
M3_PLUG = (3.8, 6.0)  # just over the old 3.1-3.2 mm hole and 5.6-5.7 mm pocket


def rebore_m2(path, name):
    import Part
    V = FreeCAD.Vector
    axis, (cu, cw), outer, wall, inner, flat = M2_PIN_SEATS[name]
    unit = {"x": V(1, 0, 0), "y": V(0, 1, 0), "z": V(0, 0, 1)}
    u, w = [k for k in "xyz" if k != axis]

    def at(t):
        d = {axis: t, u: cu, w: cw}
        return V(d["x"], d["y"], d["z"])

    def cyl(dia, t0, t1):
        return Part.makeCylinder(dia / 2, t1 - t0, at(t0), unit[axis])

    def hexagon(af, t0, t1):
        r, across = af / math.sqrt(3), (u if flat != u else w)
        pts = [at(t0) + unit[across] * (r * math.cos(math.radians(60 * k))) + unit[flat] * (r * math.sin(math.radians(60 * k)))
               for k in range(6)]
        return Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(unit[axis] * (t1 - t0))

    mesh = Mesh.Mesh(path)
    shell = Part.Shape()
    shell.makeShapeFromMesh(mesh.Topology, 0.05)
    solid = Part.makeSolid(shell)
    filled = solid.fuse(cyl(M3_PLUG[0], outer, wall).fuse(hexagon(M3_PLUG[1], wall, inner))).removeSplitter()
    added = filled.Volume - solid.Volume
    old = math.pi * 1.6 ** 2 * abs(wall - outer) + 1.5 * math.sqrt(3) * (5.65 / math.sqrt(3)) ** 2 * abs(inner - wall)
    step = 1 if inner > outer else -1
    cut = filled.cut(cyl(M2_HOLE_D, outer - step, inner).fuse(hexagon(M2_NUT_AF, wall, inner + 0.5 * step)))
    removed = filled.Volume - cut.Volume
    new = math.pi * (M2_HOLE_D / 2) ** 2 * abs(wall - outer) + 1.5 * math.sqrt(3) * (M2_NUT_AF / math.sqrt(3)) ** 2 * abs(inner - wall)
    if not cut.isValid() or abs(added - old) > 0.1 * old or abs(removed - new) > 0.05 * new:
        raise RuntimeError(f"{path}: M2 rebore filled {added:.1f} (expected ~{old:.1f}) and cut {removed:.1f} (expected {new:.1f}) mm3")
    MeshPart.meshFromShape(Shape=cut, LinearDeflection=0.02, AngularDeflection=0.2, Relative=False).write(path)


# Shoulder blocks made longer than Kooba's. As drawn, the leg between the outer and inner shoulders has no axial
# clearance (the bearing sits 0.25 mm deeper than its seat), and real horns, servos and prints only add to it: a
# measured build came out 1.5 mm too long, leaving the outer shoulder standing off the blocks. The extra length goes
# in the middle of the block, where it has no features, so the block stays symmetric, both nut slots stay 4.5 mm from
# their ends (M3x8 still reaches) and the cover screw holes keep their distance from each end: the head and rear
# covers move out with the legs, and nothing in the body moves.
# name: (axis in the print position, extra length in mm, half-width of the feature-free band at the middle)
LENGTHEN = {
    "Top_Shoulder": ("y", 2.0, 1.7),
    "Bottom_Shoulder": ("y", 2.0, 1.7),
}


def lengthen(path, name):
    """Stretch the mesh at the middle of its length: every vertex past the middle moves out by half the extra
    length. Only valid when no vertex lies in the band around the middle (so only straight faces span it)."""
    import Part
    axis, extra, band = LENGTHEN[name]
    k = "xyz".index(axis)
    mesh = Mesh.Mesh(path)
    pts, facets = mesh.Topology
    b = mesh.BoundBox
    mid = ((b.XMin + b.XMax) / 2, (b.YMin + b.YMax) / 2, (b.ZMin + b.ZMax) / 2)[k]
    if any(abs(p[k] - mid) < band for p in pts):
        raise RuntimeError(f"{path}: vertices inside the {2 * band} mm band at the middle; can't stretch there")
    moved = []
    for p in pts:
        c = [p.x, p.y, p.z]
        c[k] += extra / 2 if c[k] > mid else -extra / 2
        moved.append(FreeCAD.Vector(*c))
    out = Mesh.Mesh((moved, facets))
    # check: the added volume is the cross-section at the middle times the extra length
    shell = Part.Shape()
    shell.makeShapeFromMesh(mesh.Topology, 0.05)
    normal = FreeCAD.Vector(*[1 if i == k else 0 for i in range(3)])
    section = Part.Face(Part.makeSolid(shell).slice(normal, mid), "Part::FaceMakerBullseye").Area
    added = out.Volume - mesh.Volume
    if not out.isSolid() or abs(added - section * extra) > 0.01 * section * extra:
        raise RuntimeError(f"{path}: stretch added {added:.1f} mm3, expected {section * extra:.1f}")
    out.write(path)


# Side labels engraved into the parts that come in normal and mirrored versions, so a printed part says which leg
# it belongs to. Each label sits on a face that is horizontal as printed, so it adds no overhang: an upward face
# (the label is the last layers) or the bed face (the first layers, bridged by about 1 mm). Every spot was picked
# with scripts/find_label_spots.py as fully hidden once the robot is assembled.
# name: (x, y, z of the box centre on the face, in the print position of the normal part; "up"|"bed"; rotation in
#        degrees; (width, height) of the flat box the text is fitted into, in mm; normal-part text; mirrored-part text)
LABELS = {
    "Wrist": (-69.0, -1.5, 20.0, "up", 0, (7, 9), "L", "R"),
    "Wrist_Counterpart": (-2.8, 3.5, 5.0, "up", 0, (9, 9), "L", "R"),
    "Limb_Ball_Bearing_Mount_long_v4": (-5.7, 9.8, 0.0, "bed", 0, (9, 9), "L", "R"),
    "Limb_Servohorn_Mount_long_v4": (6.3, 9.8, 0.0, "bed", 0, (9, 9), "L", "R"),
    "Limb_Top_Shell_with_BB_hole": (-5.8, 9.2, 5.0, "up", 0, (9, 9), "L", "R"),
    "Limb_Bottom_Shell": (20.7, 10.0, 5.0, "up", 0, (9, 9), "L", "R"),
    # front-left and rear-right legs take the normal mount, front-right and rear-left the mirrored one
    "Shoulder_Joint_Servomount_extended_BB": (-1.5, -24.2, 25.0, "up", 0, (18, 8), "FL RR", "FR RL"),
}
LABEL_DEPTH = 0.6        # three 0.2 mm layers
LABEL_FONT = "Ubuntu-B.ttf"  # bundled with FreeCAD (Ubuntu Font Licence)


def engrave(path, x, y, z, face, rot, box, text):
    """Cut `text` LABEL_DEPTH deep into the horizontal face at (x, y, z), fitted inside `box` less a 1 mm margin and
    reading correctly when you look at that face (from above for "up", from below for "bed")."""
    import Part
    V = FreeCAD.Vector
    font = os.path.join(FreeCAD.getHomePath(), "fonts", LABEL_FONT)
    glyphs = Part.makeWireString(text, font, 10.0, 0.0)
    flat = Part.makeCompound([Part.Face(g, "Part::FaceMakerBullseye") for g in glyphs if g])
    b = flat.BoundBox
    flat.translate(V(-(b.XMin + b.XMax) / 2, -(b.YMin + b.YMax) / 2, 0))
    flat.scale(min((box[0] - 2) / b.XLength, (box[1] - 2) / b.YLength))
    if face == "bed":
        flat = flat.mirror(V(0, 0, 0), V(1, 0, 0))  # read from below; mirror() returns a new shape
    flat.rotate(V(0, 0, 0), V(0, 0, 1), rot)
    tool = flat.extrude(V(0, 0, LABEL_DEPTH + 1.0))
    tool.translate(V(x, y, z - LABEL_DEPTH) if face == "up" else V(x, y, z - 1.0))
    mesh = Mesh.Mesh(path)
    shell = Part.Shape()
    shell.makeShapeFromMesh(mesh.Topology, 0.05)
    solid = Part.makeSolid(shell)
    cut = solid.cut(tool)
    removed = solid.Volume - cut.Volume
    expected = flat.Area * LABEL_DEPTH
    if not cut.isValid() or abs(removed - expected) > 0.05 * expected:
        raise RuntimeError(f"{path}: label cut removed {removed:.1f} mm3, expected {expected:.1f}")
    MeshPart.meshFromShape(Shape=cut, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False).write(path)


def mirror_spot(x, y, z, face, rot):
    """The same spot on the mirrored part (mirrored across X), with the text kept the same way up."""
    return -x, y, z, face, rot


# Kooba covers changed for this build. Each is cut from Kooba's FreeCAD body (exact geometry, not the STL), in that
# body's own frame, which is also the frame of his STL; the result is meshed and its STEP written in the print position.
# Numbers below were checked against test prints.

# Front cover: its four sensor screw bosses held nothing, because the camera mount sits beside them. The mount now has
# four 2 mm ears flush with its back (cad/Sensormount_DualCam.FCStd, Cover_Ears), and each boss is lowered by
# HEAD_BOSS_DROP so the ear sits on it; the side-loaded nut pocket and the screw hole move down with it and keep the
# 1.65 mm cap, so the M3x8 still passes the whole nut. Worked in the frame of the assembled cover ("M": screw axes along
# +Z at x 14 / 100, y 20.5 / 48.5), which is Kooba's body frame moved by HEAD_FRAME.
HEAD_FRAME = (0.0, 14.457226, -31.814962)
HEAD_BOSSES = [(14.0, 20.5, -1), (100.0, 48.5, 1), (14.0, 48.5, -1), (100.0, 20.5, 1)]  # x, y, side (-1 left, 1 right)
HEAD_BOSS_TOP = 10.07
HEAD_BOSS_DROP = 2.27


def mod_front_cover(shape):
    import Part
    V = FreeCAD.Vector
    t = V(*HEAD_FRAME)
    cov = shape.copy()
    cov.translate(t)
    top = HEAD_BOSS_TOP - HEAD_BOSS_DROP
    cuts, fills, voids, holes = [], [], [], []
    for hx, hy, side in HEAD_BOSSES:
        x0, x1 = (6.7, 20.0) if side < 0 else (94.0, 107.3)  # stops short of the cover wall's inner face
        cuts.append(Part.makeBox(x1 - x0, 13.0, 3.0, V(x0, hy - 6.5, top)))
        void = Part.makeBox(7.4, 10.2, 4.6, V(hx - 3.7, hy - 3.7, 4.0)).cut(cov)  # old nut pocket and hole
        fills.append(void.common(Part.makeBox(x1 - x0, 10.25, top - 4.3, V(x0, hy - 6.25, 4.3))))
        moved = void.copy()
        moved.translate(V(0, 0, -HEAD_BOSS_DROP))
        voids.append(moved)
        holes.append(Part.makeCylinder(1.6, top - 0.3 + 0.01, V(hx, hy, 0.3)))
    out = cov.cut(Part.makeCompound(cuts)).fuse(Part.makeCompound(fills))
    out = out.cut(Part.makeCompound(voids + holes)).removeSplitter()
    out.translate(t.negative())
    return out


# Top cover halves. The two halves are joined by an M3 screw through a pair of flanges hanging under the seam; Kooba's
# flanges sit 27.5 mm either side of the centre line, and the one on the USB-C side lands on the servo shield's power
# terminal block. Both flanges move to a symmetric pair 15 mm apart, between the shield's bent-over capacitor and the
# far side; each keeps 2.75 mm from the servo headers. The rear half also loses its OLED window (with its counterbore,
# pin recess and four pilot holes), the square opening for Kooba's balance-plug holder and the two rounded slits, filled
# flush with its 2 mm top skin.
# name: ((old flange centres), (new flange centres), seam-end band along Z), along the body's X (its width).
SEAM_FLANGES = {
    "Top_Cover_Split_Front": ((82.5, 137.5), (112.5, 127.5), (-106.7, -101.0)),
    "Top_Cover_Split_Rear": ((27.5, -27.5), (-2.5, -17.5), (111.0, 116.7)),
}
TOP_SKIN = (120.0, 122.0)  # Y range of the top skin in both bodies
REAR_FILLS = [((-30.0, 126.7), (30.0, 29.1)), ((5.5, 141.3), (18.0, 14.0)), ((26.2, 142.3), (10.0, 12.0))]  # (x, z), (w, d)
OLED_PILOTS = [(-3.25, 129.35), (-3.25, 153.15), (-26.75, 129.35), (-26.75, 153.15)]


def mod_top_cover(shape, name):
    import Part
    V = FreeCAD.Vector
    olds, news, (z0, z1) = SEAM_FLANGES[name]
    boxes = [Part.makeBox(7.2, TOP_SKIN[0] - 80, z1 - z0, V(x - 3.6, 80, z0)) for x in olds]
    flange = shape.common(boxes[0])
    out = shape.cut(Part.makeCompound(boxes))
    for x in news:
        f = flange.copy()
        f.translate(V(x - olds[0], 0, 0))
        out = out.fuse(f)
    if name == "Top_Cover_Split_Rear":
        skin = TOP_SKIN[1] - TOP_SKIN[0]
        fills = [Part.makeBox(w, skin, dz, V(x, TOP_SKIN[0], z)) for (x, z), (w, dz) in REAR_FILLS]
        fills += [Part.makeCylinder(1.2, skin + 0.6, V(x, TOP_SKIN[0] - 0.6, z), V(0, 1, 0)) for x, z in OLED_PILOTS]
        out = out.fuse(fills)
    return out.removeSplitter()


# LiPo bay for the 3S pack (126 x 43 x 31.2 mm measured). Kooba's three brackets were drawn for a 2S pack: their bay is
# 25.5 mm tall, their end walls box in leads that leave a 3S pack's end at its corners, and the rear one's balance-plug
# holder is too small for a 3S plug. They are replaced by two battery rails (BATTERY_RAIL), one each side of the pack,
# screwed up into blind pilot holes in the plate's underside (Battery_Rail_Pilots in cad/UnoQ_Mountingplate.FCStd), so
# no nuts sit on top of the plate. Two 20 mm hook-and-loop straps run across the pack's width, through slots in the
# rails, and hold it up against the plate. The bottom cover's floor drops BAY_DROP so the pack and the straps under it
# fit (28 -> 34 mm below the plate).
BAY_DROP = 6.0
# Bottom covers: stretched across the side walls at this Y of Kooba's body (floor at Y -38, open edge at Y -80). The
# rear half's top edge ramps down to about Y -68, so the plane is below that: there the front half's walls are exactly
# straight (its sections at Y -68..-65.4 are identical) and the rear half's within about 1 degree, with no edges within
# a millimetre, so the stretch only lengthens straight wall.
BOTTOM_STRETCH_Y = -66.4
# Battery rail, in the plate's frame on the pack's right (+X; the left one is the same part turned 180 degrees about Z),
# hanging down from the plate's underside at Z 0. A flange outside the pack's width carries three M3x8, which end
# 0.4 mm short of the end of the plate's 3.9 mm pilot holes; a side wall 2 mm from the pack locates it sideways and has
# a slot for each strap.
BATTERY_RAIL = {
    "length": (-49.0, 49.0),           # Y
    "flange": (23.5, 35.0, 4.5),       # X range, thickness
    "holes": (31.0, (-45.0, 0.0, 45.0), 3.4),  # X, Ys (the plate's pilot holes), clearance diameter
    "wall": (23.5, 26.0, 16.0),        # X range (the pack's side is at X 21.5), depth below the plate
    "slots": ((-35.0, 35.0), 22.0, (6.5, 10.0)),  # strap centres in Y, slot length for a 20 mm strap, Z below the plate
}


def build_battery_rail():
    """The right-hand rail in the plate frame (see BATTERY_RAIL)."""
    import Part
    V = FreeCAD.Vector
    r = BATTERY_RAIL
    y0, y1 = r["length"]
    fx0, fx1, ft = r["flange"]
    wx0, wx1, wd = r["wall"]
    out = Part.makeBox(fx1 - fx0, y1 - y0, ft, V(fx0, y0, -ft)).fuse(Part.makeBox(wx1 - wx0, y1 - y0, wd, V(wx0, y0, -wd)))
    hx, hys, hd = r["holes"]
    out = out.cut(Part.makeCompound([Part.makeCylinder(hd / 2, ft + 2, V(hx, y, -ft - 1)) for y in hys]))
    ys, sl, (sz0, sz1) = r["slots"]
    out = out.cut(Part.makeCompound([Part.makeBox(wx1 - wx0 + 2, sl, sz1 - sz0, V(wx0 - 1, y - sl / 2, -sz1)) for y in ys]))
    return out.removeSplitter()


def export_battery_rail(dest, step_dest):
    shape = build_battery_rail()
    if len(shape.Solids) != 1 or not shape.isValid():
        raise RuntimeError("battery rail is not one valid solid")
    shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 180)   # plate face on the bed, wall up
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False)
    b = mesh.BoundBox
    move = FreeCAD.Vector(-(b.XMin + b.XMax) / 2, -(b.YMin + b.YMax) / 2, -b.ZMin)
    mesh.translate(move.x, move.y, move.z)
    mesh.write(dest)
    shape.translate(move)
    os.makedirs(os.path.dirname(step_dest), exist_ok=True)
    shape.exportStep(step_dest)


def stretch_solid(shape, axis, at, extra):
    """Cut the solid across `axis` at `at`, move the part beyond it out by `extra` and fill the gap with the
    cross-section. Only valid where nothing but straight walls cross the plane."""
    import Part
    V = FreeCAD.Vector
    k = "xyz".index(axis)
    d = V(*[1 if i == k else 0 for i in range(3)])
    big = 2000.0
    corner = [-big / 2] * 3
    corner[k] = at - big
    lo = Part.makeBox(big, big, big, V(*corner))      # everything below `at` along the axis
    hi = lo.copy()
    hi.translate(d * big)
    low, high = shape.common(lo), shape.common(hi)
    high.translate(d * extra)
    face = Part.Face(shape.slice(d, at), "Part::FaceMakerBullseye")
    out = low.fuse([high, face.extrude(d * extra)]).removeSplitter()
    expected = face.Area * extra
    if abs(out.Volume - shape.Volume - expected) > 0.01 * expected + 1:
        raise RuntimeError(f"stretch added {out.Volume - shape.Volume:.1f} mm3, expected {expected:.1f}")
    return out


def mod_bottom_cover(shape):
    # floor is on the +Y side of the plane: moving it out lowers the floor
    return stretch_solid(shape, "y", BOTTOM_STRETCH_Y, BAY_DROP)


# output name: (Kooba FreeCAD file, body label, modifier, expected volume change in mm3)
KOOBA_MODS = {
    "Bottom_Cover_Split_Front": ("Bottom_Cover_Split_Front.FCStd", "Bottom_Cover_Split_Front", mod_bottom_cover, 1228),
    "Bottom_Cover_Split_Rear": ("Bottom_Cover_Split_Rear.FCStd", "Bottom_Cover_Split_Rear", mod_bottom_cover, 2580),
    "Front_Cover_Optimized": ("Front_Cover_Optimized.FCStd", "Front_Cover_Optimized", mod_front_cover, -1003),
    "Top_Cover_Split_Front": ("Top_Cover_Split_Front.FCStd", "Top_Cover_Split_Front", lambda s: mod_top_cover(s, "Top_Cover_Split_Front"), 0),
    "Top_Cover_Split_Rear": ("Top_Cover_Split_Rear_with_OLED.FCStd", "Top_Cover_Split_Rear_with_OLED", lambda s: mod_top_cover(s, "Top_Cover_Split_Rear"), 1382),
}


def export_kooba_mod(dest, name, step_dest):
    fcstd, label, mod, change = KOOBA_MODS[name]
    doc = FreeCAD.openDocument(os.path.join(REF, KOOBA, fcstd), hidden=True)
    body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body" and o.Label == label][0]
    src = body.Shape.copy()
    # the brackets sit in an App::Part that turns them into Kooba's print position
    parent = [p for p in body.InList if p.TypeId == "App::Part"]
    print_pl = parent[0].Placement if parent else FreeCAD.Placement()
    FreeCAD.closeDocument(doc.Name)
    shape = mod(src)
    shape.Placement = print_pl.multiply(shape.Placement)
    print(f"{name}: volume change {shape.Volume - src.Volume:.1f} mm3")
    if len(shape.Solids) != 1 or not shape.isValid() or (change is not None and abs(shape.Volume - src.Volume - change) > 15):
        raise RuntimeError(f"{name}: modified cover has {len(shape.Solids)} solids, valid {shape.isValid()}, "
                           f"volume change {shape.Volume - src.Volume:.0f} mm3 (expected {change})")
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False)
    b = mesh.BoundBox  # the mesh's box: a B-rep box can be loose
    move = FreeCAD.Vector(-(b.XMin + b.XMax) / 2, -(b.YMin + b.YMax) / 2, -b.ZMin)
    mesh.translate(move.x, move.y, move.z)
    mesh.write(dest)
    shape.translate(move)
    os.makedirs(os.path.dirname(step_dest), exist_ok=True)
    shape.exportStep(step_dest)


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
        elif src in (CARRIER_TEST, SZBK07_TEST, IMU_TEST):
            export_mount_test(dest, src)
        elif src == BATTERY_RAIL_SRC:
            export_battery_rail(dest, os.path.join(ROOT, "step", folder, name + ".step"))
        elif src == KOOBA_MOD:
            export_kooba_mod(dest, name, os.path.join(ROOT, "step", folder, name + ".step"))
        else:
            Mesh.Mesh(os.path.join(REF, src)).write(dest)  # rewrite as binary STL
        to_print_position(dest, name)
        if name in M2_PIN_SEATS:  # before mirroring, so the mirrored copy gets it too
            rebore_m2(dest, name)
        if name in LENGTHEN:
            lengthen(dest, name)
        files = [f"{folder}/{name}.stl"]
        if m:
            mirrored(dest, os.path.join(d, name + "_mirrored.stl"))
            files.append(f"{folder}/{name}_mirrored.stl")
        if name in LABELS:  # after mirroring, so the mirrored copy gets its own readable text
            x, y, z, face, rot, box, text, text_m = LABELS[name]
            engrave(dest, x, y, z, face, rot, box, text)
            engrave(os.path.join(d, name + "_mirrored.stl"), *mirror_spot(x, y, z, face, rot), box, text_m)
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
        "`_mirrored` files are the mirrored copies of parts that come in pairs: normal files for the left legs, `_mirrored` for the right legs (the shoulder servo mount takes one of each per side).",
        "Each of those pairs has its side engraved 0.6 mm deep on a face that ends up hidden: L or R, and FL RR or FR RL on the shoulder servo mount.",
        "Every part is in its print orientation, centred, with its lowest point at Z = 0.",
        "",
        "Sources and licenses: Kooba's SpotMicroESP32 and robjk's reinforced shoulders (CC BY, Thingiverse",
        "thing:4559827 and thing:4937631), the helper stand from Leika (stefi01, CC BY 4.0; Nova-SM2, MIT), and",
        "`electronics/UnoQ_Mountingplate.stl` and `head/Sensormount_DualCam.stl` (this project, modified from Kooba,",
        "CC BY-SA 4.0). `head/Front_Cover_Optimized.stl` and the two top cover halves are Kooba's, changed for this build",
        "as noted below. See ../NOTICE.md.",
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
