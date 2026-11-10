#!/usr/bin/env bash
# Fetch the third-party CAD this project builds on. These files are not committed
# (size and licensing), so run this once after cloning.
#
#   reference/kubina/assembled.FCStd   Michael Kubina's full SpotMicroESP32 assembly (GPL-3.0)
#   reference/unoq/step/               Arduino UNO Q STEP model (Arduino)
#   cad/UnoQ_board.FCStd               built from the STEP, linked by cad/SpotUnoQ.FCStd
#   reference/media-carrier/step/      Arduino UNO Media Carrier STEP model (Arduino)
#   cad/MediaCarrier_board.FCStd       built from it, linked by cad/SpotUnoQ_MediaCarrier.FCStd
#
#   reference/leika/helper_stand/      Leika's helper stand STLs (stefi01 CC BY 4.0, Nova-SM2 MIT)
#
# Kooba's (thing:4559827) and robjk's (thing:4937631) files are CC BY and must be downloaded
# by hand, because Thingiverse blocks scripted downloads. See README.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FREECADCMD="${FREECADCMD:-/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd}"

mkdir -p "$ROOT/reference/kubina" "$ROOT/reference/unoq"

KUBINA="$ROOT/reference/kubina/assembled.FCStd"
if [[ ! -f "$KUBINA" ]]; then
  echo "Downloading Kubina assembly (~67 MB)..."
  curl -fL -o "$KUBINA" \
    "https://raw.githubusercontent.com/michaelkubina/SpotMicroESP32/master/assembly/spotmicroesp32_assembled_quick_and_dirty.FCStd"
fi

STAND="$ROOT/reference/leika/helper_stand"
mkdir -p "$STAND"
for f in 2x_stand_top 2x_stand_bottom 2x_stand_brace 4x_stand_feet; do
  [[ -f "$STAND/$f.stl" ]] || curl -fL -o "$STAND/$f.stl" \
    "https://raw.githubusercontent.com/runeharlyk/SpotMicroESP32-Leika/master/hardware/printable/helper_stand/$f.stl"
done

STEP_ZIP="$ROOT/reference/unoq/ABX00162-step.zip"
if [[ ! -f "$STEP_ZIP" ]]; then
  echo "Downloading Arduino UNO Q STEP model..."
  curl -fL -o "$STEP_ZIP" "https://docs.arduino.cc/resources/models/ABX00162-step.zip"
fi
unzip -oq "$STEP_ZIP" -d "$ROOT/reference/unoq/step"

if [[ ! -f "$ROOT/cad/UnoQ_board.FCStd" ]]; then
  if [[ -x "$FREECADCMD" ]]; then
    echo "Building cad/UnoQ_board.FCStd..."
    UNOQ_STEP="$ROOT/reference/unoq/step/UNO Q simplified.stp" \
    UNOQ_OUT="$ROOT/cad/UnoQ_board.FCStd" \
      "$FREECADCMD" "$ROOT/scripts/build_unoq_board.py"
  else
    echo "freecadcmd not found; set FREECADCMD and re-run to build cad/UnoQ_board.FCStd" >&2
    exit 1
  fi
fi

MC_ZIP="$ROOT/reference/media-carrier/ASX00083-step.zip"
mkdir -p "$ROOT/reference/media-carrier/step"
if [[ ! -f "$MC_ZIP" ]]; then
  echo "Downloading Arduino UNO Media Carrier STEP model..."
  curl -fL -o "$MC_ZIP" "https://docs.arduino.cc/resources/models/ASX00083-step.zip"
fi
unzip -oq "$MC_ZIP" -d "$ROOT/reference/media-carrier/step"

if [[ ! -f "$ROOT/cad/MediaCarrier_board.FCStd" ]]; then
  if [[ -x "$FREECADCMD" ]]; then
    echo "Building cad/MediaCarrier_board.FCStd..."
    UNOQ_STEP="$ROOT/reference/media-carrier/step/ASX00083-step.step" \
    UNOQ_OUT="$ROOT/cad/MediaCarrier_board.FCStd" \
    UNOQ_LABEL="Arduino UNO Media Carrier" \
      "$FREECADCMD" "$ROOT/scripts/build_unoq_board.py"
  else
    echo "freecadcmd not found; set FREECADCMD and re-run to build cad/MediaCarrier_board.FCStd" >&2
    exit 1
  fi
fi

echo "Done."
