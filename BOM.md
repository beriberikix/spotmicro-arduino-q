# Bill of materials

This is the [SpotMicroESP32](https://github.com/michaelkubina/SpotMicroESP32#bill-of-material) /
[Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika/blob/main/docs/1_components.md) BOM, changed for the
Arduino UNO Q. The mechanical parts are unchanged; the electronics bay is new.

Links marked *search* go to a marketplace search, because these parts are sold by many vendors under the same name.
Check the specs listed in the notes before buying.

## Electronics

| Qty | Part | Notes | Where to buy |
| --- | ---- | ----- | ------------ |
| 1 | Arduino UNO Q, 4 GB (ABX00173) | Replaces the ESP32. Runs from the battery through VIN (7-24 V). The 2 GB ABX00162 has the same footprint. | [Arduino Store](https://store-usa.arduino.cc/products/uno-q-4gb) |
| 1 | PCA9685 16-channel 12-bit PWM driver | Same as Leika. Mounts on Kooba's existing posts. Runs on the UNO Q's 3.3 V I2C. | [Adafruit 815](https://www.adafruit.com/product/815) |
| 1 | Pololu D24V150F6, 6 V 15 A step-down regulator | Servo rail. 43.2 x 31.8 mm, M2 holes 38.86 x 25.4 mm; the plate posts are sized for it. Replaces the SZBK07/XL4016. About 17.5 A continuous at 8 V in. Dropout is about 1.3 V at 3 A and 1.45 V at 10 A, so it holds 6 V only while the pack is above about 7.4 V; below that the servos get a little less than 6 V, which is still inside their rating. | [Pololu 2882](https://www.pololu.com/product/2882) |
| 12 | Servos, 25T spline, standard size: DS3218MG (20 kg) or MG996R (11 kg) | See [Servos](#servos). Both fit the same mounts and run on the 6 V rail. | [DS3218 180°, HOOYIJ 4-pack (buy 3)](https://www.amazon.com/HOOYIJ-Digital-Waterproof-Crawler-Control/dp/B0CJ7B2MBN) · [DS3218MG search](https://www.amazon.com/s?k=DS3218MG+servo) · [MG996R search](https://www.amazon.com/s?k=MG996R+servo) |
| 12 | 25T six-arm servo horn (FSH6S type) | Often included with the servos. `Servohorn_6_B_Star` is a printable fallback. | [search](https://www.amazon.com/s?k=25T+servo+horn+aluminum) |
| 48 | Servo rubber dampeners | Usually included with the servos. | - |
| 4 | Servo extension cable, 10-15 cm | For the lower-leg servos. | [search](https://www.amazon.com/s?k=servo+extension+cable+15cm) |
| 1 | GY-521 (MPU-6050) IMU | The plate keeps Kooba's GY-521 posts. Leika also supports the ICM-20948 and BNO055, which need their own mount. | [search](https://www.amazon.com/s?k=GY-521+MPU6050) |
| 1 | 2S LiPo, 5200-6200 mAh, 30C+ | Fits Kooba's LiPo brackets under the plate. Feeds the UNO Q VIN and the servo regulator. | [search](https://www.amazon.com/s?k=2S+LiPo+5200mAh+hardcase) |
| 1 | Main power switch or 19 mm latching push button | Kooba's covers have a 19 mm cutout. | [search](https://www.amazon.com/s?k=19mm+latching+push+button+LED) |
| 1 | XT60 connector pair | Battery connector. | [search](https://www.amazon.com/s?k=XT60+connector+pair) |
| 1 | USB-C PD power supply, 5 V 3 A | For bench work and flashing. The UNO Q does not boot from a non-PD supply. | [search](https://www.amazon.com/s?k=USB-C+PD+charger+15W) |
| - | Wire (16 AWG for power, 22-26 AWG for signals), Dupont jumpers, heat shrink | | |

### Optional

| Qty | Part | Notes | Where to buy |
| --- | ---- | ----- | ------------ |
| 1 | INA219 current/voltage sensor | Servo rail monitoring and low-battery cut-off, as in Leika. Needs a mount. | [Adafruit 904](https://www.adafruit.com/product/904) |
| 2 | HC-SR04 ultrasonic sensor | Kubina's head holds two. The echo pin is 5 V; use a divider for the UNO Q's 3.3 V inputs. | [search](https://www.amazon.com/s?k=HC-SR04) |
| 1 | WS2812 LED ring, 12 LEDs, 50 mm | Status LEDs. | [search](https://www.amazon.com/s?k=WS2812B+12+LED+ring+50mm) |
| 1 | USB-C extension, right angle | Gives access to the UNO Q's USB-C port without removing the top cover. | [search](https://www.amazon.com/s?k=usb-c+right+angle+extension+short) |

### Removed from the ESP32 build

ESP32 DevKitC, ESP32-CAM, FT232RL USB-TTL adapter, LM2596 5 V buck (the UNO Q takes the battery on VIN),
HW-482 relay, micro-USB DIP adapters, ACS712 current sensor, 25 V voltage sensor, SZBK07/XL4016 buck.
The head's ESP32-CAM mount has no UNO Q replacement yet.

### Servos

| | MG996R | DS3218MG |
| - | ------ | -------- |
| Rated voltage | 4.8-7.2 V | 4.8-6.8 V |
| Stall torque at 6 V | about 11 kg·cm | about 20 kg·cm |
| Stall current | about 2.5 A at 6 V | about 1.8-2.6 A |
| Builder experience | Kubina: stands and walks, "not great, but also not horrible", with jitter and play. Leika: the minimum. | Kubina: walks significantly better, no jitter |

Buy the 180° version: Kubina's and Leika's calibration assumes 180°, and the 270° version moves a different amount per
signal step.

Both run directly from the 6 V rail and both need it: a full 2S pack (8.4 V) is above either rating.
A cheaper middle ground from Kubina: DS3218MG on the four lower legs (the most loaded joints) and MG996R elsewhere.
Twelve servos cannot all stall at once in normal use, so the regulator's 17.5 A continuous (32 A peak limit)
is enough for either choice.

## Hardware

From Kubina's BOM, plus the new electronics bay.

| Qty | Part | Used for |
| --- | ---- | -------- |
| 84 + 84 | M2x8 cylinder-head screws + M2 nuts | Servo horns, bearing pins |
| 80 + 80 | M3x8 cylinder-head screws + M3 nuts | General assembly |
| 64 + 64 | M3x20 cylinder-head screws + M3 nuts | Servos, upper legs |
| extra | M3x20 screws + M3 nuts | Reinforced shoulder covers to the extended servo caps. robjk doesn't give a count; a bulk pack covers it. |
| 4 + 4 | M3x8 screws + M3 nuts | robjk's bearing pins: each pin runs in the shoulder cover's 625ZZ and is screwed to the upper-leg shell's 3.2 mm hole on the pivot axis |
| 4 | M3x8 screws | UNO Q to the standoffs (2.6 mm pilot holes) |
| 4 | M2x6 screws | Pololu regulator to its posts (1.8 mm pilot holes) |
| 12 | 625ZZ ball bearing, unflanged | Shoulder and leg joints (8), plus the reinforced shoulder covers (4) |

[625ZZ search](https://www.amazon.com/s?k=625ZZ+bearing) ·
[M2/M3 screw kit search](https://www.amazon.com/s?k=M2+M3+socket+cap+screw+nut+kit)

## Printed parts

About 1 kg of PLA or PETG, plus a little TPU for the foot tips. Everything prints without supports.

All STLs are in [`stl/`](stl/README.md), with quantities, mirrored copies, material and infill for each part.
They are Kooba's SpotMicroESP32 parts, with:

- **The new electronics plate** (`stl/electronics/UnoQ_Mountingplate.stl`) in place of the ESP32 circuitry plate.
- **robjk's reinforced shoulders** in place of Kooba's shoulder joints. The shoulder cover adds a second, bearing-supported
  attachment to the outside of each upper leg, so the leg no longer hangs on the servo shaft alone. They need the matching
  upper-leg shell, `Limb_Top_Shell_with_BB_hole`, which replaces Kooba's `Limb_Top_Shell`.

### Optional: helper stand

Holds the robot by its belly with the legs hanging free. Leika's calibration guide needs this to level the IMU,
and it is handy for servo calibration and bench work. Print `stl/optional/helper-stand/`: 2× top, 2× bottom,
2× brace, 4× feet.

No changes needed: the body and covers are the same as Leika's, and the UNO Q build doesn't touch the underside.
Checked against the bottom cover's cross-section: the cover (113 mm wide) sits in the 126 mm cradle about 15 mm above
the cradle floor, held by the cradle's sides.
