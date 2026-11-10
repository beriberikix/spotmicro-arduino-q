# Background

Where this robot's design comes from, and what changed along the way. Licenses and exact file-level changes are in
[NOTICE.md](../NOTICE.md).

## Lineage

| Project | Author | What this robot uses from it |
| ------- | ------ | ---------------------------- |
| [Spot Micro](https://www.thingiverse.com/thing:3445283) | Deok-yeon Kim (KDY0523) | The original quadruped design every Spot Micro derives from |
| [SpotMicroESP32, printable parts](https://www.thingiverse.com/thing:4559827) | Michael Kubina (Kooba) | Every printed part except the electronics plate and the reinforced shoulders; the FreeCAD sources for the electronics plate and the camera mount |
| [SpotMicroESP32, repository](https://github.com/michaelkubina/SpotMicroESP32) | Michael Kubina | The full FreeCAD assembly that `cad/SpotUnoQ.FCStd` links, the parts list, and servo experience |
| [SpotMicroESP32-Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika) | Rune Harlyk | Kinematics, the electronics list this build started from, the helper stand selection, and the firmware to be ported |
| [Reinforced shoulders](https://www.thingiverse.com/thing:4937631) | robjk | Shoulder cover, extended servo cap and mount, M3 bearing pin, upper-leg shell with bearing hole, medium rear cover |
| [Stronger microspot stand top](https://www.thingiverse.com/thing:4814187) | stefi01 | Helper stand top |
| [Nova-SM2](https://github.com/cguweb-com/Arduino-Projects/tree/main/Nova-SM2) | cguweb | Helper stand bottom, brace and feet |

## From the ESP32 build to the UNO Q

Leika and Kubina's builds run on an ESP32. This one replaces it with an Arduino UNO Q, which pairs a Linux processor
(Qualcomm QRB2210) with a real-time microcontroller (STM32U585), and changes the electronics around it:

| ESP32 build | This build | Why |
| ----------- | ---------- | --- |
| ESP32 DevKitC | Arduino UNO Q | Linux and a real-time MCU on one board |
| PCA9685 breakout (Adafruit 815) | Adafruit servo shield (#1411), same PCA9685 | Stacks on the UNO Q, so the servo board takes no plate space |
| SZBK07 or XL4016 on Kooba's plates (an early version of this build used a Pololu D24V150F6) | SZBK07 | Cheap and common |
| LM2596 5 V buck for the ESP32 | None | The UNO Q takes the battery on VIN (7-24 V) |
| ESP32-CAM, or OV2640/OV5640 (Leika) | Two Raspberry Pi Camera Module 2s on an Arduino UNO Media Carrier | Stereo MIPI-CSI cameras; the carrier officially supports IMX219 only, so not Camera Module 3 |
| Two HC-SR04 ultrasonic sensors in the head | Removed | The cameras take their place |
| HW-482 relay, ACS712 current sensor, 25 V voltage sensor, FT232RL USB-TTL adapter, micro-USB DIP adapters | Removed | Not needed with the UNO Q; INA219 monitoring is an option |

## Changes to upstream parts

- **Electronics plate:** started as Kooba's `Circuitry_Mountingplate_SZBK07`. The ESP32, LM2596, relay and PCA9685
  features are gone. So is the raised power-cable cap over the battery-lead channel, because the board stack and the
  SZBK07 don't both fit with it; the battery lead now runs under the plate beside the battery. New: the Media Carrier
  pads and clips (the carrier has no mounting holes) and the SZBK07 posts.
- **Camera mount:** started as Kooba's `sensormount_esp32_cam`. The HC-SR04 holes and the ESP32-CAM lens and flash
  openings are filled; two camera mounts with flared lens windows are added.
- **Shoulders:** robjk's reinforced set replaces Kooba's shoulder joints and upper-leg top shell.
- **Head:** Kooba's ESP32-CAM mount and its counterpiece are no longer printed.

Two earlier layouts were modelled and dropped: a UNO Q on standoffs with a PCA9685 breakout and a Pololu D24V150F6
regulator, and a version that kept the HC-SR04s.

## Servo experience

From Kubina's and Leika's builds:

- **MG996R:** stands and walks, "not great, but also not horrible" (Kubina), with jitter and play. Leika treats it as
  the minimum.
- **DS3218MG:** walks significantly better with no jitter (Kubina).
- **Mixed:** Kubina suggests DS3218MG on the four lower legs, the most loaded joints, and MG996R elsewhere.

## Helper stand

Leika's helper stand fits unchanged: the body and covers are the same as Leika's, and the bottom cover (113 mm wide)
sits in the 126 mm cradle about 15 mm above its floor, held by the cradle's sides.
