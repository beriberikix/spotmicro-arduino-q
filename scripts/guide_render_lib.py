# -*- coding: utf-8 -*-
"""Helpers for rendering assembly-guide images from cad/SpotUnoQ.FCStd in the FreeCAD GUI.

Used by scripts/render_guide.FCMacro. Run inside the FreeCAD GUI: FreeCAD's off-screen image
export needs a 3D view.
"""
import math
import os
import re
import shutil
import subprocess
import tempfile

import FreeCAD
import FreeCADGui
from FreeCAD import Vector as V
from pivy import coin

GROUPS = {
    "base": "Spot_Base",
    "front_legs": "Front_Legs_and_Shoulder_flat",
    "rear_legs": "Rear_Legs_and_Shoulder_flat",
    "robjk": "Reinforced_Shoulders_robjk",
    "head": "Head_DualCam",
    "electronics": "Electronics_UnoQ",
}
HARDWARE = re.compile(r"(Nut|M2x|M3x|Dampener|Servohorn .* M3x8)", re.I)

# Colours (r, g, b in 0..1)
C_NEW = (0.96, 0.55, 0.12)       # parts added in this step
C_PRINT = (0.85, 0.86, 0.88)      # printed parts already in place
C_SERVO = (0.16, 0.18, 0.22)
C_STEEL = (0.55, 0.57, 0.60)
C_HORN = (0.70, 0.72, 0.76)
C_PCB = (0.10, 0.45, 0.30)


def _leaves(group, out, path):
    for o in group.Group:
        if o.TypeId == "App::Part":
            _leaves(o, out, path + [o.Name])
        elif o.TypeId in ("App::Link", "Part::Feature", "Mesh::Feature"):
            out.append((o, path))
    return out


