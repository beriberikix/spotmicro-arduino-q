# servo_tool

An Arduino App Lab app for the UNO Q with the Adafruit servo shield: test the twelve servos, and set each one to the
right angle while its horn goes on. Used on the build guide's
[Test and label the servos](https://beriberikix.github.io/spotmicro-arduino-q/prepare/servos/) page and on every
page where a horn is fitted.

- `sketch/` runs on the microcontroller and drives the PCA9685. It takes commands from App Lab's Serial Monitor
  (type `h`) and from the web page over the Bridge.
- `python/` and `assets/` serve the web page on port 7000: one tab per guide page (Test servos, Knee joint,
  Hip joint, Install shoulders), with the same steps as the guide and a button for each servo move.

`assets/libs/` is Arduino's WebUI client (`arduino.js`, MPL-2.0) and Socket.IO 4.8.1 (MIT), copied from App Lab's
Web UI brick examples.

The guide links to a packed copy, `site/public/downloads/servo_tool.zip`. After changing anything here, rebuild it
with `scripts/build_servo_tool_zip.sh`.
