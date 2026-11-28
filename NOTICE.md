# Third-party work and attribution

This project builds on the following work. Each keeps its own license.

| Work | Author | License | Used here |
| ---- | ------ | ------- | --------- |
| [Spotmicro - robot dog](https://www.thingiverse.com/thing:3445283) | Deok-yeon Kim (KDY0523) | CC BY | The original design every Spot Micro derives from |
| [SpotMicroESP32 (prints without supports)](https://www.thingiverse.com/thing:4559827) | Michael Kubina (Kooba) | CC BY | `cad/UnoQ_Mountingplate.FCStd` is a modified copy of `Circuitry_Mountingplate_SZBK07.FCStd`, and `cad/Sensormount_DualCam.FCStd` is a modified copy of `sensormount_esp32_cam.FCStd`. Its STLs are redistributed in `stl/`, re-saved as binary STL, with a generated mirrored copy (`_mirrored.stl`) of left-hand parts; the parts changed for this build are listed in `stl/README.md` and below. STEP versions in `step/` are exported from Kooba's FreeCAD files, placed to match the STLs. |
| [SpotMicroESP32 repository](https://github.com/michaelkubina/SpotMicroESP32) | Michael Kubina | GPL-3.0 | `cad/SpotUnoQ.FCStd` links to the full assembly `spotmicroesp32_assembled_quick_and_dirty.FCStd`. It is fetched by `scripts/fetch-references.sh`, not redistributed. |
| [SpotMicroESP32-Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika) | Rune Harlyk | MIT | Kinematic dimensions, electronics list, helper stand selection, and the firmware this project will port |
| [Reinforced shoulder remix](https://www.thingiverse.com/thing:4937631) | robjk | CC BY 4.0 | Reinforced shoulder parts, upper-leg shell and medium rear cover, redistributed in `stl/` (mirrored copies generated as above), with STEP versions of the parts robjk published as FreeCAD files in `step/`. The shoulder parts are also embedded in `cad/SpotUnoQ.FCStd`, taken from robjk's `Limb_Top_Shell_mod.FCStd` and STL. |
| [stronger microspot stand top](https://www.thingiverse.com/thing:4814187) | stefi01 | CC BY 4.0 | Helper stand top, redistributed in `stl/optional/helper-stand/` |
| [Nova-SM2 stand parts](https://github.com/cguweb-com/Arduino-Projects/tree/main/Nova-SM2/STL%20Files) | cguweb | MIT | Helper stand bottom, brace and feet, redistributed in `stl/optional/helper-stand/` with its license text |
| [Arduino UNO Q STEP model](https://docs.arduino.cc/hardware/uno-q/) | Arduino | See Arduino's documentation | Board model, fetched and converted by the scripts, not redistributed |
| [Arduino UNO Media Carrier STEP model](https://docs.arduino.cc/hardware/uno-media-carrier/) | Arduino | See Arduino's documentation | Board model, fetched and converted by the scripts, not redistributed |

## Changes to Kooba's mounting plate

In `cad/UnoQ_Mountingplate.FCStd`:

- Removed: ESP32 TTL pins, ESP32-SOC pocket and antenna pocket, header-board pins, LM2596 pins, HW-482 relay pins,
  PCA9685 pins, the power-cable cap and cable hollow, and the original SZBK07 pins and screw-hole deepening.
- Removed: the LiPo bracket screw holes and nut pockets (filled by `Kooba_LiPo_Holes_Fill`).
- Removed: the balance-charger cable tunnel and its slot, and the USB-ports fin (`Kooba_Tunnel_And_USB_Fin_Removal`,
  `Kooba_Tunnel_Slot_Fill`).
- Added: a `Params` spreadsheet; six blind pilot holes in the underside for the battery rails (`Battery_Rail_Pilots`); four Media Carrier support pads, two fixed hooks and two snap clips; four SZBK07 posts
  with M3 pilot holes.
- Fixed: a redundant constraint in `Sketch677`, and the edge fillet next to the removed cap now references only the
  edges that remain.

## Changes to Kooba's sensor mount

In `cad/Sensormount_DualCam.FCStd` (from `sensormount_esp32_cam.FCStd`):

- Removed: the four HC-SR04 transducer holes, the two crystal pockets, the ESP32-CAM lens and flash openings, and the
  ESP32-CAM board slot on the back (suppressed; it printed as a sagging overhang).
- Added: a `Params` spreadsheet, and for each of two Raspberry Pi Camera Module 2s a component recess, four M2 pilot
  holes and a flared lens window. The recess ceiling is stepped (`Cam_Bridge_Step`) so it prints face down as two
  layers of anchored bridges, with no supports.

## Changes to Kooba's covers

Made by `scripts/export_stls.py` (`KOOBA_MODS`) from Kooba's FreeCAD files:

- `Front_Cover_Optimized`: the four sensor screw bosses are 2.27 mm lower, with their nut pockets and screw holes
  moved down with them, so the M3 screws clamp the camera mount's ears.
- `Top_Cover_Split_Front` and `Top_Cover_Split_Rear` (from `Top_Cover_Split_Rear_with_OLED`): the seam flanges move
  from 27.5 mm either side of the centre line to a pair 15 mm apart, clear of the servo shield's terminal block. The
  rear half's OLED window, square opening and two slits are filled.
- `Bottom_Cover_Split_Front` and `Bottom_Cover_Split_Rear`: the side walls are 6 mm taller, so the floor sits 6 mm
  lower and a 3S pack fits.
- Kooba's three `LiPo_Mountingbracket` parts aren't used: `stl/chassis/Battery_Rail.stl` (this project) holds the pack
  with two straps instead.

In `cad/Sensormount_DualCam.FCStd`, four screw ears (`Cover_Ears`, `Cover_Ear_Roots`) are added for those screws.
