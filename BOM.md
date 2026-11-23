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
| 1 | SZBK07 20 A step-down module | Servo rail at 6.0 V; set it before connecting servos. 60 x 45 mm board (about 60 x 56 x 33 mm with heatsinks and coil), M3 holes 39 x 53.5 mm. About 15 A continuous. | [search](https://www.amazon.com/s?k=SZBK07+20A+buck) |
| 2 | Raspberry Pi Camera Module 2 (IMX219) | Stereo pair in the head. Arducam's IMX219 V2 boards also fit the mount (same holes, lens 5 mm lower). | [Adafruit 3099](https://www.adafruit.com/product/3099) |
| 2 | Raspberry Pi camera cable, Standard–Mini, 200 mm | Camera to carrier. The cable in the camera box doesn't fit the carrier. | [Adafruit 5818](https://www.adafruit.com/product/5818) |
| 12 | DS3218 servo, 20 kg, **180°**, 25T spline | Many DS3218 listings are 270°; check the angle. See [Servos](#servos). | [Miuzei 4-pack (buy 3)](https://www.amazon.com/dp/B0FH53CKCS) · [HOOYIJ 4-pack](https://www.amazon.com/dp/B0CJ7B2MBN) |
| 12 | 25T six-arm servo horn (FSH6S type) | Often included with the servos. `Servohorn_6_B_Star` is a printable fallback. | [search](https://www.amazon.com/s?k=25T+servo+horn+aluminum) |
| 48 | Servo rubber dampeners | Usually included with the servos. | - |
| 4 | Servo extension cable, 10-15 cm | Lower-leg servos. | [search](https://www.amazon.com/s?k=servo+extension+cable+15cm) |
| 1 | Adafruit MPU-6050 6-DoF accel and gyro, STEMMA QT / Qwiic | On four posts on the plate, held with four M2x5 self-tapping screws. Same chip and I2C address (0x68) as a GY-521. | [Adafruit 3886](https://www.adafruit.com/product/3886) |
| 1 | STEMMA QT / Qwiic JST SH 4-pin cable, 200 mm | IMU to the UNO Q's Qwiic socket, routed round the front of the board stack (about 145 mm). | [Adafruit 4401](https://www.adafruit.com/product/4401) |
| 1 | 3S LiPo, about 5000-5200 mAh, 30C+, XT60, at most 138 x 47 x 25 mm | Sits in the LiPo brackets under the plate. The bay is 25.6 mm tall, so most 3S hard cases (37 mm) don't fit: use a soft case. The reference build uses a Zeee 3S 5200 mAh 50C soft case (132 x 43 x 25 mm, 343 g). | [search](https://www.amazon.com/s?k=3S+LiPo+5200mAh+soft+case+XT60) |
| 1 | LiPo balance charger, 3S capable | Charging the battery. | [search](https://www.amazon.com/s?k=LiPo+balance+charger+3S) |
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

DS3218 on all twelve joints: 20 kg·cm at 6 V, 4.8-6.8 V. MG996R (11 kg·cm) works but walks with jitter and play.

- Buy the 180° version (500-2500 µs for 0-180°); the gait calibration assumes 180°. The same seller often lists a
  270° pack under a near-identical title.
- Buy all twelve from one seller, so they centre and respond alike.
- "Waterproof" in the title doesn't matter; nearly every DS3218 is sold that way.
- Some DS3218s cut out after about 5 s at stall (overload protection). Standing and walking don't trigger it; a leg
  pressed against the stand can.
- The 6 V rail is required: a full 3S pack (12.6 V) is far above the rating.
- The battery is 3S, not 2S: the SZBK07 needs about 3 V more on its input than its output, so it can't hold 6.0 V from a
  2S pack (8.4 V full) and the rail sags to 4-5 V.
- The SZBK07's 15 A continuous is enough; twelve servos never all stall at once.

## Hardware

| Qty | Part | Used for |
| --- | ---- | -------- |
| 84 + 84 | M2x8 cylinder-head screws + M2 nuts | Servo horns, bearing pins |
| 76 + 76 | M3x8 cylinder-head screws + M3 nuts | General assembly |
| 12 | M3x8 screws | Knee mounts, servo caps and outer shoulders to the servo shafts (no nuts) |
| 64 + 64 | M3x20 cylinder-head screws + M3 nuts | Servos, upper legs |
| 12 + 12 | M3x20 screws + M3 nuts | Shoulder covers to the extended servo caps (3 per cover) |
| 4 | M3x8 screws | SZBK07 to its posts |
| 4 + 4 | M3x8 screws + M3 washers (DIN 125, 7 mm OD) | Media Carrier clamps: the washers clamp the carrier's short edges |
| 12 | M2x5 self-tapping screws | Cameras to the head mount (8), IMU to its posts (4) |
| 12 | 625ZZ ball bearing, unflanged | Shoulder and leg joints (8), shoulder covers (4) |

[625ZZ search](https://www.amazon.com/s?k=625ZZ+bearing) ·
[M2/M3 screw kit search](https://www.amazon.com/s?k=M2+M3+socket+cap+screw+nut+kit)

## Printed parts

About 1.2 kg of PLA (PETG works) and a little TPU for the feet, all without supports. Every STL is in
[`stl/`](stl/README.md) with quantities, mirrored copies, material and infill. Print the fit tests first (about 3 h):
see [docs/test-prints.md](docs/test-prints.md).

### Helper stand (optional, recommended)

Holds the robot by its belly with the legs free. You can build the robot without it, but from the body step on you'll
want it for servo checks, first power-on, IMU levelling and calibration: a robot resting on folded legs isn't level,
and a leg pressed against something can stall a servo.

Print `stl/optional/helper-stand/` (2× top, 2× bottom, 2× brace, 4× feet; about 2.7 h and 92 g of PLA, or the
MakerWorld "Helper stand" profile), plus:

| Qty | Part | Used for |
| --- | ---- | -------- |
| 4 + 4 | M3x12 screws + M3 nuts (M3x10 also fits); 8 M3 washers recommended | Each stand's top to its bottom: two per stand through the overlapping tabs (4.0 mm holes) |
| 8 + 8 | M3x16 screws + M3 nuts | The two braces between the stands: two per brace end, nuts in the brace's slots |

These sizes are confirmed on a real build. M3x8 is too short for both joints,
and M3x20 bottoms out in the brace ends (their holes are about 9 mm deep). A spare M3x20 does work in the tab joint,
with about 10 mm sticking out past the nut. The feet push onto the base corners; glue them if they're loose.
