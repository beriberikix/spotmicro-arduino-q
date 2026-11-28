# -*- coding: utf-8 -*-
"""Step definitions for the assembly-guide renders (see scripts/render_guide.FCMacro).

Each step lists:
  context  - parts already in place (drawn in their normal colours)
  new      - parts added in this step (drawn orange in the still, and flying in in the animation)
  explode  - list of (selector, (dx, dy, dz)) giving how far each new part starts from its place
  view     - camera direction (from the camera towards the model), global frame:
             +X towards the head, +Y to the robot's left, +Z up
Selectors are object names, labels, or "re:<regex on label>".
The legs are shown for the front-left leg; the others are the same or mirrored.
"""
import math

import FreeCAD

# ---------------------------------------------------------------- front-left leg, by object name
FOOT = ["LL_Body055"]
FOOT_HW = ["LL_Body003", "LL_Body008", "LL_Body009", "LL_Body010"]
WRIST = ["LL_Body054"]
WRIST_CP = ["LL_Body011"]
KNEE_SERVO = ["LL_Body058", "LL_Body056", "LL_Body059", "LL_Body053", "LL_Body057"]
KNEE_SERVO_DAMP = ["LL_Body287", "LL_Body288", "LL_Body289", "LL_Body290"]
KNEE_SERVO_SCREWS = ["LL_Body021", "LL_Body022", "LL_Body020", "LL_Body005"]
KNEE_SERVO_NUTS = ["LL_Body015", "LL_Body016", "LL_Body017", "LL_Body018"]
KNEE_PIN = ["LL_Body013", "LL_Body052", "LL_Body012"]
KNEE_BEARING = ["LL_Body062", "LL_Body064", "LL_Body063"]
KNEE_HORN = ["LL_Body042"]
KNEE_HORN_SCREWS = ["LL_Body038", "LL_Body046", "LL_Body048", "LL_Body040", "LL_Body043", "LL_Body050"]
KNEE_HORN_NUTS = ["LL_Body037", "LL_Body045", "LL_Body047", "LL_Body039", "LL_Body044", "LL_Body049"]
KNEE_HORN_CENTRE = ["LL_Body086"]
HORN_PLATE = ["LL_Body041"]           # Limb_Servohorn_Mount_long (inner side)
BEARING_PLATE = ["LL_Body051"]        # Limb_Ball_Bearing_Mount_long (outer side)
KNEE_PLATE_SCREWS = ["LL_Body078", "LL_Body079", "LL_Body084", "LL_Body085"]
KNEE_PLATE_NUTS = ["LL_Body065", "LL_Body066", "LL_Body067", "LL_Body068"]
UPPER_BOTTOM = ["LL_Body060"]         # Limb_Bottom_Shell (inner half)
UPPER_TOP = ["robjk_shell_FL"]        # robjk Limb_Top_Shell_with_BB_hole (outer half)
HIP_SERVO = ["LL_Body075", "LL_Body073", "LL_Body077", "LL_Body076", "LL_Body074"]
HIP_SERVO_DAMP = ["LL_Body291", "LL_Body292", "LL_Body293", "LL_Body294"]
HIP_SERVO_SCREWS = ["LL_Body080", "LL_Body081", "LL_Body082", "LL_Body083"]
HIP_SERVO_NUTS = ["LL_Body069", "LL_Body070", "LL_Body071", "LL_Body072"]
HIP_HORN = ["LL_Body150"]
HIP_HORN_SCREWS = ["LL_Body151", "LL_Body146", "LL_Body147", "LL_Body141", "LL_Body138", "LL_Body139"]
HIP_HORN_NUTS = ["LL_Body142", "LL_Body148", "LL_Body145", "LL_Body152", "LL_Body149", "LL_Body140"]
CAP = ["robjk_cap_FL"]
COVER = ["robjk_cover_FL"]
SHOULDER_MOUNT = ["robjk_servomount_FL"]
SH_SERVO = ["LL_Body154", "LL_Body158", "LL_Body157", "LL_Body155", "LL_Body156"]
SH_SERVO_DAMP = ["LL_Body283", "LL_Body284", "LL_Body285", "LL_Body286"]
SH_SERVO_SCREWS = ["LL_Body163", "LL_Body164", "LL_Body165", "LL_Body166"]
SH_SERVO_NUTS = ["LL_Body159", "LL_Body160", "LL_Body161", "LL_Body162"]
CAP_SCREWS = ["LL_Body131", "LL_Body132", "LL_Body133", "LL_Body135"]
CAP_NUTS = ["LL_Body130", "LL_Body134", "LL_Body136", "LL_Body137"]
SH_PIN = ["LL_Body143", "LL_Body144", "LL_Body129"]
SH_BEARING = ["LL_Body685", "LL_Body687", "LL_Body686"]
SH_HORN = ["LL_Body572"]
SH_HORN_SCREWS = ["LL_Body573", "LL_Body574", "LL_Body577", "LL_Body580", "LL_Body582", "LL_Body584"]
SH_HORN_NUTS = ["LL_Body575", "LL_Body576", "LL_Body578", "LL_Body579", "LL_Body581", "LL_Body583"]
SH_HORN_CENTRE = ["LL_Body625"]

