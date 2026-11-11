# Ideas

Additions that aren't built yet, and what each would take.

## Sensors

| Idea | What it takes |
| ---- | ------------- |
| ICM-20948 or BNO055 IMU (with compass; the BNO055 fuses on chip) | A mount in place of the GY-521 posts |
| HMC5883L magnetometer, or a GY-87 (MPU-6050 + compass) | A mount; only if the GY-521 stays |
| BMP180 barometer | A mount; I2C |
| PAJ7620U2 gesture sensor | A mount in the head; I2C |
| INA219 current/voltage sensor | A mount; I2C address 0x41 (A0 high), since the shield's PCA9685 is 0x40 |
| VL53L1X time-of-flight distance sensor | An opening in the middle of the camera mount; I2C. Stereo depth from the cameras may make it unnecessary. |

## Head and display

| Idea | What it takes |
| ---- | ------------- |
| Camera Module 3 (autofocus) | Media Carrier support for the IMX708. The board and hole pattern match; check the lens window and `Cam_Pupil_Depth` for its taller lens. |
| 0.96" SSD1306 OLED | `Top_Cover_Split_Rear_with_OLED` has the cutout; needs firmware support |

## Power

| Idea | What it takes |
| ---- | ------------- |
| Servo power cut-off | The SZBK07 has no enable pin: switch its input with a MOSFET or relay from a UNO Q GPIO, or pull the shield's OE pin high (servos go limp but stay powered) |
| Battery voltage monitoring | The INA219, or a resistor divider into a UNO Q analog pin |
