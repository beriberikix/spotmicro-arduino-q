# servo_tool: web page for the build guide's servo steps.
#
# Serves assets/ (http://<board>:7000) and passes the page's requests to the sketch over the Bridge:
#   set {ch, deg}  -> set_angle(ch, deg)
#   off {ch}       -> set_off(ch), ch -1 = every output
#   test {ch}      -> test_sweep(ch)
# It also keeps a little state the guide steps need (which straight-down angle worked for the hips on each side)
# in data/servo_tool.json, so the check is only needed once per side.
#
# The Serial Monitor commands in the sketch keep working alongside the page.
import json
import os
import threading

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App, Bridge, Logger

logger = Logger("servo_tool")
ui = WebUI()

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
STATE_FILE = os.path.join(DATA, "servo_tool.json")
_lock = threading.Lock()


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    try:
        os.makedirs(DATA, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=1)
    except OSError as e:
        logger.warning(f"could not save state: {e}")


def channel(data):
    ch = int(data.get("ch", -1))
    if not -1 <= ch <= 11:
        raise ValueError("channel must be 0-11")
    return ch


def bridge(fn, *args):
    try:
        Bridge.call(fn, *args)
        return {"ok": True}
    except Exception as e:  # the sketch isn't running, or the call timed out
        logger.warning(f"{fn}{args} failed: {e}")
        return {"ok": False, "error": str(e)}


def on_set(sid, data):
    ch = channel(data)
    deg = max(0, min(180, int(data["deg"])))
    if ch < 0:
        return {"ok": False, "error": "pick a channel"}
    return bridge("set_angle", ch, deg) | {"ch": ch, "deg": deg}


def on_off(sid, data):
    return bridge("set_off", channel(data or {}))


def on_test(sid, data):
    ch = channel(data)
    if ch < 0:
        return {"ok": False, "error": "pick a channel"}
    return bridge("test_sweep", ch)


def on_state_get(sid, data):
    with _lock:
        return load_state()


def on_state_set(sid, data):
    with _lock:
        state = load_state()
        state[str(data["key"])] = data["value"]
        save_state(state)
        return state


ui.on_message("set", on_set)
ui.on_message("off", on_off)
ui.on_message("test", on_test)
ui.on_message("state_get", on_state_get)
ui.on_message("state_set", on_state_set)

App.run()