LOWER_LEG = FOOT + FOOT_HW + WRIST + WRIST_CP + KNEE_SERVO + KNEE_SERVO_DAMP + KNEE_SERVO_SCREWS + KNEE_SERVO_NUTS
UPPER_LEG = UPPER_BOTTOM + UPPER_TOP + HIP_SERVO + HIP_SERVO_DAMP + HIP_SERVO_SCREWS + HIP_SERVO_NUTS
KNEE = (KNEE_PIN + KNEE_BEARING + KNEE_HORN + KNEE_HORN_SCREWS + KNEE_HORN_NUTS + KNEE_HORN_CENTRE + HORN_PLATE
        + BEARING_PLATE + KNEE_PLATE_SCREWS + KNEE_PLATE_NUTS)
SHOULDER = SHOULDER_MOUNT + SH_SERVO + SH_SERVO_DAMP + SH_SERVO_SCREWS + SH_SERVO_NUTS + SH_PIN
HIP = HIP_HORN + HIP_HORN_SCREWS + HIP_HORN_NUTS + CAP + CAP_SCREWS + CAP_NUTS
LEG_ALL = LOWER_LEG + UPPER_LEG + KNEE + SHOULDER + HIP + COVER

# ---------------------------------------------------------------- selections made at render time
def sel(**kw):
    """Selector evaluated against the scene: guide_render_lib.Scene.select(**kw)."""
    return lambda S: S.select(**kw)


FRONT = (-130, None)
REAR = (None, -130)
LEFT = (-100, None)
RIGHT = (None, -100)
SH_BEARINGS_ALL = "re:^L_Body(685|686|687|688|689|690|679|680|681|682|683|684)$"


def legs(xr, yr=None):
    """Whole legs (with shoulder joints, without the chassis plates or shoulder bearings) in an x range."""
    return sel(groups=["front_legs", "rear_legs", "robjk"], box=(xr, yr, None),
               exclude=r"^L_Outer_Shoulder|^L_Body(6[89]\d|69[0-9]|70[0-2]|679|68[0-4])$|FOS Servohorn|Futuba FSH6B01[0-3]"
                       r"|^L_M2(x08[1-9]|x09[0-9]|x1\d\d)|^L_M2 Nut(07\d|08\d|09\d)")


def outer_shoulder(xr):
    """Outer shoulder plate with its two horns, horn screws and nuts."""
    return sel(groups=["front_legs", "rear_legs"], box=(xr, None, None),
               labels=r"^L_Outer_Shoulder|Futuba FSH6B01[0-3]|^L_M2(x08[1-9]|x09\d|x1\d\d)|^L_M2 Nut(07\d|08\d|09\d)")


