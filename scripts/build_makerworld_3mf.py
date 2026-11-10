#!/usr/bin/env python3
"""Build the Bambu Studio project (3MF) for MakerWorld from stl/.

Runs the Bambu Studio command line: loads every part with its quantity and filament, places
the parts on the plates defined below, auto-orients each part, auto-arranges each plate on its
own, applies per-part print settings, and slices every plate.

    python3 scripts/build_makerworld_3mf.py            # writes makerworld/SpotUnoQ_P1S.3mf
    python3 scripts/build_makerworld_3mf.py --no-orient  # keep each STL's own orientation

Printer: Bambu Lab P1S, 0.4 mm nozzle, 0.20 mm Standard. Filaments: 1 Bambu PLA Basic black,
2 Bambu PLA Basic white, 3 Bambu TPU 95A HF. Set BAMBU_STUDIO to use another install.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP = os.environ.get("BAMBU_STUDIO", "/Applications/BambuStudio.app")
EXE = os.path.join(APP, "Contents/MacOS/BambuStudio")
PROFILES = os.path.join(APP, "Contents/Resources/profiles/BBL")
OUT = os.path.join(ROOT, "makerworld", "SpotUnoQ_P1S.3mf")

MACHINE = "Bambu Lab P1S 0.4 nozzle"
PROCESS = "0.20mm Standard @BBL X1C"  # Bambu's 0.20 mm Standard process; lists the P1S as compatible
FILAMENTS = [  # (preset, colour)
    ("Bambu PLA Basic @BBL P1S 0.4 nozzle", "#000000"),
    ("Bambu PLA Basic @BBL P1S 0.4 nozzle", "#FFFFFF"),
    ("Bambu TPU 95A HF @BBL P1S", "#808080"),
]
BLACK, WHITE, TPU = 1, 2, 3
INFILL = "20%"  # Kubina's parts list: 20% for parts
BED = "Textured PEI Plate"  # the plate the P1S ships with
SOLID = {"sparse_infill_density": "100%"}  # and 100% for the covers
STRUCTURAL = {"wall_loops": "3"}  # load-bearing plates get a third wall

# (plate name, plate-wide print overrides, filament, [(stl path relative to stl/, copies, print overrides)])
PLATES = [
    ("Chassis plates and rails", STRUCTURAL, BLACK, [
        ("chassis/Inner_Shoulder.stl", 2, {}),
        ("chassis/Outer_Shoulder.stl", 2, {}),
        ("chassis/Chassis_Side.stl", 2, {}),
    ]),
    ("Electronics plate and chassis blocks", STRUCTURAL, BLACK, [
        ("electronics/UnoQ_Mountingplate.stl", 1, {}),
        ("chassis/Top_Shoulder.stl", 2, {}),
        ("chassis/Bottom_Shoulder.stl", 2, {}),
        ("chassis/LiPo_Mountingbracket_Front.stl", 1, {}),
        ("chassis/LiPo_Mountingbracket_Middle.stl", 1, {}),
        ("chassis/LiPo_Mountingbracket_Rear.stl", 1, {}),
    ]),
    ("Shoulder joints and head mounts", STRUCTURAL, BLACK, [
        ("shoulders/Shoulder_Joint_Servomount_extended_BB.stl", 2, {}),
        ("shoulders/Shoulder_Joint_Servomount_extended_BB_mirrored.stl", 2, {}),
        ("shoulders/Shoulder_Joint_Servo_Cap_Extended.stl", 4, {}),
        ("shoulders/Shoulder_Joint_Ball_Bearing_Pin.stl", 8, {}),
        ("shoulders/Shoulder_Joint_Ball_Bearing_Pin_M3x8.stl", 4, {}),
        ("head/Sensormount.stl", 1, {}),
        ("head/Cameramount_ESP32_CAM.stl", 1, {}),
        ("head/Cameramount_ESP32_CAM_Counterpiece.stl", 1, {}),
    ]),
    ("Upper leg frames", STRUCTURAL, BLACK, [
        ("legs/Limb_Ball_Bearing_Mount_long_v4.stl", 2, {}),
        ("legs/Limb_Ball_Bearing_Mount_long_v4_mirrored.stl", 2, {}),
        ("legs/Limb_Servohorn_Mount_long_v4.stl", 2, {}),
        ("legs/Limb_Servohorn_Mount_long_v4_mirrored.stl", 2, {}),
    ]),
    ("Lower legs", STRUCTURAL, BLACK, [
        ("legs/Wrist.stl", 2, {}),
        ("legs/Wrist_mirrored.stl", 2, {}),
        ("legs/Wrist_Counterpart.stl", 2, {}),
        ("legs/Wrist_Counterpart_mirrored.stl", 2, {}),
    ]),
    ("Upper leg top shells", STRUCTURAL, WHITE, [
        ("legs/Limb_Top_Shell_with_BB_hole.stl", 2, {}),
        ("legs/Limb_Top_Shell_with_BB_hole_mirrored.stl", 2, {}),
    ]),
    ("Upper leg bottom shells and shoulder covers", STRUCTURAL, WHITE, [
        ("legs/Limb_Bottom_Shell.stl", 2, {}),
        ("legs/Limb_Bottom_Shell_mirrored.stl", 2, {}),
        ("shoulders/Shoulder_Cover.stl", 4, {}),
    ]),
    ("Body covers", {}, WHITE, [
        ("hull/Top_Cover_Split_Front.stl", 1, SOLID),
        ("hull/Top_Cover_Split_Rear_with_OLED.stl", 1, SOLID),
        ("hull/Bottom_Cover_Split_Front.stl", 1, SOLID),
        ("hull/Bottom_Cover_Split_Rear.stl", 1, SOLID),
    ]),
    ("Head and rear covers", {}, WHITE, [
        ("head/Front_Cover_Optimized.stl", 1, SOLID),
        ("hull/Rear_Cover_Shell_Long.stl", 1, SOLID),
        ("hull/Rear_Cover_Plate.stl", 1, SOLID),
    ]),
    ("Feet (TPU)", {}, TPU, [
        ("legs/Foot_Tip.stl", 4, {}),
    ]),
]


def preset_index():
    index = {}
    for cat in ("machine", "process", "filament"):
        for f in glob.glob(os.path.join(PROFILES, cat, "*.json")):
            try:
                d = json.load(open(f))
            except ValueError:
                continue
            if "name" in d:
                index[(cat, d["name"])] = f
    return index


def resolve(index, cat, name):
    """Flatten a Bambu system preset; the command line does not follow "inherits" itself."""
    d = json.load(open(index[(cat, name)]))
    out = {}
    if d.get("inherits"):
        out.update(resolve(index, cat, d["inherits"]))
    for inc in d.get("include") or []:
        out.update(resolve(index, cat, inc))
    out.update({k: v for k, v in d.items() if k not in ("inherits", "include")})
    out["from"] = "system"
    return out


def write_presets(tmp):
    index = preset_index()
    machine = resolve(index, "machine", MACHINE)
    process = resolve(index, "process", PROCESS)
    process["sparse_infill_density"] = INFILL
    process["curr_bed_type"] = BED
    paths = [os.path.join(tmp, "machine.json"), os.path.join(tmp, "process.json")]
    json.dump(machine, open(paths[0], "w"))
    json.dump(process, open(paths[1], "w"))
    fils = []
    for i, (name, colour) in enumerate(FILAMENTS):
        f = resolve(index, "filament", name)
        f["filament_colour"] = [colour]
        f["default_filament_colour"] = [colour]
        p = os.path.join(tmp, f"filament_{i + 1}.json")
        json.dump(f, open(p, "w"))
        fils.append(p)
    return paths, fils


def write_assemble_list(tmp):
    plates, names, n = [], {}, 0
    for plate_name, plate_params, fil, parts in PLATES:
        objs = []
        for rel, copies, part_params in parts:
            params = {**plate_params, **part_params}
            path = os.path.join(ROOT, "stl", rel)
            if not os.path.exists(path):
                sys.exit(f"missing {path}; run scripts/export_stls.py")
            base = os.path.splitext(os.path.basename(rel))[0]
            for c in range(copies):
                n += 1  # one assemble group per copy keeps every copy a separate object
                names[f"assemble_{n}"] = f"{base}_{c + 1}" if copies > 1 else base
                objs.append({"path": path, "count": 1, "filaments": [fil], "assemble_index": [n],
                             "subtype": "normal_part", "print_params": params,
                             "pos_x": [128], "pos_y": [128], "pos_z": [0]})
        plates.append({"plate_name": plate_name, "need_arrange": True, "plate_params": {}, "objects": objs})
    path = os.path.join(tmp, "assemble_list.json")
    json.dump({"plates": plates}, open(path, "w"), indent=1)
    return path, names


PART_KEYS = ("name", "matrix", "extruder", "source_file", "source_object_id", "source_volume_id",
             "source_offset_x", "source_offset_y", "source_offset_z")


def object_settings(text):
    """The assemble list puts a part's filament and print overrides on the mesh inside each object.
    The command-line slicer honours them there, but the Bambu Studio app shows and edits a
    single-part object's settings at object level, and colours the object by its own extruder
    (otherwise filament 1). Move the overrides up to the object and copy the extruder, as
    Bambu Studio's own projects do."""
    def fix(m):
        head, body = m.group(1), m.group(2)
        obj, sep, parts = body.partition("<part")
        if not sep:
            return m.group(0)
        meta = re.findall(r'\n\s*<metadata key="([^"]+)" value="([^"]*)"/>', parts.split("<mesh_stat", 1)[0])
        moved = [(k, v) for k, v in meta if k not in PART_KEYS]
        ext = [v for k, v in meta if k == "extruder"]
        add = ([("extruder", ext[0])] if ext and 'key="extruder"' not in obj else []) + moved
        if not add:
            return m.group(0)
        for k, v in moved:
            parts = parts.replace(f'<metadata key="{k}" value="{v}"/>', "", 1)
        oname = re.search(r'<metadata key="name" value="([^"]*)"/>', obj)
        if oname:
            parts = re.sub(r'<metadata key="name" value="[^"]*"/>', f'<metadata key="name" value="{oname.group(1)}"/>', parts, count=1)
        lines = "".join(f'\n    <metadata key="{k}" value="{v}"/>' for k, v in add)
        obj = re.sub(r'(<metadata key="name" value="[^"]*"/>)', lambda n: n.group(1) + lines, obj, count=1)
        parts = re.sub(r"\n\s*\n", "\n", parts)
        return head + obj + sep + parts + "</object>"
    return re.sub(r'(<object id="\d+">)(.*?)</object>', fix, text, flags=re.S)


