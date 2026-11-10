# SpotMicro for Arduino UNO Q

A Spot Micro quadruped built around the [Arduino UNO Q](https://docs.arduino.cc/hardware/uno-q/) instead of an ESP32.
It is a port of [SpotMicroESP32-Leika](https://github.com/runeharlyk/SpotMicroESP32-Leika), which uses Michael Kubina's
[SpotMicroESP32](https://github.com/michaelkubina/SpotMicroESP32) printed parts, which in turn derive from KDY0523's
original [Spot Micro](https://www.thingiverse.com/thing:3445283).

![Exploding and reassembling the robot](docs/images/spot-unoq-explode.gif)

10-second loop rendered from `cad/SpotUnoQ.FCStd` by `scripts/explode_animation.FCMacro`; 1080p video:
[docs/images/spot-unoq-explode.mp4](docs/images/spot-unoq-explode.mp4).

**Print it:** [SpotMicro Robot Dog for Arduino UNO Q on MakerWorld](https://makerworld.com/en/models/3584508-spotmicro-robot-dog-for-arduino-uno-q)
(Bambu Studio print profiles for the P1S).

## Status

| Area | State |
| ---- | ----- |
| Mechanical (frame, legs, covers, head) | SpotMicroESP32, with robjk's reinforced shoulders, in the CAD assembly and the STLs |
| Electronics bay | New mounting plate for a stacked UNO Media Carrier, UNO Q and Adafruit servo shield, an SZBK07 regulator and the GY-521. Interference-checked in the full assembly. Not yet printed. |
| Head | Kooba's sensor mount, changed to hold two Raspberry Pi Camera Module 2s. Not yet printed. |
| Firmware | Not started. See [firmware/README.md](firmware/README.md). |

## Reinforced shoulders

![Reinforced shoulder](docs/images/reinforced-shoulder.png)

robjk's shoulder cover bolts to an extended servo cap and carries a 625ZZ bearing on the outside of the upper leg, so
each leg pivots on two supports instead of hanging on the servo shaft. In `cad/SpotUnoQ.FCStd` the parts are in the
`Reinforced_Shoulders_robjk` group, fitted to Kubina's assembly: the cover's bearing bore is on the shoulder servo axis to
within 0.3 mm on all four legs, and the covers and leg shells don't collide with anything.

## Electronics bay

![Electronics bay](docs/images/electronics-bay-top.png)

The boards form one stack at the rear of the plate:

- **Bottom:** an [Arduino UNO Media Carrier](https://store-usa.arduino.cc/products/uno-media-carrier).
- **Middle:** the UNO Q, plugged into the carrier's high-speed connectors.
- **Top:** Adafruit's [16-channel servo shield](https://www.adafruit.com/product/1411) on the UNO Q's headers.

The stack's front edge faces the head: the carrier's two camera connectors are underneath it, and the servo headers
sit on top of the shield. Right-angle headers make the servo plugs lie flat and point forward, 1.8 mm under the top
cover.

The red box in front of the stack is the SZBK07 servo regulator. The two orange ribbons are the camera cables. They
run flat on the plate, under the SZBK07, and through the front shoulder plates to the head.

The Media Carrier has no mounting holes; it hangs from the UNO Q's connectors. The plate holds it instead:

- four pads under the bare middle of its underside
- two fixed hooks on the edge opposite the USB-C
- two snap clips on the USB-C edge

Clip the carrier in first, then press the UNO Q onto it.

Clearances in the assembly:

| Between | Clearance |
| ------- | --------- |
| Servo plugs and the top cover | 1.8 mm |
| SZBK07 and the top cover | 4.5 mm |
| Media Carrier bottom sockets and the plate | 0.95 mm |
| Board stack and the battery-cable tunnel (rear) | 0.7 mm |
| Servo plugs and the SZBK07 | 5.5 mm |

The servo wires run sideways into the channels on either side of the SZBK07: 23 mm wide on the left, 19 mm on the
right. The UNO Q's USB-C port faces the right side rail, 20 mm away, so use a right-angle USB-C plug or program it
over Wi-Fi.

The plate has no raised power-cable cap like Kooba's. The XT60 battery lead runs under the plate beside the battery
and comes up through the slot at the rear-left corner.

Power, from a 2S LiPo (7.4-8.4 V):

- **UNO Q:** straight from the battery into VIN (7-24 V). The Media Carrier is powered through the UNO Q.
- **Servos:** SZBK07 set to 6.0 V, into the shield's V+ terminal block. The SZBK07 needs about 1-2 V of headroom, so
  it holds 6.0 V down to roughly 7.5 V of battery; below that the servo rail follows the battery down, still inside
  the servos' rating.
- **Logic:** the shield's PCA9685 and the IMU are on the UNO Q's I2C.

Every position, height and clearance is in the `Params` spreadsheet in `cad/UnoQ_Mountingplate.FCStd`:

- **Stack:** `Carrier_X0`, `Carrier_Y0`, `Standoff_H`, `Standoff_D`.
- **Clips:** `Clip_W`, `Clip_Gap`, `Hook_T`, `Hook_Lip`, `Snap_T`, `Snap_Lip`, `Lip_H`.
- **SZBK07:** `Buck_CX`, `Buck_CY`, `Buck_SX`, `Buck_SY`, `Buck_H`, `Buck_Post_D`, `Buck_Screw_D`.

## Cameras

![Camera head](docs/images/camera-head.png)

Two Raspberry Pi Camera Module 2s replace Leika's ultrasonic sensors, in about the same place. The Media Carrier
officially supports only IMX219 cameras, which is why this uses Camera Module 2 and not Camera Module 3. The cameras
are 47 mm apart and face the same way as the head, so their images are parallel for stereo.

`cad/Sensormount_DualCam.FCStd` is Kooba's sensor mount with these changes:

- The ultrasonic and ESP32-CAM openings are filled in.
- Each camera gets a recess on the back for its lens module, four M2 pilot holes, and a lens window that opens
  towards the front to clear its full 62° × 49° field of view.

Every camera dimension is in the mount's `Params` spreadsheet. The lens position (`Cam_Lens_From_Top`, 9.46 mm
below the board's top edge) uses commonly cited Camera Module 2 figures that haven't been checked against an
official drawing, so check it on the first print.

Use two **Standard–Mini 200 mm** camera cables; the cable in the camera box is Standard–Standard and doesn't fit the
carrier. The modelled routes (`FPC_left`, `FPC_right` in the assembly) use about 172 mm each, leaving about 28 mm of
slack to fold flat in the shoulder box. The cable nearer the carrier's USB-C edge goes to the right camera.

Parts and buy links are in [BOM.md](BOM.md). Optional sensors and changes not yet in the BOM are in
[docs/ideas.md](docs/ideas.md).

## Repository layout

```
cad/
  SpotUnoQ.FCStd              full assembly: Kubina's assembly (linked), robjk's shoulders, the new electronics and head
  UnoQ_Mountingplate.FCStd    new electronics plate (parametric, PartDesign)
  Sensormount_DualCam.FCStd   two-camera head mount (parametric, PartDesign)
  UnoQ_board.FCStd            UNO Q model, built by scripts/fetch-references.sh (not committed)
  MediaCarrier_board.FCStd    Media Carrier model, built by scripts/fetch-references.sh (not committed)
stl/                          every printable part, with quantities (stl/README.md)
step/                         the same parts as STEP, from the designers' FreeCAD sources (see below)
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

This downloads Kubina's assembly and Arduino's UNO Q and Media Carrier models, and builds `cad/UnoQ_board.FCStd` and
`cad/MediaCarrier_board.FCStd`. On macOS it expects
FreeCAD at `/Applications/FreeCAD.app`; set `FREECADCMD` otherwise.

Then open `cad/SpotUnoQ.FCStd`. FreeCAD asks to open the linked documents; allow it.

To print, you only need [`stl/`](stl/README.md).

To regenerate `stl/` (for example after changing the plate or the camera mount), you also need Kooba's and robjk's original files.
Thingiverse blocks scripted downloads, so download them by hand with "Download all files" and unzip them:
[thing:4559827](https://www.thingiverse.com/thing:4559827) (three zips) into `reference/kooba/`, and
[thing:4937631](https://www.thingiverse.com/thing:4937631) into `reference/robjk/`. Then run:

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_stls.py
```

### STEP files

`step/` mirrors `stl/` with STEP versions of every part that has a FreeCAD source: Kooba's parts, robjk's shoulder
cover, extended cap, upper-leg shell and medium rear cover, and this project's electronics plate and camera mount
(written by `scripts/export_stls.py`).
Each solid is fitted to its STL so the two match in print orientation and position; the script refuses any part whose
STL surface lies more than 0.1 mm from the STEP (95th percentile). robjk's extended servo mount and M3 bearing pin
exist only as STL upstream.

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd scripts/export_steps.py
```

### Exploded-view animation

`scripts/explode_animation.FCMacro` renders the exploded turntable loop from the assembly and encodes
`docs/images/spot-unoq-explode.mp4` (1080p) and `.gif` with ffmpeg (`brew install ffmpeg`). Run it inside the FreeCAD
GUI with `cad/SpotUnoQ.FCStd` open: Macro → Macros… → Execute, or from the Python console:

```python
exec(open("/path/to/spotmicro-arduino-q/scripts/explode_animation.FCMacro").read())
```

If the assembly isn't open, set `SPOT_ROOT` to the repository first so the macro can find it.

Timing, size, frame rate and how far each group of parts moves are settings at the top of the file. Frames are rendered
at twice the output size and scaled down, since FreeCAD's image export doesn't anti-alias. The macro puts every part
back when it finishes and doesn't save the document.

### MakerWorld project

```sh
python3 scripts/build_makerworld_3mf.py --no-orient
```

writes `makerworld/SpotUnoQ_P1S.3mf`: a sliced Bambu Studio project for the P1S (0.4 mm nozzle, 0.20 mm Standard),
10 plates, one filament each (Bambu PLA Basic black and white, Bambu TPU 95A HF), auto-arranged plate by plate, with
100% infill on the covers and 20% elsewhere. The script stops if any part fails to land on its plate or Bambu Studio
reports a slicing warning. Without `--no-orient` it also auto-orients every part, which lays
`Top_Cover_Split_Rear_with_OLED` down in a position that needs supports.

Add `--test-prints` for `makerworld/SpotUnoQ_P1S_test_prints.3mf`: a 2.8-hour, 84 g fit test to print before the
robot. One black plate has the Media Carrier pads and clips and the SZBK07 posts (cut from the electronics plate onto
thin frames), the camera mount, a shoulder servo mount, an extended servo cap, an upper-leg bearing mount and one of
each bearing pin; one white plate has a shoulder cover. See [docs/test-prints.md](docs/test-prints.md) for what to check and what to change if
something doesn't fit.

### Coordinate frame

The plate and cover files share a body frame: +Y toward the head, +X to the robot's right, plate top at Z = 5 mm,
side rails centered at Z ≈ 10 mm. In the assembly that frame is Kubina's `Chassis All` placement multiplied by a
translation of (55, 0, -9.75) mm.

### Driving FreeCAD from Claude Code

`.mcp.json` registers the [freecad-mcp](https://github.com/neka-nat/freecad-mcp) server for this project, so Claude
Code can open, edit and render the CAD in a running FreeCAD while you watch. It has two halves: an addon that runs
inside FreeCAD and listens on `127.0.0.1:9875`, and an MCP server that Claude Code starts with `uvx`. Setup on macOS:

1. **Install FreeCAD 1.1 and uv** (uv provides `uvx`, which runs the MCP server):

   ```sh
   brew install --cask freecad
   brew install uv
   ```

2. **Install the FreeCAD addon.** Create the `Mod` folder first; if it doesn't exist, `cp -r` copies the addon's
   contents into a new folder named `Mod` instead of into `Mod/FreeCADMCP`, and FreeCAD won't find it.

   ```sh
   git clone https://github.com/neka-nat/freecad-mcp.git /tmp/freecad-mcp
   mkdir -p ~/Library/Application\ Support/FreeCAD/v1-1/Mod
   cp -r /tmp/freecad-mcp/addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/v1-1/Mod/
   ```

   The result should be `~/Library/Application Support/FreeCAD/v1-1/Mod/FreeCADMCP/InitGui.py`. Other platforms and
   FreeCAD versions use other folders; see the addon's
   [installation guide](https://github.com/neka-nat/freecad-mcp/blob/main/docs/installation.md#addon-directory).

3. **Start the addon's server with FreeCAD** (optional, saves a click every launch). It only listens on 127.0.0.1:

   ```sh
   echo '{"remote_enabled": false, "allowed_ips": "127.0.0.1", "auto_start_rpc": true, "auth_token": ""}' \
     > ~/Library/Application\ Support/FreeCAD/v1-1/freecad_mcp_settings.json
   ```

   Without this, choose the **MCP Addon** workbench in FreeCAD and click **Start RPC Server** each time.

4. **Open FreeCAD** (quit and reopen it if it was running when you installed the addon). The Report view should show
   the server listening on `127.0.0.1:9875`.

5. **Start Claude Code in this repository** and approve the `freecad` server from `.mcp.json` when asked. Run `/mcp`
   to check that it's connected. If FreeCAD wasn't running when Claude Code started, reconnect it from `/mcp`.

Claude Code only reaches FreeCAD while FreeCAD is open with the addon's server running. Heavy mesh operations through
the server (for example booleans on large STLs) can crash FreeCAD; the scripts in `scripts/` run headless with
`freecadcmd` instead and don't need the addon.

## License

- Code (scripts, firmware): MIT, see [LICENSE](LICENSE).
- Hardware and documentation (CAD in `cad/`, renders, docs): CC BY-SA 4.0, see [LICENSE-HARDWARE](LICENSE-HARDWARE).

Third-party work keeps its own license; see [NOTICE.md](NOTICE.md). Most files in `stl/` are Kooba's and robjk's
parts (CC BY) and the helper stand (CC BY 4.0 and MIT). In particular, Kubina's assembly is GPL-3.0 and is
fetched rather than redistributed.