# The inner shoulders and their blocks are linked sub-assemblies in the model (moved only as a whole), so for the whole
# run proxies stand in for their pieces (setup() below), labelled "Front_Inner ..." / "Rear_Inner ...".
INNER = sel(labels=r"^(Front|Rear)_Inner ")
# The CAD's two blocks are square-edged; the printed ones (stl/chassis/Top_Shoulder, Bottom_Shoulder) have R7 rounds
# on the two long edges of the face away from the plate's middle, and are 2 mm longer (scripts/export_stls.py
# LENGTHEN), stretched at their middle. Everything outboard of the blocks' middles - the leg pairs, the head and rear
# covers and their screws and nuts - therefore sits 2 mm further out than in the model.
BLOCK_EXTRA = 2.0
BODY_MID_X = -108.0   # between the two inner shoulders
INNER_LINKS = {  # end: (link, {piece: sub-object path[, round]})
    "Front": ("L_Front_Inner_SHoulder_Assembly001", [
        ("Inner_Shoulder", "Body024."),
        ("Bottom_Shoulder", "Part009.Body025.", (7, "zmax")),
        ("M3 Nut bottom 1", "Part009.Body671."),
        ("M3 Nut bottom 2", "Part009.Body023."),
        ("Top_Shoulder", "Part007.Body028.", (7, "zmin")),
        ("M3 Nut top 1", "Part007.Body029."),
        ("M3 Nut top 2", "Part007.Body670."),
        ("M3x8 1", "Part008.Body030."),
        ("M3x8 2", "Part008.Body032."),
        ("M3x8 3", "Part008.Body031."),
        ("M3x8 4", "Part008.Body026."),
    ]),
    "Rear": ("L_Rear_Inner_SHoulder_Assembly", [
        ("Inner_Shoulder", "Body658."),
        ("Bottom_Shoulder", "Part267.Body659.", (7, "zmax")),
        ("M3 Nut bottom 1", "Part267.Body656."),
        ("M3 Nut bottom 2", "Part267.Body657."),
        ("Top_Shoulder", "Part265.Body661.", (7, "zmin")),
        ("M3 Nut top 1", "Part265.Body019."),
        ("M3 Nut top 2", "Part265.Body660."),
        ("M3x8 1", "Part266.Body662."),
        ("M3x8 2", "Part266.Body669."),
        ("M3x8 3", "Part266.Body663."),
        ("M3x8 4", "Part266.Body014."),
    ]),
}
COVER_NUTS = ("L_Cover_Nuts", ["Part304.Body%d." % n for n in range(759, 767)]
              + ["Part305.Body%d." % n for n in range(767, 775)])
OUTBOARD_FRONT = r"^L_(Front_Cover|Front_Cover_Screws|Head_Cover_Screws)$"
OUTBOARD_REAR = r"^L_(Rear_Cover_Assembly|Rear_Cover_Screws001)$"


def add_carrier_clamps(S):
    """The four M3x8 screws and washers that clamp the Media Carrier's edges (not in the CAD assembly), on the
    plate's clamp posts. Labels: 'Clamp M3x8 n' and 'Clamp Washer n' (no 'Carrier', which would colour them as a PCB)."""
    import Part
    V = FreeCAD.Vector
    link = S.doc.getObject(PLATE[0])
    pdoc = link.LinkedObject.Document
    sk = pdoc.getObject("Carrier_Clamp_Posts_Sketch")
    P = pdoc.getObject("Params")
    z = 5 + P.Standoff_H + P.Carrier_T  # carrier top, plate frame
    pl = link.Placement
    for i, g in enumerate(sk.Geometry):
        x, y = g.Center.x, g.Center.y
        washer = Part.makeCylinder(3.5, 0.5, V(x, y, z)).cut(Part.makeCylinder(1.6, 0.5, V(x, y, z)))
        head = Part.makeCylinder(2.75, 3.0, V(x, y, z + 0.5))
        sock = Part.makePolygon([V(x + 1.44 * math.cos(math.radians(a)), y + 1.44 * math.sin(math.radians(a)),
                                   z + 2.0) for a in range(0, 361, 60)])
        head = head.cut(Part.Face(sock).extrude(V(0, 0, 1.6)))
        screw = head.fuse(Part.makeCylinder(1.5, 8.0, V(x, y, z + 0.5 - 8.0))).removeSplitter()
        for shp in (washer, screw):
            shp.transformShape(pl.toMatrix())
        S.add_shape(f"Clamp Washer {i + 1}", washer, keep=True)
        S.add_shape(f"Clamp M3x8 {i + 1}", screw, keep=True)


