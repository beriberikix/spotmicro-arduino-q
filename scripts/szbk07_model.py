"""Simplified SZBK07 20 A buck converter, modelled from measurements (no third-party CAD).

Frame: origin at the centre of the four mounting holes, z = 0 on the underside of the PCB, +Y towards the robot's
front (the 2-capacitor end with the input/output terminal block), +X towards the robot's right.

Outline: 60 x 45 x 1.7 mm PCB, Ø3.6 holes at 39 x 53.5 mm (measured), two 45 x 10 x 25 mm finned heatsinks overhanging the long
edges (top 26.7 mm above the board's underside), toroidal coil to 25.9 mm.

    import szbk07_model; shape = szbk07_model.make()
"""

import FreeCAD
import Part

V = FreeCAD.Vector

PCB = (45.0, 60.0, 1.7)
HOLE_D, HOLE_X, HOLE_Y = 3.6, 19.5, 26.75
TOP = PCB[2]


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(x, y, r, z0, z1):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0))


def heatsink(inner_x, side):
    """Base plate against the board edge, 8 fins sticking outwards (side = +1 right, -1 left)."""
    base_t, depth, y0, y1, z1 = 3.0, 10.1, -22.0, 23.0, TOP + 25.0
    x_in, x_base = inner_x, inner_x + side * base_t
    parts = [box(min(x_in, x_base), max(x_in, x_base), y0, y1, TOP, z1)]
    n, fin_t = 8, 1.4
    pitch = (y1 - y0 - fin_t) / (n - 1)
    x_out = inner_x + side * depth
    for i in range(n):
        y = y0 + i * pitch
        parts.append(box(min(x_base, x_out), max(x_base, x_out), y, y + fin_t, TOP, z1))
    return parts


def make():
    w, l, t = PCB
    board = box(-w / 2, w / 2, -l / 2, l / 2, 0, t)
    board = board.cut(Part.makeCompound([cyl(sx * HOLE_X, sy * HOLE_Y, HOLE_D / 2, -1, t + 1)
                                         for sx in (-1, 1) for sy in (-1, 1)]))
    parts = [board]
    parts += heatsink(17.2, 1) + heatsink(-17.2, -1)
    # toroidal coil standing on edge, axis along Y, sitting on the board: top 25.9 mm above the PCB underside (measured)
    coil = Part.makeTorus(8.1, 4.0, V(0.2, 1.0, TOP + 12.1), V(0, 1, 0))
    parts.append(coil)
    # capacitors: two large at the front, three small behind the coil
    parts += [cyl(x, 12.2, 5.6, TOP, TOP + 18.7) for x in (-7.6, 3.7)]
    parts += [cyl(x, -10.8, 4.4, TOP, TOP + 16.0) for x in (-9.8, -0.45, 9.15)]
    # screw terminal blocks (front: 2 ways, rear: 2 ways) with screw recesses
    for (x0, x1, y0, y1), screws in (((-9.0, 7.7, 18.4, 30.0), ((-4.0, 24.0), (3.0, 24.0))),
                                     ((-3.3, 13.4, -29.8, -18.2), ((1.0, -24.0), (9.0, -24.0)))):
        blk = box(x0, x1, y0, y1, TOP, TOP + 12.0)
        blk = blk.cut(Part.makeCompound([cyl(x, y, 2.4, TOP + 7.9, TOP + 13) for x, y in screws]))
        parts.append(blk)
    # power devices clamped to the heatsinks, diodes and small parts
    parts += [box(12.5, 17.2, 7.0, 17.0, TOP, TOP + 18.5), box(-17.2, -13.2, 7.0, 17.0, TOP, TOP + 18.5)]
    parts += [box(-15.0, -5.0, -29.0, -24.5, TOP, TOP + 10.5), box(-15.0, -5.0, -23.7, -19.2, TOP, TOP + 10.5)]
    parts += [box(10.0, 13.7, 20.6, 24.2, TOP, TOP + 7.0), box(-14.3, -10.6, 20.4, 27.9, TOP, TOP + 6.8)]
    return Part.makeCompound(parts)
