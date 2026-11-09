# spot-unoq

A Spot Micro quadruped built around the [Arduino UNO Q](https://docs.arduino.cc/hardware/uno-q/) instead of an ESP32.
It is a port of [SpotMicroESP32-Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika), which uses Michael Kubina's
[SpotMicroESP32](https://github.com/michaelkubina/SpotMicroESP32) printed parts, which in turn derive from KDY0523's
original [Spot Micro](https://www.thingiverse.com/thing:3445283).

![Assembled robot, top cover hidden](docs/images/spot-unoq-iso.png)

## Status

| Area | State |
| ---- | ----- |
| Mechanical (frame, legs, covers, head) | Unchanged from SpotMicroESP32 |
| Electronics bay | New mounting plate for the UNO Q, PCA9685, GY-521 and a Pololu 6 V 15 A regulator. Interference-checked in the full assembly. Not yet printed. |
| Firmware | Not started. See [firmware/README.md](firmware/README.md). |
| Head camera mount | Still the ESP32-CAM mount; needs a redesign for a USB or MIPI-CSI camera |

## Electronics bay

![Electronics bay](docs/images/electronics-bay-top.png)

The UNO Q sits middle-left on four 8 mm standoffs, USB-C facing the rear. The standoffs clear the two bottom
connectors (JMISC, JMEDIA), which hang 5 mm below the board. Green is the PCA9685, red is the servo regulator,
yellow is an 8 mm space reserved above the UNO Q headers for plugged-in wires.

Clearances in the assembly: UNO Q to top cover 7.9 mm, wiring space to top cover 3.4 mm, UNO Q to side rails 4.4 mm,
regulator to UNO Q 5.8 mm.

Power, from a 2S LiPo (7.4-8.4 V):

- **UNO Q:** straight from the battery into VIN (7-24 V). The ESP32 build's LM2596 5 V buck is gone.
- **Servos:** Pololu D24V150F6 at 6 V, through the PCA9685's V+ terminal.
- **Logic:** PCA9685 and IMU on the UNO Q's 3.3 V I2C (UNO header A4/A5 or Qwiic).

Positions, standoff heights, hole sizes and the regulator hole spacing are all in the `Params` spreadsheet in
`cad/UnoQ_Mountingplate.FCStd`. If you use a different regulator, change `Buck_SX`, `Buck_SY` and `Buck_Screw_D`.

Parts and buy links are in [BOM.md](BOM.md). Optional sensors and changes not yet in the BOM are in
[docs/ideas.md](docs/ideas.md).

## Repository layout

```
cad/
  SpotUnoQ.FCStd              full assembly: links Kubina's assembly + the new electronics
  UnoQ_Mountingplate.FCStd    new electronics plate (parametric, PartDesign)
  UnoQ_board.FCStd            UNO Q model, built by scripts/fetch-references.sh (not committed)
  export/                     STL and STEP of the new plate for printing
docs/images/                  renders
firmware/                     placeholder for the Leika port
scripts/                      fetch third-party CAD, build the board model
reference/                    downloaded third-party CAD (not committed)
```

## Getting started

Requires [FreeCAD](https://www.freecad.org/) 1.1 or later.

```sh
scripts/fetch-references.sh
```

This downloads Kubina's assembly and Arduino's UNO Q model, and builds `cad/UnoQ_board.FCStd`. On macOS it expects
FreeCAD at `/Applications/FreeCAD.app`; set `FREECADCMD` otherwise.

Then open `cad/SpotUnoQ.FCStd`. FreeCAD asks to open the linked documents; allow it.

Kooba's individual part files are only needed to edit or print the unchanged parts. Thingiverse blocks scripted
downloads, so get them from [thing:4559827](https://www.thingiverse.com/thing:4559827) ("Download all files", three
zips) and unzip them into `reference/kooba/`.

### Coordinate frame

The plate and cover files share a body frame: +Y toward the head, +X to the robot's right, plate top at Z = 5 mm,
side rails centered at Z ≈ 10 mm. In the assembly that frame is Kubina's `Chassis All` placement multiplied by a
translation of (55, 0, -9.75) mm.

### Driving FreeCAD from Claude Code

`.mcp.json` registers [freecad-mcp](https://github.com/neka-nat/freecad-mcp). To use it, install its FreeCAD addon in
FreeCAD's `Mod` directory (`~/Library/Application Support/FreeCAD/v1-1/Mod/FreeCADMCP` on macOS) and start its RPC
server from the MCP Addon workbench.

## License

- Code (scripts, firmware): MIT, see [LICENSE](LICENSE).
- Hardware and documentation (CAD in `cad/`, renders, docs): CC BY-SA 4.0, see [LICENSE-HARDWARE](LICENSE-HARDWARE).

Third-party work keeps its own license; see [NOTICE.md](NOTICE.md). In particular, Kubina's assembly is GPL-3.0 and is
fetched rather than redistributed.