def setup(S):
    """Make the scene match the printed parts (see BLOCK_EXTRA): proxies for the inner shoulders, with the blocks
    rounded and stretched, and the parts outboard of the blocks' middles moved out."""
    out = {}  # end -> (x of the blocks' middle, outward sign)
    for end, (link, pieces) in INNER_LINKS.items():
        lk = S.doc.getObject(link)
        blk = lk.getSubObject(pieces[1][1]).BoundBox
        mid = (blk.XMin + blk.XMax) / 2
        sign = 1 if mid > BODY_MID_X else -1
        out[end] = (mid, sign)
        for piece in pieces:
            name, sub = piece[0], piece[1]
            rounds = piece[2] if len(piece) > 2 else None
            stretch = (mid, sign * BLOCK_EXTRA) if name.endswith("_Shoulder") and name != "Inner_Shoulder" else None
            S.add_proxy(f"{end}_Inner {name}", link, sub, rounds=rounds, stretch=stretch, keep=True)
    add_carrier_clamps(S)
    nuts = []
    for i, sub in enumerate(COVER_NUTS[1]):
        nuts.append(S.add_proxy(f"Cover M3 Nut {i + 1}", COVER_NUTS[0], sub, keep=True))
    for o in nuts:
        o.Visibility = False

    def outboard(o):
        x = S.centre.get(o.Name, (None,))[0]
        if x is None:
            return 0
        mid, sign = out["Front"] if x > BODY_MID_X else out["Rear"]
        return sign if (x - mid) * sign > 0 else 0

    front = {o.Name for o in S.select(groups=["head"]) + S.select(labels=OUTBOARD_FRONT)}
    rear = {o.Name for o in S.select(labels=OUTBOARD_REAR)}
    for o in S.select(groups=["front_legs", "rear_legs", "robjk", "head"]) + S.select(labels=OUTBOARD_REAR) + nuts:
        if o.Name in front:
            sign = 1
        elif o.Name in rear:
            sign = -1
        elif o in nuts:
            sign = outboard(o)
        elif o.Name in S.centre:  # legs and shoulder joints: by which end they are at (empty links have no centre)
            sign = 1 if S.centre[o.Name][0] > BODY_MID_X else -1
        else:
            sign = 0
        if sign:
            S.shift([o], (sign * BLOCK_EXTRA, 0, 0))


CHASSIS_SIDES = sel(labels=r"^L_Chassis_Side|Right_Side_Nuts")
CHASSIS_SCREWS = sel(labels=r"^L_Part01[01]$")
PLATE = ["UnoQ_Mountingplate"]
SH_BEARINGS = sel(groups=["front_legs", "rear_legs"], labels=r"^L_Body(68[0-9]|69[0])$|^L_Body679$")
SH_BEARINGS_FRONT = sel(groups=["front_legs", "rear_legs"], labels=r"^L_Body(68[5-9]|690)$")  # 625ZZ on the front pins
SH_BEARINGS_REAR = sel(groups=["front_legs", "rear_legs"], labels=r"^L_Body(679|68[0-4])$")
FRONT_HORN_SCREWS = sel(labels="FOS Servohorn", box=(FRONT, None, None))  # M3x8 into the front shoulder servo shafts
# The front pair's shoulder joints only (servo mounts, caps, servos, pins), without the rest of the legs
SHOULDERS_FRONT = sel(groups=["front_legs", "rear_legs", "robjk"], box=(FRONT, None, (190, None)),
                      exclude=r"^L_Outer_Shoulder|^L_Body(6[89]\d|69[0-9]|70[0-2]|679|68[0-4])$|FOS Servohorn"
                              r"|Futuba FSH6B01[0-3]|^L_M2(x08[1-9]|x09[0-9]|x1\d\d)|^L_M2 Nut(07\d|08\d|09\d)")