def project_settings(text):
    """Bambu Studio reloads every value of a named system preset unless the key is listed in
    different_settings_to_system (index 0 is the process preset), so record our process change."""
    d = json.loads(text)
    diffs = d.get("different_settings_to_system") or [""] * (len(FILAMENTS) + 2)
    keys = [k for k in diffs[0].split(";") if k]
    if "sparse_infill_density" not in keys:
        keys.append("sparse_infill_density")
    diffs[0] = ";".join(sorted(keys))
    d["different_settings_to_system"] = diffs
    return json.dumps(d, indent=4)


def rename_objects(path, names):
    """Bambu names each assembled object assemble_N; give it the part's name instead."""
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "Metadata/project_settings.config":
                data = project_settings(data.decode("utf-8")).encode("utf-8")
            elif item.filename in ("Metadata/model_settings.config", "Metadata/slice_info.config", "3D/3dmodel.model"):
                text = data.decode("utf-8")
                text = re.sub(r'(?<=")assemble_\d+(?=")', lambda m: names.get(m.group(0), m.group(0)), text)
                if item.filename == "Metadata/model_settings.config":
                    text = object_settings(text)
                data = text.encode("utf-8")
            zout.writestr(item, data)
    os.replace(tmp, path)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        settings, fils = write_presets(tmp)
        alist, names = write_assemble_list(tmp)
        outdir = os.path.join(tmp, "out")
        cmd = [EXE, "--debug", "2", "--load-settings", ";".join(settings), "--load-filaments", ";".join(fils),
               "--load-assemble-list", alist, "--orient", "0" if "--no-orient" in sys.argv else "1", "--arrange", "1", "--ensure-on-bed", "--slice", "0",
               "--outputdir", outdir, "--export-3mf", os.path.basename(OUT)]
        log = subprocess.run(cmd, capture_output=True, text=True)
        result_path = os.path.join(outdir, "result.json")
        result = json.load(open(result_path)) if os.path.exists(result_path) else {}
        if log.returncode != 0 or result.get("return_code", 1) != 0:
            print(log.stdout[-3000:], log.stderr[-3000:])
            sys.exit(f"Bambu Studio failed ({log.returncode}): {result.get('error_string')}")
        shutil.copy(os.path.join(outdir, os.path.basename(OUT)), OUT)
        json.dump(result, open(os.path.join(os.path.dirname(OUT), "slice_result.json"), "w"), indent=1)
    rename_objects(OUT, names)
    total_h = total_g = 0
    problems = []
    first = 1
    for (plate_name, _, fil, parts), p in zip(PLATES, result["sliced_plates"]):
        h = p["main_predication"] / 3600
        g = sum(f["total_used_g"] for f in p["filaments"])
        total_h += h
        total_g += g
        warn = re.sub(r"assemble_\d+", lambda m: names.get(m.group(0), m.group(0)), p.get("warning_message", ""))
        expected = sum(c for _, c, _ in parts)
        sliced = {o["name"] for o in p["objects"]}
        missing = [names[f"assemble_{i}"] for i in range(first, first + expected) if f"assemble_{i}" not in sliced]
        first += expected
        print(f"plate {p['id']:2d}  {plate_name:45s} {len(p['objects']):3d}/{expected:<3d} parts  {h:5.1f} h  {g:6.0f} g  {warn}")
        if missing:
            problems.append(f"plate {p['id']} did not slice: {', '.join(missing)}")
        if warn:
            problems.append(f"plate {p['id']}: {warn}")
    print(f"total {total_h:.1f} h, {total_g:.0f} g -> {os.path.relpath(OUT, ROOT)}")
    if problems:
        sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))


main()
