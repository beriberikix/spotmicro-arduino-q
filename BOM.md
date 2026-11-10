# Bill of materials

Everything needed for one robot. *Search* links go to a marketplace search for parts sold under the same name by
many vendors; check the specs in the notes before buying.

## Electronics

| Qty | Part | Notes | Where to buy |
| --- | ---- | ----- | ------------ |
| 1 | Arduino UNO Q, 4 GB (ABX00173) | Runs from the battery through VIN (7-24 V). The 2 GB ABX00162 fits the same way. | [Arduino Store](https://store-usa.arduino.cc/products/uno-q-4gb) |
| 1 | Arduino UNO Media Carrier (ASX00083) | Under the UNO Q; provides the two camera connectors. Held by the plate's pads and clips. | [Arduino Store](https://store-usa.arduino.cc/products/uno-media-carrier) |
| 1 | Adafruit 16-channel 12-bit PWM/Servo Shield (PCA9685) | On top of the UNO Q. Solder the plain male header strip it comes with, not stacking headers. | [Adafruit 1411](https://www.adafruit.com/product/1411) |
| 1 | Right-angle 3x4 male headers, 4-pack | In place of the shield's straight servo headers, so the plugs fit under the top cover. | [Adafruit 816](https://www.adafruit.com/product/816) |
| 1 | SZBK07 20 A step-down module | Servo rail at 6.0 V; set it before connecting servos. 60 x 54 x 28 mm, M3 holes 39 x 53.5 mm. About 15 A continuous. | [search](https://www.amazon.com/s?k=SZBK07+20A+buck) |
| 2 | Raspberry Pi Camera Module 2 (IMX219) | Stereo pair in the head. | [Adafruit 3099](https://www.adafruit.com/product/3099) |
| 2 | Raspberry Pi camera cable, Standard–Mini, 200 mm | Camera to carrier. The cable in the camera box doesn't fit the carrier. | [Adafruit 5818](https://www.adafruit.com/product/5818) |
| 12 | Servos, 25T spline, standard size: DS3218MG (20 kg) or MG996R (11 kg) | See [Servos](#servos). | [DS3218 180°, HOOYIJ 4-pack (buy 3)](https://www.amazon.com/HOOYIJ-Digital-Waterproof-Crawler-Control/dp/B0CJ7B2MBN) · [DS3218MG search](https://www.amazon.com/s?k=DS3218MG+servo) · [MG996R search](https://www.amazon.com/s?k=MG996R+servo) |
| 12 | 25T six-arm servo horn (FSH6S type) | Often included with the servos. `Servohorn_6_B_Star` is a printable fallback. | [search](https://www.amazon.com/s?k=25T+servo+horn+aluminum) |
| 48 | Servo rubber dampeners | Usually included with the servos. | - |
| 4 | Servo extension cable, 10-15 cm | Lower-leg servos. | [search](https://www.amazon.com/s?k=servo+extension+cable+15cm) |
| 1 | GY-521 (MPU-6050) IMU | Mounts on the plate's GY-521 posts. | [search](https://www.amazon.com/s?k=GY-521+MPU6050) |
| 1 | 2S LiPo, 5200-6200 mAh, 30C+ | Sits in the LiPo brackets under the plate. | [search](https://www.amazon.com/s?k=2S+LiPo+5200mAh+hardcase) |
| 1 | Main power switch or 19 mm latching push button | Fits the covers' 19 mm cutout. | [search](https://www.amazon.com/s?k=19mm+latching+push+button+LED) |
| 1 | XT60 connector pair | Battery connector. | [search](https://www.amazon.com/s?k=XT60+connector+pair) |
| 1 | USB-C PD power supply, 5 V 3 A | Bench work and flashing. The UNO Q does not boot from a non-PD supply. | [search](https://www.amazon.com/s?k=USB-C+PD+charger+15W) |
| - | Wire (16 AWG for power, 22-26 AWG for signals), Dupont jumpers, heat shrink | | |

### Optional

| Qty | Part | Notes | Where to buy |
| --- | ---- | ----- | ------------ |
| 1 | USB-C extension, right angle | Reaches the UNO Q's USB-C port, which faces a side rail 20 mm away. | [search](https://www.amazon.com/s?k=usb-c+right+angle+extension+short) |
| 1 | INA219 current/voltage sensor | Servo-rail monitoring. Needs a mount and I2C address 0x41. | [Adafruit 904](https://www.adafruit.com/product/904) |
| 1 | WS2812 LED ring, 12 LEDs, 50 mm | Status LEDs. | [search](https://www.amazon.com/s?k=WS2812B+12+LED+ring+50mm) |

### Servos

| | MG996R | DS3218MG |
| - | ------ | -------- |
| Rated voltage | 4.8-7.2 V | 4.8-6.8 V |
| Stall torque at 6 V | about 11 kg·cm | about 20 kg·cm |
| Stall current | about 2.5 A at 6 V | about 1.8-2.6 A |
| Walking | Works, with jitter and play | Smooth |

- Buy the 180° version; the gait calibration assumes 180°.
- Both need the 6 V rail: a full 2S pack (8.4 V) is above either rating.
- To save money, use DS3218MG on the four lower legs (the most loaded joints) and MG996R elsewhere.
- The SZBK07's 15 A continuous is enough for either; twelve servos never all stall at once.

## Hardware

| Qty | Part | Used for |
| --- | ---- | -------- |
| 84 + 84 | M2x8 cylinder-head screws + M2 nuts | Servo horns, bearing pins |
| 80 + 80 | M3x8 cylinder-head screws + M3 nuts | General assembly |
| 64 + 64 | M3x20 cylinder-head screws + M3 nuts | Servos, upper legs |
| extra | M3x20 screws + M3 nuts | Shoulder covers to the extended servo caps; buy a bulk pack |
| 4 + 4 | M3x8 screws + M3 nuts | Shoulder bearing pins to the upper-leg shells |
| 4 | M3x8 screws | SZBK07 to its posts |
| 8 | M2x5 self-tapping screws | Cameras to the head mount |
| 12 | 625ZZ ball bearing, unflanged | Shoulder and leg joints (8), shoulder covers (4) |

[625ZZ search](https://www.amazon.com/s?k=625ZZ+bearing) ·
[M2/M3 screw kit search](https://www.amazon.com/s?k=M2+M3+socket+cap+screw+nut+kit)

## Printed parts

About 1.2 kg of PLA (PETG works) and a little TPU for the feet, all without supports. Every STL is in
[`stl/`](stl/README.md) with quantities, mirrored copies, material and infill. Print the fit tests first (about 3 h):
see [docs/test-prints.md](docs/test-prints.md).

### Optional: helper stand

Holds the robot by its belly with the legs free, for IMU levelling, servo calibration and bench work. Print
`stl/optional/helper-stand/`: 2× top, 2× bottom, 2× brace, 4× feet.