OUTER_SCREWS = sel(labels=r"^L_(M3x13[5-8]|M3 Nut1(1[7-9]|20))$")
CARRIER = ["Arduino_UNO_Media_Carrier"]
CLAMP_WASHERS = sel(labels=r"^Clamp Washer")
CLAMP_SCREWS = sel(labels=r"^Clamp M3x8")
CLAMPS = [CLAMP_WASHERS, CLAMP_SCREWS]
UNOQ = ["Arduino_UNO_Q"]
SHIELD = ["Adafruit_1411"]
BUCK = ["SZBK07"]
FPC = ["FPC_left", "FPC_right"]
HEAD = ["L_Front_Cover", "L_Front_Cover_Screws", "Sensormount_DualCam"]
CAMS = ["Camera_Module_2_left", "Camera_Module_2_right"]
BATTERY_RAILS = ["Battery_Rail_Right", "Battery_Rail_Left"]
LIPO = ["LiPo_3S_placeholder"]
BOTTOM_COVER = ["Bottom_Cover_3S"]   # floor 5 mm lower than Kooba's, for a 3S pack
TOP_COVER = ["L_Top_Cover_Assembly"]
REAR_COVER = ["L_Rear_Cover_Assembly", "L_Rear_Cover_Screws001"]
COVER_HW = [sel(labels=r"^Cover M3 Nut "), "L_Head_Cover_Screws"]

BODY = [INNER, CHASSIS_SIDES, CHASSIS_SCREWS] + PLATE
ALL_LEGS = [legs(None)]

# view directions (camera -> model)
# Assembly poses. The CAD model stands the robot up; these rotate a leg's parts about a joint axis (front left leg,
# both axes along Y) to the pose the guide assembles them in.
# setup() moves the front legs out by BLOCK_EXTRA, so the axes move with them.
KNEE_AXIS = ((-82.52 + BLOCK_EXTRA, 0, 121.01), (0, 1, 0))
HIP_AXIS = ((-4.95 + BLOCK_EXTRA, 0, 200.35), (0, 1, 0))
# Knee folded flat (servo at its assembly angle): the lower leg turned 74 degrees from standing, 0.6 mm clear of the
# upper leg shells (they touch at 75).
FOLD_KNEE = [(LOWER_LEG + KNEE_PIN, *KNEE_AXIS, -74)]
# Upper leg hanging straight down from the shoulder joint, as the hip is fitted: 60 degrees, one horn arm, from standing.
HIP_DOWN = [(LOWER_LEG + KNEE_PIN + UPPER_LEG + [k for k in KNEE if k not in KNEE_PIN], *HIP_AXIS, -60)]

OUTSIDE = (-0.55, -1.0, -0.45)   # from the robot's left, slightly front and above
INSIDE = (-0.55, 1.0, -0.45)     # from the centre line, looking out at the leg
ISO_FRONT = (-1.0, -0.75, -0.6)  # body: from front-left, above
ISO_REAR = (1.0, -0.75, -0.6)

