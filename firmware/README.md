# Firmware

Not started. The plan is to port [Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika)
(ESP-IDF/FreeRTOS on an ESP32) to the UNO Q.

The UNO Q has two processors:

- **STM32U585 MCU** (Arduino sketches, 3.3 V I/O): drives the UNO headers and the Qwiic port. It is the natural home for the
  real-time loop: PCA9685 servo output over I2C, IMU reads, gait timing.
- **Qualcomm QRB2210 MPU** (Debian Linux): Wi-Fi, the web app, the two cameras over MIPI-CSI (through the Media Carrier), and higher-level planning.

Leika's kinematics and gait code (`esp32/include/kinematics.h` and the motion service) are the parts most worth carrying over.
Its ESP32-specific networking, camera and peripheral drivers would be replaced.
