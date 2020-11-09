from pymunk import Vec2d, Space, Body, Circle, Segment, Poly
import pymunk
import pyxel
import random
from math import pi, sqrt

N = 200
RADIUS = 1.5
SPEED = 50
MASS = 1.0
MOMENT = 1.0
force_pos_x = 90
force_pos_y = 90


def init_space():
    sp = Space()
    
    h = 20 * sqrt(2)
    player = Body(mass=1, moment=400)
    shape = Poly(player, [(-20, -h/3), (20, -h/3), (0, 2/3*h)])
    player.position = (90, 90)
    shape.elasticity = 1.0
    shape.color = pyxel.COLOR_YELLOW

    line = Body(body_type=Body.STATIC)
    lines = [
        Segment(line, (0, 1), (240, 1), 2),
        Segment(line, (0, 179), (240, 179), 2),
        Segment(line, (1, 0), (1, 180), 2),
        Segment(line, (239, 0), (239, 180), 2),
    ]
    for line in lines:
        line.elasticity = 1.0
        line.color = pyxel.COLOR_PEACH

    sp.add(player, shape, *lines)
    sp.player = player
    return sp


def update():
    global force_pos_x, force_pos_y

    delta = 1
    if pyxel.btn(pyxel.KEY_UP):
        force_pos_y -= delta
    elif pyxel.btn(pyxel.KEY_DOWN):
        force_pos_y += delta
    if pyxel.btn(pyxel.KEY_LEFT):
        force_pos_x -= delta
    elif pyxel.btn(pyxel.KEY_RIGHT):
        force_pos_x += delta

    if pyxel.btn(pyxel.KEY_SPACE):
        force = (0, -100)
    else:
        force = (0, 0)

    force_pos = (force_pos_x, force_pos_y)
    space.player.apply_force_at_world_point(force, force_pos)

    space.step(1/60)


def draw():
    pyxel.cls(pyxel.COLOR_NAVY 
              if pyxel.btn(pyxel.KEY_SPACE)
              else pyxel.COLOR_PURPLE)

    pyxel.line(0, force_pos_y, pyxel.width, force_pos_y, pyxel.COLOR_WHITE)
    pyxel.line(force_pos_x, 0, force_pos_x, pyxel.height, pyxel.COLOR_WHITE)

    for body in space.bodies:
        for shape in body.shapes:
            if isinstance(shape, Circle):
                x, y = body.position + shape.offset
                color = getattr(shape, 'color', pyxel.COLOR_WHITE)
                pyxel.circ(x, y, shape.radius, color)
            elif isinstance(shape, Segment):
                ax, ay = body.position + shape.a
                bx, by = body.position + shape.b
                pyxel.line(ax, ay, bx, by, pyxel.COLOR_RED)
            elif isinstance(shape, Poly):
                color = getattr(shape, 'color', pyxel.COLOR_WHITE)
                for tri in group_tri(shape.get_vertices()):
                    coords = []
                    for v in tri:
                        x,y = v.rotated(body.angle) + body.position
                        coords.extend((x, y))
                    pyxel.tri(*coords, color)

    obj = space.player
    pyxel.circ(*obj.position, 2, pyxel.COLOR_RED)
    pyxel.text(0, 160, f"angle: {obj.angle:.2f}", pyxel.COLOR_WHITE)
    pyxel.text(0, 170, f"omega: {obj.angular_velocity:.2f}", pyxel.COLOR_WHITE)

def group_tri(seq):
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z

pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
space: Space = init_space()
pyxel.run(update, draw)