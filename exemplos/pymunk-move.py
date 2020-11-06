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


def init_space():
    sp = Space()
    
    player = Body(mass=1, moment=1)
    shape = Circle(player, 10)
    player.position = (20, 90)
    player.velocity = (5, 0)
    shape.color = pyxel.COLOR_YELLOW

    line = Body(body_type=Body.STATIC)
    line_shape = Segment(line, (0, 1), (240, 1), 2)
    line_shape.color = pyxel.COLOR_RED 

    sp.add(player, shape, line, line_shape)
    sp.player = player
    return sp


def update():
    if pyxel.btn(pyxel.KEY_UP):
        space.player.apply_force_at_local_point((0, -1000), (0, 0))
    elif pyxel.btn(pyxel.KEY_DOWN):
        space.player.apply_force_at_local_point((0, +1000), (0, 0))
    
    force = space.player.velocity * (-10)
    space.player.apply_force_at_local_point(force, (0, 0))

    space.step(1/60)


def draw():
    degrade(pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_NAVY)

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


def group_tri(seq):
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z


def degrade(c1, c2):
    pyxel.cls(c1)

    for y in range(pyxel.height):
        prob = y / pyxel.height
        for x in range(pyxel.width):
            if random.random() < prob:
                pyxel.pset(x, y, c2)


pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
space: Space = init_space()
pyxel.run(update, draw)