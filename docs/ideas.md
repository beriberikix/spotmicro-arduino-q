# Ideas to explore

Optional parts and changes suggested by Leika, Kubina or Kooba that are not in the [BOM](../BOM.md) yet.

## Sensors

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| ICM-20948 or BNO055 IMU | Leika | Both have a compass; the BNO055 fuses on chip. Needs a mount on the plate in place of the GY-521 posts. |
| HMC5883L magnetometer | Leika | A compass for the MPU-6050. Only needed if the GY-521 stays. The GY-87 board combines both. |
| BMP180 barometer | Leika | Pressure, temperature and altitude over I2C. Needs a mount. |
| PAJ7620U2 gesture sensor | Leika | Hand-gesture interaction over I2C. Probably belongs in the head. |
| INA219 current/voltage sensor | Leika | Already listed as optional in the BOM. Needs a mount, and I2C address 0x41 (tie A0 high) because 0x40 is the PCA9685's. |

## Camera and head

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| Camera | Leika (OV2640/OV5640), Kubina (ESP32-CAM) | The ESP32 cameras don't apply. Options: a USB camera, or a MIPI-CSI camera on the UNO Q's JMEDIA connector through a carrier. Either needs a new head mount in place of `cameramount_esp32_cam`. |
| 0.96" SSD1306 OLED | Leika, Kubina | Kooba's `Top_Cover_Split_Rear_with_OLED` already has the cutout. Leika's firmware has no display driver. |

## Power

| Idea | Suggested by | What it would take |
| ---- | ------------ | ------------------ |
| Servo power cut-off | Kubina (HW-482 relay) | No relay needed: drive the Pololu D24V150F6's EN pin low from a UNO Q GPIO to switch the servo rail off. Wiring only. |
| Battery voltage monitoring | Kubina (ACS712, 25 V sensor) | Covered by the INA219, or a resistor divider into a UNO Q analog pin. |
