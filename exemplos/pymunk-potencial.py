from pymunk import Vec2d, Space, Body, Circle, Segment, Poly
import re
import string
import pymunk
import pyxel
import random
import math
from math import pi, sqrt
from input_widget import Input

POT_EXPR = "(x ** 2 + y ** 2) * 0.5"
FUNCTIONS = vars(math)

def U(x, y): 
    return eval(POT_EXPR, {"x": x, "y": y, "r": sqrt(x**2 + y**2)}, FUNCTIONS)


def init_space():
    sp = Space()

    # Cria quadrado    
    L = 5
    player = Body(mass=1, moment=100)
    shape = Poly(player, [(-L, -L), (L, -L), (L, L), (-L, L)])
    player.position = (50, 40)
    player.velocity = (-25, 25)
    shape.elasticity = 1.0
    shape.color = pyxel.COLOR_RED

    # Cria margens
    line = Body(body_type=Body.STATIC)
    lines = [
        Segment(line, (-30, -30), (270, -30), 2),
        Segment(line, (-30, 210), (270, 210), 2),
        Segment(line, (-30, -30), (-30, 210), 2),
        Segment(line, (270, -30), (270, 210), 2),
    ]
    for line in lines:
        line.elasticity = 1.0

    # Adiciona elementos ao espaço
    sp.add(player, shape, *lines)
    sp.player = player
    return sp


def update():
    inpt.update_widgets()
    p = space.player

    # Modifica velocidade
    factor = 1.05
    if pyxel.btn(pyxel.KEY_UP):
        p.velocity = factor * p.velocity
    if pyxel.btn(pyxel.KEY_DOWN):
        p.velocity = p.velocity / factor

    # Aplica força
    x, y = p.position - (120, 90)
    y *= -1
    try:
        e = 0.01
        Fx = -(U(x + e, y) - U(x, y)) / e
        Fy = -(U(x, y + e) - U(x, y)) / e
    except Exception as ex:
        print("Error:", ex)
    else:
        space.player.apply_force_at_world_point((Fx, -Fy), space.player.position)
    
    space.step(1/60)


def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    pyxel.line(0, 90, 240, 90, pyxel.COLOR_PEACH) 
    pyxel.line(120, 0, 120, 180, pyxel.COLOR_PEACH) 

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

    pyxel.text(5, 6, "U(x, y) =", pyxel.COLOR_WHITE)
    inpt.draw_widgets()
    
    # Energia
    obj = space.player
    K = obj.kinetic_energy
    x, y = obj.position - (120, 90)
    y *= -1
    K = obj.mass * obj.velocity.length**2 / 2
    
    pyxel.text(5, 150, f"K: {K:5.1f}", pyxel.COLOR_WHITE)
    pyxel.text(5, 160, f"U: {U(x, y):5.1f}", pyxel.COLOR_WHITE)
    pyxel.text(5, 170, f"E: {K + U(x, y):5.1f}", pyxel.COLOR_WHITE)


def group_tri(seq):
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z


def set_potential(value):
    global POT_EXPR
    POT_EXPR = value


inpt = Input(
    None, pyxel.FONT_WIDTH * 10 + 5, 5, 45, POT_EXPR, 
    callback=set_potential,
    text_transform=str.lower,
)

pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
space: Space = init_space()
pyxel.run(update, draw)