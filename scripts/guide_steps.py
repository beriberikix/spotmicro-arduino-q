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


INNER = sel(labels=r"Inner_SHoulder_Assembly")
CHASSIS_SIDES = sel(labels=r"^L_Chassis_Side|Right_Side_Nuts")
CHASSIS_SCREWS = sel(labels=r"^L_Part01[01]$")
PLATE = ["UnoQ_Mountingplate"]
SH_BEARINGS = sel(groups=["front_legs", "rear_legs"], labels=r"^L_Body(68[0-9]|69[0])$|^L_Body679$")
OUTER_SCREWS = sel(labels=r"^L_(M3x13[5-8]|M3 Nut1(1[7-9]|20))$")
CARRIER = ["Arduino_UNO_Media_Carrier"]
UNOQ = ["Arduino_UNO_Q"]
SHIELD = ["Adafruit_1411"]
BUCK = ["SZBK07"]
FPC = ["FPC_left", "FPC_right"]
HEAD = ["L_Front_Cover", "L_Front_Cover_Screws", "Sensormount_DualCam"]
CAMS = ["Camera_Module_2_left", "Camera_Module_2_right"]
BOTTOM_COVER = ["L_Bottom_Cover_Assembly"]
TOP_COVER = ["L_Top_Cover_Assembly"]
REAR_COVER = ["L_Rear_Cover_Assembly", "L_Rear_Cover_Screws001"]
COVER_HW = ["L_Cover_Nuts", "L_Head_Cover_Screws"]

BODY = [INNER, CHASSIS_SIDES, CHASSIS_SCREWS] + PLATE
ALL_LEGS = [legs(None)]

# view directions (camera -> model)
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
         view=INSIDE),
    dict(id="knee-bearing-plate", context=LOWER_LEG + KNEE_PIN + HORN_PLATE + KNEE_HORN + KNEE_HORN_SCREWS
         + KNEE_HORN_NUTS + KNEE_HORN_CENTRE,
         new=BEARING_PLATE + KNEE_BEARING,
         explode=[(BEARING_PLATE, (0, 40, 0)), (KNEE_BEARING, (0, 70, 0))],
         view=OUTSIDE),
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
         view=INSIDE),
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
         view=INSIDE),
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
    dict(id="legs-to-outer", context=[outer_shoulder(FRONT)], new=[legs(FRONT), sel(labels="FOS Servohorn")],
         explode=[(legs(FRONT, LEFT), (-60, 0, 0)), (legs(FRONT, RIGHT), (-60, 0, 0))],
         view=(0.9, -0.8, -0.5)),
    dict(id="frame", context=[], new=[INNER, CHASSIS_SIDES, CHASSIS_SCREWS] + PLATE,
         explode=[(sel(labels=r"^L_Chassis_Side$|Right_Side_Nuts$"), (0, 50, 0)),
                  (sel(labels=r"^L_Chassis_Side001$|Right_Side_Nuts001$"), (0, -50, 0)),
                  (sel(labels="Front_Inner"), (60, 0, 0)), (sel(labels="Rear_Inner"), (-60, 0, 0)),
                  (sel(labels=r"^L_Part011$"), (90, 0, 0)), (sel(labels=r"^L_Part010$"), (-90, 0, 0)),
                  (PLATE, (0, 0, 40))],
         view=ISO_FRONT),
    dict(id="install-shoulders", context=BODY,
         new=[legs(None), outer_shoulder(None), sel(labels="FOS Servohorn"), SH_BEARINGS, OUTER_SCREWS],
         explode=[(legs(FRONT), (90, 0, 0)), (outer_shoulder(FRONT), (90, 0, 0)), (sel(labels="FOS Servohorn Left"), (90, 0, 0)),
                  (sel(labels="FOS Servohorn Right"), (90, 0, 0)),
                  (legs(REAR), (-90, 0, 0)), (outer_shoulder(REAR), (-90, 0, 0)),
                  (SH_BEARINGS, (0, 0, 0)), (OUTER_SCREWS, (130, 0, 0))],
         view=ISO_FRONT),
    # ---------------------------------------------------------------- electronics
    dict(id="plate-boards", context=PLATE, new=CARRIER + UNOQ + SHIELD + BUCK,
         explode=[(CARRIER, (0, 0, 30)), (UNOQ, (0, 0, 60)), (SHIELD, (0, 0, 95)), (BUCK, (0, 0, 50))],
         view=(-0.8, -0.9, -1.0)),
    dict(id="camera-cables", context=PLATE + CARRIER + UNOQ + SHIELD + BUCK + [INNER, CHASSIS_SIDES], new=FPC,
         explode=[(FPC, (0, 0, 60))],
         view=(-0.6, -0.5, -1.0), focus=PLATE + FPC),
    dict(id="head", context=[], new=HEAD + CAMS,
         explode=[(["L_Front_Cover"], (60, 0, 0)), (["L_Front_Cover_Screws"], (-60, 0, 0)), (CAMS, (-45, 0, 0))],
         view=(1.0, -0.8, -0.45)),
    # ---------------------------------------------------------------- covers
    dict(id="covers", context=BODY + ALL_LEGS + [outer_shoulder(None), sel(labels="FOS Servohorn")] + CARRIER + UNOQ
         + SHIELD + BUCK + HEAD + CAMS,
         new=BOTTOM_COVER + TOP_COVER + REAR_COVER,
         explode=[(BOTTOM_COVER, (0, 0, -90)), (TOP_COVER, (0, 0, 110)), (REAR_COVER, (-90, 0, 0))],
         view=ISO_FRONT),
]
