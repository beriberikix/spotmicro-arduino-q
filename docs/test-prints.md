# Fit-test prints

Print these before the full robot. They take about 3 hours and 84 g of filament. They check every place where a
printed part has to fit something you bought: the Media Carrier, the servo regulator, the cameras, a servo and its
horn, and the 625ZZ bearings. If they fit, the other parts will too, since they share the same printer tolerances and
the same designs.

## Files

| File | What it is |
| ---- | ---------- |
| `makerworld/SpotUnoQ_P1S_test_prints.3mf` | Bambu Studio project, sliced for the P1S (0.4 mm nozzle, 0.20 mm Standard, Textured PEI plate). Not committed; build it with the command below. |
| [`stl/optional/test-prints/Carrier_Mount_Test.stl`](../stl/optional/test-prints/Carrier_Mount_Test.stl) | The electronics plate's Media Carrier pads, hooks and snap clips on a 2 mm frame |
| [`stl/optional/test-prints/SZBK07_Mount_Test.stl`](../stl/optional/test-prints/SZBK07_Mount_Test.stl) | The SZBK07 posts from the electronics plate on a 2 mm frame |
| [`stl/head/Sensormount_DualCam.stl`](../stl/head/Sensormount_DualCam.stl) | The real camera mount; it's small, so it serves as its own test |

Build the project:

```sh
python3 scripts/build_makerworld_3mf.py --no-orient --test-prints
```

`scripts/export_stls.py` cuts the two test frames from the electronics plate's real pads, clips and posts, using its
`Params` spreadsheet, so they always match the current plate. Re-run that script, then the build, after changing the
plate.

Print settings match the real parts: 3 walls, 20% infill, Bambu PLA Basic, no supports.

## Plates

| Plate | Filament | Parts | Time | Filament used |
| ----- | -------- | ----- | ---- | ------------- |
| 1 | Black PLA | Carrier_Mount_Test, SZBK07_Mount_Test, Sensormount_DualCam, Shoulder_Joint_Servomount_extended_BB, Shoulder_Joint_Servo_Cap_Extended, Limb_Ball_Bearing_Mount_long_v4, Shoulder_Joint_Ball_Bearing_Pin, Shoulder_Joint_Ball_Bearing_Pin_M3x8 | 2.2 h | 66 g |
| 2 | White PLA | Shoulder_Cover | 0.6 h | 18 g |

## What you need on hand

- Arduino UNO Media Carrier (and the UNO Q, to check that it presses on)
- SZBK07 regulator
- Two Raspberry Pi Camera Module 2s
- One servo (DS3218MG or MG996R) with its rubber dampeners and a 25T six-arm horn
- Two 625ZZ bearings
- Screws: 4× M3x8 (SZBK07), 8× M2x5 self-tapping (cameras), M3x20 + nuts (servo and shoulder cover), M2x8 + nuts
  (horn and Kooba pin)

## Checks

| Part | Check | Passes when |
| ---- | ----- | ----------- |
| Carrier_Mount_Test | Hook the carrier's edge opposite the USB-C under the two fixed hooks, then press the USB-C edge down past the two snap clips | The clips flex and click over the board without cracking; the carrier sits flat on the four pads without rocking; none of its bottom sockets or jacks touch the frame. Then press the UNO Q onto the carrier: the pads take the force and the carrier stays put. |
| SZBK07_Mount_Test | Screw the SZBK07 on with 4× M3x8 | All four holes line up; screws bite into the 2.6 mm pilot holes and hold |
| Sensormount_DualCam | Fit each camera from the back with 4× M2x5 | The board sits flat on the back face; the lens is centred in its window and the lens module sits in the recess without pressing; the cable connector on the bottom edge is free |
| Shoulder_Joint_Servomount_extended_BB | Fit the servo with its dampeners, M3x20 + nuts | The servo body slides in without filing and the mounting holes line up |
| Shoulder_Joint_Servo_Cap_Extended | Seat the servo horn, M2x8 screws | The horn sits flat in its recess and the screw holes line up with the horn's arms |
| Limb_Ball_Bearing_Mount_long_v4 | Press in a 625ZZ | The bearing presses in by hand or with light pressure and stays put |
| Shoulder_Cover | Press in a 625ZZ; hold against the cap's extension with M3x20 + nuts | The bearing seats in the 16.3 mm bore; the cover's screw holes line up with the cap |
| Shoulder_Joint_Ball_Bearing_Pin (Kooba, M2 bore) | Slide into the second bearing | The 5 mm pin goes into the bearing's centre snugly, without wobble |
| Shoulder_Joint_Ball_Bearing_Pin_M3x8 (robjk, M3 bore) | Same | Same |

## If something doesn't fit

**Carrier, regulator or camera mounts**: these are this project's own designs. Change the `Params` spreadsheet in
`cad/UnoQ_Mountingplate.FCStd` or `cad/Sensormount_DualCam.FCStd`, then regenerate the STLs and both projects:

| Problem | Parameter |
| ------- | --------- |
| Carrier too tight or loose between the clips | `Clip_Gap` (default 0.3 mm) |
| Snap clips too stiff, or crack | `Snap_T` (default 1.5 mm; thinner flexes more) or `Snap_Lip` (default 0.6 mm) |
| Carrier lifts off the hooks | `Hook_Lip` (default 1.5 mm) |
| Carrier's bottom sockets touch the plate | `Standoff_H` (default 5.5 mm; each extra mm also raises the servo plugs, which have 1.8 mm to the top cover) |
| M3 screws too tight or loose in the SZBK07 posts | `Buck_Screw_D` (default 2.6 mm) |
| SZBK07 holes don't line up (different board revision) | `Buck_SX`, `Buck_SY` |
| Camera lens off-centre in its window | `Cam_Lens_From_Top` (default 9.462 mm) |
| Camera holes don't line up | `Cam_Hole_SX`, `Cam_Hole_SY`, `Cam_Hole_Inset` |
| M2 screws too tight or loose in the camera mount | `Cam_Pilot_D` (default 1.8 mm) |

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_stls.py
python3 scripts/build_makerworld_3mf.py --no-orient --test-prints
python3 scripts/build_makerworld_3mf.py --no-orient
```

**Servo, horn, bearing and pin fits**: these are Kooba's and robjk's designs, printed successfully by many builders,
so a bad fit usually means the printer, not the model. Before editing any CAD:

- Run Bambu Studio's flow-rate calibration for the filament.
- If holes and bearing bores are tight but outside dimensions are right, set **X-Y hole compensation** (Process →
  Quality) to about +0.1 mm and re-slice. If pins and other outside dimensions are oversized, use **X-Y contour
  compensation** instead.
- Change these in the full robot project too, so the real parts print the same way.