STEPS = [
    # ---------------------------------------------------------------- lower leg
    dict(id="leg-foot", context=WRIST, new=FOOT + FOOT_HW,
         explode=[(FOOT, (0, 0, -40)), (["LL_Body009", "LL_Body003"], (0, -30, 0)),
                  (["LL_Body010", "LL_Body008"], (0, 30, 0))],
         view=(-0.6, -1.0, -0.3)),
    dict(id="leg-knee-pin", context=WRIST_CP, new=KNEE_PIN,
         explode=[(["LL_Body013"], (0, 25, 0)), (["LL_Body052"], (0, 45, 0)), (["LL_Body012"], (0, -25, 0))],
         view=(-0.5, 1.0, -0.35)),
    dict(id="leg-knee-servo", context=WRIST + FOOT + FOOT_HW,
         new=KNEE_SERVO + KNEE_SERVO_DAMP + WRIST_CP + KNEE_PIN + KNEE_SERVO_SCREWS + KNEE_SERVO_NUTS,
         explode=[(KNEE_SERVO + KNEE_SERVO_DAMP, (0, -45, 0)), (WRIST_CP + KNEE_PIN, (0, 70, 0)),
                  (KNEE_SERVO_SCREWS, (0, -95, 0)), (KNEE_SERVO_NUTS, (0, 100, 0))],
         view=(-0.5, -1.0, -0.35)),
    # ---------------------------------------------------------------- knee
    dict(id="knee-horn", context=[], new=HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS + KNEE_HORN_NUTS,
         explode=[(KNEE_HORN, (0, -20, 0)), (KNEE_HORN_NUTS, (0, -35, 0)), (KNEE_HORN_SCREWS, (0, -45, 0))],
         view=(-0.3, 1.0, -0.2)),
    dict(id="knee-horn-plate", context=LOWER_LEG + KNEE_PIN,
         new=HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS + KNEE_HORN_NUTS + KNEE_HORN_CENTRE,
         explode=[(HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS + KNEE_HORN_NUTS, (0, -40, 0)),
                  (KNEE_HORN_CENTRE, (0, -70, 0))],
         pose=FOLD_KNEE, view=INSIDE),
    dict(id="knee-bearing-plate", context=LOWER_LEG + KNEE_PIN + HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS
         + KNEE_HORN_NUTS + KNEE_HORN_CENTRE,
         new=BEARING_PLATE + KNEE_BEARING,
         explode=[(BEARING_PLATE, (0, 40, 0)), (KNEE_BEARING, (0, 70, 0))],
         pose=FOLD_KNEE, view=OUTSIDE),
    # ---------------------------------------------------------------- upper leg
    dict(id="upper-servo", context=[], new=UPPER_BOTTOM + HIP_SERVO + HIP_SERVO_DAMP + HIP_SERVO_NUTS,
         explode=[(HIP_SERVO + HIP_SERVO_DAMP, (0, 50, 0)), (HIP_SERVO_NUTS, (0, 25, 0))],
         view=(-0.4, 1.0, -0.6)),
    dict(id="upper-shells", context=UPPER_BOTTOM + HIP_SERVO + HIP_SERVO_DAMP + HIP_SERVO_NUTS,
         new=UPPER_TOP + HIP_SERVO_SCREWS,
         explode=[(UPPER_TOP, (0, 60, 0)), (HIP_SERVO_SCREWS, (0, -70, 0))],
         view=(-0.4, -1.0, -0.5)),
    dict(id="upper-to-knee", context=LOWER_LEG + KNEE_PIN + HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS + KNEE_HORN_NUTS
         + KNEE_HORN_CENTRE + BEARING_PLATE + KNEE_BEARING,
         new=UPPER_LEG + KNEE_PLATE_SCREWS + KNEE_PLATE_NUTS,
         explode=[(UPPER_LEG, (15, 0, 40)), (["LL_Body078", "LL_Body079"], (15, -40, 40)),
                  (["LL_Body084", "LL_Body085"], (15, 40, 40)), (KNEE_PLATE_NUTS, (15, 0, 40))],
         pose=FOLD_KNEE, view=INSIDE),
    # ---------------------------------------------------------------- shoulder joint
    dict(id="hip-horn-cap", context=[], new=CAP + HIP_HORN + HIP_HORN_SCREWS + HIP_HORN_NUTS,
         explode=[(HIP_HORN, (0, 20, 0)), (HIP_HORN_NUTS, (0, 35, 0)), (HIP_HORN_SCREWS, (0, 45, 0))],
         view=(-0.3, -1.0, -0.3)),
    dict(id="shoulder-pin", context=SHOULDER_MOUNT, new=SH_PIN,
         explode=[(["LL_Body143"], (-25, 0, 0)), (["LL_Body144"], (-45, 0, 0)), (["LL_Body129"], (20, 0, 0))],
         view=(-1.0, 0.7, -0.4)),
    dict(id="cap-to-mount", context=SHOULDER_MOUNT + SH_PIN,
         new=CAP + HIP_HORN + HIP_HORN_SCREWS + HIP_HORN_NUTS + CAP_SCREWS + CAP_NUTS,
         explode=[(CAP + HIP_HORN + HIP_HORN_SCREWS + HIP_HORN_NUTS, (0, 40, 0)), (CAP_SCREWS, (0, 70, 0)),
                  (CAP_NUTS, (0, -25, 0))],
         view=(-0.6, -1.0, -0.4)),
    dict(id="shoulder-to-leg", context=LOWER_LEG + UPPER_LEG + KNEE,
         new=SHOULDER_MOUNT + SH_PIN + HIP,
         explode=[(SHOULDER_MOUNT + SH_PIN + HIP, (0, -60, 0))],
         pose=FOLD_KNEE + HIP_DOWN, view=INSIDE),
    dict(id="shoulder-servo", context=LOWER_LEG + UPPER_LEG + KNEE + SHOULDER_MOUNT + SH_PIN + HIP,
         new=SH_SERVO + SH_SERVO_DAMP + SH_SERVO_SCREWS + SH_SERVO_NUTS,
         explode=[(SH_SERVO + SH_SERVO_DAMP, (0, 0, 70)), (SH_SERVO_SCREWS, (-60, 0, 0)), (SH_SERVO_NUTS, (40, 0, 0))],
         view=(-0.8, 1.0, -0.5)),
    dict(id="shoulder-cover", context=LOWER_LEG + UPPER_LEG + KNEE + SHOULDER + HIP,
         new=COVER, explode=[(COVER, (0, 0, 60))],
         view=OUTSIDE),
    # ---------------------------------------------------------------- body
    dict(id="outer-shoulder-horns", context=[], new=[outer_shoulder(FRONT)],
         explode=[(sel(labels=r"Futuba FSH6B01[01]"), (25, 0, 0)), (sel(labels=r"^L_M2 Nut(07\d|08[01])$"), (40, 0, 0)),
                  (sel(labels=r"^L_M2x(08[1-9]|09[0-2])$"), (55, 0, 0))],
         view=(-1.0, -0.5, -0.35)),
    dict(id="legs-to-outer", context=[outer_shoulder(FRONT)], new=[legs(FRONT), FRONT_HORN_SCREWS],
         explode=[(legs(FRONT, LEFT), (-60, 0, 0)), (legs(FRONT, RIGHT), (-60, 0, 0))],
         view=(0.9, -0.8, -0.5)),
    dict(id="shoulder-bearings", context=[outer_shoulder(FRONT), FRONT_HORN_SCREWS, SHOULDERS_FRONT],
         new=[SH_BEARINGS_FRONT], explode=[(SH_BEARINGS_FRONT, (-40, 0, 0))],
         view=(0.9, -0.7, -0.45)),
    dict(id="inner-shoulder", context=["Front_Inner Inner_Shoulder"],
         new=["Front_Inner " + p[0] for p in INNER_LINKS["Front"][1][1:]],
         explode=[(["Front_Inner Top_Shoulder", "Front_Inner Bottom_Shoulder"], (45, 0, 0)),
                  (["Front_Inner M3 Nut top 1", "Front_Inner M3 Nut top 2"], (45, 0, 25)),
                  (["Front_Inner M3 Nut bottom 1", "Front_Inner M3 Nut bottom 2"], (45, 0, 25)),
                  (["Front_Inner M3x8 %d" % i for i in range(1, 5)], (-30, 0, 0))],
         view=(0.55, -1.0, -0.55)),
    dict(id="frame", context=[], new=[INNER, CHASSIS_SIDES, CHASSIS_SCREWS] + PLATE,
         explode=[(sel(labels=r"^L_Chassis_Side$|Right_Side_Nuts$"), (0, 50, 0)),
                  (sel(labels=r"^L_Chassis_Side001$|Right_Side_Nuts001$"), (0, -50, 0)),
                  (sel(labels="^Front_Inner "), (60, 0, 0)), (sel(labels="^Rear_Inner "), (-60, 0, 0)),
                  (sel(labels=r"^L_Part011$"), (90, 0, 0)), (sel(labels=r"^L_Part010$"), (-90, 0, 0)),
                  (PLATE, (0, 0, 40))],
         view=ISO_FRONT),
    dict(id="install-shoulders", context=BODY,
         new=[legs(None), outer_shoulder(None), sel(labels="FOS Servohorn"), SH_BEARINGS, OUTER_SCREWS],
         explode=[(legs(FRONT), (90, 0, 0)), (outer_shoulder(FRONT), (90, 0, 0)), (FRONT_HORN_SCREWS, (90, 0, 0)),
                  (legs(REAR), (-90, 0, 0)), (outer_shoulder(REAR), (-90, 0, 0)),
                  (sel(labels="FOS Servohorn", box=(REAR, None, None)), (-90, 0, 0)),
                  (SH_BEARINGS_FRONT, (90, 0, 0)), (SH_BEARINGS_REAR, (-90, 0, 0)),
                  (OUTER_SCREWS, (130, 0, 0))],  # bearings stay on the pins, travelling with the legs
         view=ISO_FRONT),
    # ---------------------------------------------------------------- electronics
    dict(id="plate-boards", context=PLATE, new=CARRIER + CLAMPS + UNOQ + SHIELD + BUCK,
         explode=[(CARRIER, (0, 0, 30)), (CLAMPS, (0, 0, 42)), (UNOQ, (0, 0, 60)), (SHIELD, (0, 0, 95)),
                  (BUCK, (0, 0, 50))],
         view=(-0.8, -0.9, -1.0)),
    # step 3 close-ups: carrier onto its pads and clamps, then the UNO Q and the shield.
    dict(id="plate-carrier", context=PLATE, new=CARRIER + [CLAMP_WASHERS, CLAMP_SCREWS],
         explode=[(CARRIER, (0, 0, 25)), (CLAMP_WASHERS, (0, 0, 45)), (CLAMP_SCREWS, (0, 0, 65))],
         view=(-1.0, 0.2, -0.65), focus=CARRIER + CLAMPS),
    dict(id="plate-unoq", context=PLATE + CARRIER + CLAMPS, new=UNOQ,
         explode=[(UNOQ, (0, 0, 35))],
         view=(-0.75, 0.8, -1.0), focus=CARRIER + UNOQ),
    dict(id="plate-shield", context=PLATE + CARRIER + CLAMPS + UNOQ, new=SHIELD,
         explode=[(SHIELD, (0, 0, 35))],
         view=(-0.75, -0.9, -1.0), focus=CARRIER + SHIELD),
    # step 4: the cables go down first, flat along the plate, then the SZBK07 drops onto its posts over them
    dict(id="camera-cables", context=PLATE + CARRIER + CLAMPS + UNOQ + SHIELD + [INNER, CHASSIS_SIDES], new=FPC,
         explode=[(FPC, (0, 0, 25))],
         view=(-0.6, -0.5, -1.0), focus=PLATE + FPC),
    dict(id="plate-szbk07", context=PLATE + CARRIER + CLAMPS + UNOQ + SHIELD + FPC, new=BUCK,
         explode=[(BUCK, (0, 0, 45))],
         view=(-1.0, 0.35, -0.75), focus=BUCK + FPC),
    dict(id="head", context=[], new=HEAD + CAMS,
         explode=[(["L_Front_Cover"], (60, 0, 0)), (["L_Front_Cover_Screws"], (-60, 0, 0)), (CAMS, (-45, 0, 0))],
         view=(1.0, -0.8, -0.45)),
    # ---------------------------------------------------------------- covers
    # battery rails and the pack between them, under the plate, seen from below
    dict(id="battery", context=BODY + CARRIER + UNOQ + SHIELD + BUCK, new=BATTERY_RAILS + LIPO,
         explode=[(BATTERY_RAILS, (0, 0, -35)), (LIPO, (0, 0, -75))],
         view=(0.55, -0.6, 0.75), focus=PLATE + BATTERY_RAILS + LIPO),
    dict(id="covers", context=BODY + ALL_LEGS + [outer_shoulder(None), sel(labels="FOS Servohorn", box=(FRONT, None, None))] + CARRIER + UNOQ
         + SHIELD + BUCK + HEAD + CAMS + BATTERY_RAILS + LIPO,
         new=BOTTOM_COVER + TOP_COVER + REAR_COVER,
         explode=[(BOTTOM_COVER, (0, 0, -90)), (TOP_COVER, (0, 0, 110)), (REAR_COVER, (-90, 0, 0))],
         view=ISO_FRONT),
]
