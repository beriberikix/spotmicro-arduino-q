# Third-party work and attribution

This project builds on the following work. Each keeps its own license.

| Work | Author | License | Used here |
| ---- | ------ | ------- | --------- |
| [Spotmicro - robot dog](https://www.thingiverse.com/thing:3445283) | Deok-yeon Kim (KDY0523) | CC BY | The original design every Spot Micro derives from |
| [SpotMicroESP32 (prints without supports)](https://www.thingiverse.com/thing:4559827) | Michael Kubina (Kooba) | CC BY | `cad/UnoQ_Mountingplate.FCStd` is a modified copy of `Circuitry_Mountingplate_SZBK07.FCStd`. Its STLs are redistributed unchanged in `stl/`, except that left-hand parts also get a generated mirrored copy (`_mirrored.stl`) and files are re-saved as binary STL. |
| [SpotMicroESP32 repository](https://github.com/michaelkubina/SpotMicroESP32) | Michael Kubina | GPL-3.0 | `cad/SpotUnoQ.FCStd` links to the full assembly `spotmicroesp32_assembled_quick_and_dirty.FCStd`. It is fetched by `scripts/fetch-references.sh`, not redistributed. |
| [SpotMicroESP32-Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika) | Rune Harlyk | MIT | Kinematic dimensions, electronics list, helper stand selection, and the firmware this project will port |
| [Reinforced shoulder remix](https://www.thingiverse.com/thing:4937631) | robjk | CC BY 4.0 | Reinforced shoulder parts, upper-leg shell and medium rear cover, redistributed in `stl/` (mirrored copies generated as above). The shoulder parts are also embedded in `cad/SpotUnoQ.FCStd`, taken from robjk's `Limb_Top_Shell_mod.FCStd` and STL. |
| [stronger microspot stand top](https://www.thingiverse.com/thing:4814187) | stefi01 | CC BY 4.0 | Helper stand top, redistributed in `stl/optional/helper-stand/` |
| [Nova-SM2 stand parts](https://github.com/cguweb-com/Arduino-Projects/tree/main/Nova-SM2/STL%20Files) | cguweb | MIT | Helper stand bottom, brace and feet, redistributed in `stl/optional/helper-stand/` with its license text |
| [Arduino UNO Q STEP model](https://docs.arduino.cc/hardware/uno-q/) | Arduino | See Arduino's documentation | Board model, fetched and converted by the scripts, not redistributed |

## Changes to Kooba's mounting plate

In `cad/UnoQ_Mountingplate.FCStd`:

- Removed: ESP32 TTL pins, ESP32-SOC pocket and antenna pocket, header-board pins, LM2596 pins, HW-482 relay pins,
  SZBK07 pins and screw-hole deepening.
- Added: a `Params` spreadsheet, four UNO Q standoffs with M3 pilot holes, and four Pololu D24V150F6 posts with
  M2 pilot holes.
- Fixed: a redundant constraint in `Sketch677`.