class Scene:
    def __init__(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.doc = FreeCAD.getDocument(name) if name in FreeCAD.listDocuments() else FreeCAD.openDocument(path)
        FreeCAD.setActiveDocument(self.doc.Name)
        self.gdoc = FreeCADGui.getDocument(self.doc.Name)
        FreeCADGui.ActiveDocument = self.gdoc
        self.view = self.gdoc.ActiveView
        self.items = []
        for top in self.doc.Objects:
            if top.TypeId == "App::Part" and not [p for p in top.InList if p.TypeId == "App::Part"]:
                _leaves(top, self.items, [top.Name])
        self.group_of = {o.Name: set(path) for o, path in self.items}
        self.objs = [o for o, _ in self.items]
        self.saved_vis = {o.Name: o.Visibility for o in self.objs}
        self.saved_pl = {o.Name: FreeCAD.Placement(self._pl(o)) for o in self.objs}
        self.saved_mat = {}
        self.parent_rot = {}
        self.centre = {}
        self.bb = {}
        for o in self.objs:
            b = self._bbox(o)
            if b is not None:
                self.bb[o.Name] = b
                self.centre[o.Name] = (b.Center.x, b.Center.y, b.Center.z)

    # ------------------------------------------------------------ geometry
    @staticmethod
    def _pl(o):
        return o.LinkPlacement if o.TypeId == "App::Link" else o.Placement

    @staticmethod
    def _set_pl(o, p):
        if o.TypeId == "App::Link":
            o.LinkPlacement = p
        else:
            o.Placement = p

    @staticmethod
    def _bbox(o):
        try:
            b = (o.Mesh if o.TypeId == "Mesh::Feature" else o.Shape).BoundBox
        except Exception:
            return None
        return None if b.DiagonalLength > 3000 or b.DiagonalLength == 0 else b

    # ------------------------------------------------------------ selection
    def select(self, groups=None, labels=None, exclude=None, box=None, names=None):
        """Objects in the given top-level groups whose label matches `labels` (regex) and
        whose bbox centre lies in `box` ((xmin,xmax),(ymin,ymax),(zmin,zmax), None = open)."""
        out = []
        gnames = [GROUPS.get(g, g) for g in groups] if groups else None
        for o in self.objs:
            if names is not None and o.Name not in names and o.Label not in names:
                continue
            if gnames and not (self.group_of[o.Name] & set(gnames)):
                continue
            if labels and not re.search(labels, o.Label):
                continue
            if exclude and re.search(exclude, o.Label):
                continue
            if box:
                c = self.centre.get(o.Name)
                if c is None:
                    continue
                ok = True
                for i, rng in enumerate(box):
                    if rng is None:
                        continue
                    lo, hi = rng
                    if (lo is not None and c[i] < lo) or (hi is not None and c[i] > hi):
                        ok = False
                if not ok:
                    continue
            out.append(o)
        return out

    # ------------------------------------------------------------ appearance
    def colour(self, o, rgb, transparency=0):
        vo = o.ViewObject
        if vo is None:
            return
        if o.Name not in self.saved_mat:
            self.saved_mat[o.Name] = self._get_mat(o)
        if o.TypeId == "App::Link":
            vo.OverrideMaterial = False
            m = vo.ShapeMaterial
            m.DiffuseColor = rgb
            m.AmbientColor = tuple(c * 0.4 for c in rgb)
            m.SpecularColor = (0.15, 0.15, 0.15)
            m.Shininess = 0.2
            m.Transparency = transparency / 100.0
            vo.ShapeMaterial = m
            vo.OverrideMaterial = True
        else:
            vo.ShapeColor = rgb
            vo.Transparency = transparency

    def _get_mat(self, o):
        vo = o.ViewObject
        if o.TypeId == "App::Link":
            return ("link", vo.OverrideMaterial, vo.ShapeMaterial)
        return ("feat", vo.ShapeColor, vo.Transparency)

    def default_colour(self, o):
        lab = o.Label
        if re.search(r"MG996R|DS3218", lab):
            return C_SERVO
        if re.search(r"Futuba|FSH6", lab):
            return C_HORN
        if HARDWARE.search(lab) or re.search(r"Gear|^L_Body06[234]|Body(19|20|31|33|43|45|46|68|69)\d", lab):
            return C_STEEL
        if re.search(r"UNO|Carrier|1411|SZBK07|Camera Module", lab):
            return C_PCB
        if re.search(r"wire", lab):
            return (0.6, 0.3, 0.1)
        return C_PRINT

    # ------------------------------------------------------------ state
    def reset(self):
        for o in self.objs:
            self._set_pl(o, self.saved_pl[o.Name])
            o.Visibility = self.saved_vis[o.Name]
        for n, m in self.saved_mat.items():
            o = self.doc.getObject(n)
            vo = o.ViewObject
            if m[0] == "link":
                vo.ShapeMaterial = m[2]
                vo.OverrideMaterial = m[1]
            else:
                vo.ShapeColor = m[1]
                vo.Transparency = m[2]
        self.saved_mat = {}

    def show_only(self, objs):
        keep = {o.Name for o in objs}
        for o in self.objs:
            o.Visibility = o.Name in keep
        for o in objs:  # parents must be visible too
            for p in o.InListRecursive:
                if p.TypeId == "App::Part":
                    p.Visibility = True

    def move(self, o, d):
        """Move `o` by the global vector `d` from its saved placement."""
        p = FreeCAD.Placement(self.saved_pl[o.Name])
        rot = self.parent_rot.get(o.Name)
        if rot is None:
            self._set_pl(o, p)
            try:
                parent = o.getGlobalPlacement().multiply(p.inverse())
                rot = parent.Rotation
            except Exception:
                rot = FreeCAD.Rotation()
            self.parent_rot[o.Name] = rot
        p.Base = p.Base + rot.inverted().multVec(V(*d))
        self._set_pl(o, p)

    # ------------------------------------------------------------ camera / output
    def camera(self, direction, up=(0, 0, 1), objs=(), margin=1.08, aspect=4 / 3.0, extra=()):
        """Orthographic camera looking along `direction`, framed on `objs` (current placements)."""
        d = V(*direction).normalize()
        u = V(*up)
        u = (u - d * u.dot(d)).normalize()
        r = d.cross(u)
        pts = []
        for o in objs:
            b = self._bbox(o)
            if b is None:
                continue
            for x in (b.XMin, b.XMax):
                for y in (b.YMin, b.YMax):
                    for z in (b.ZMin, b.ZMax):
                        pts.append(V(x, y, z))
        pts += [V(*p) for p in extra]
        cu = [p.dot(u) for p in pts]
        cr = [p.dot(r) for p in pts]
        cd = [p.dot(d) for p in pts]
        mid = u * ((max(cu) + min(cu)) / 2) + r * ((max(cr) + min(cr)) / 2) + d * ((max(cd) + min(cd)) / 2)
        h = max(max(cu) - min(cu), (max(cr) - min(cr)) / aspect) * margin
        self.view.setCameraType("Orthographic")
        cam = self.view.getCameraNode()
        dist = max(400.0, (max(cd) - min(cd)) * 2 + 200)
        pos = mid - d * dist
        cam.position.setValue(pos.x, pos.y, pos.z)
        # orientation: camera looks down its -Z with +Y up
        m = coin.SbMatrix(r.x, r.y, r.z, 0, u.x, u.y, u.z, 0, -d.x, -d.y, -d.z, 0, 0, 0, 0, 1)
        rot = coin.SbRotation(m)
        cam.orientation.setValue(rot)
        cam.focalDistance.setValue(dist)
        cam.height.setValue(h)
        cam.nearDistance.setValue(1.0)
        cam.farDistance.setValue(dist * 3)

    def snap(self, path, w=1280, h=960, ss=2, bg="White"):
        FreeCADGui.updateGui()
        self.view.redraw()
        FreeCADGui.updateGui()
        tmp = path + ".big.png"
        self.view.saveImage(tmp, w * ss, h * ss, bg)
        _ffmpeg(["-i", tmp, "-vf", f"scale={w}:{h}:flags=lanczos", path])
        os.remove(tmp)


def _ffmpeg(args):
    ff = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    subprocess.run([ff, "-y", "-loglevel", "error", *args], check=True)


def smootherstep(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * x * (x * (x * 6 - 15) + 10)
