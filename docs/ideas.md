# Ideas to explore

Optional parts and changes suggested by Leika, Kubina or Kooba that are not in the [BOM](../BOM.md) yet.

## Sensors

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| ICM-20948 or BNO055 IMU | Leika | Both have a compass; the BNO055 fuses on chip. Needs a mount on the plate in place of the GY-521 posts. |
| HMC5883L magnetometer | Leika | A compass for the MPU-6050. Only needed if the GY-521 stays. The GY-87 board combines both. |
| BMP180 barometer | Leika | Pressure, temperature and altitude over I2C. Needs a mount. |
| PAJ7620U2 gesture sensor | Leika | Hand-gesture interaction over I2C. Probably belongs in the head. |
| INA219 current/voltage sensor | Leika | Already listed as optional in the BOM. Needs a mount, and I2C address 0x41 (tie A0 high) because 0x40 is the servo shield's PCA9685. |
| Distance sensing | Leika, Kubina (2× HC-SR04) | The cameras took the ultrasonic sensors' place in the head. Stereo depth from the two cameras may cover it; otherwise a VL53L1X time-of-flight breakout on I2C, in a new opening in the camera mount's middle. |

## Camera and head

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| Camera Module 3 (autofocus) | - | The Media Carrier officially supports IMX219 (Camera Module 2) only. If Arduino adds IMX708 support, Camera Module 3 has the same board size and hole pattern, but a taller lens; check the mount's lens window and `Cam_Pupil_Depth`. |
| 0.96" SSD1306 OLED | Leika, Kubina | Kooba's `Top_Cover_Split_Rear_with_OLED` already has the cutout. Leika's firmware has no display driver. |

## Power

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| Servo power cut-off | Kubina (HW-482 relay) | The SZBK07 has no enable pin. Either switch its input with a MOSFET or relay module from a UNO Q GPIO, or pull the servo shield's OE pin high to stop driving the servos (they stay powered but go limp). |
| Battery voltage monitoring | Kubina (ACS712, 25 V sensor) | Covered by the INA219, or a resistor divider into a UNO Q analog pin. |
