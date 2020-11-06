from pymunk import Vec2d, Space, Body, Circle, Segment, Poly
import pymunk
import pyxel
import random
from math import pi 


def init_space():
    sp = Space()
    sp.gravity = (0, 50)
    sp.damping = 1.0
    
    floor = Body(body_type=Body.STATIC)
    stick = Body(mass=100, moment=100 * 50**2)
    L = 20
    shapes = [
        Poly(stick, [(-L, -L), (L, -L), (L, L), (0, L + L/2), (-L, L)], radius=3),
        Segment(floor, (1, 179), (239, 179), 1),
        Segment(floor, (1, 1), (239, 1), 1),
        Segment(floor, (1, 1), (1, 179), 1),
        Segment(floor, (239, 1), (239, 179), 1),
    ]
    stick.position = (120, L)
    
    bodies = []
    for _ in range(L):
        r = random.uniform(2, 6)
        mass = pi * r**2
        body = Body(mass=mass, moment=mass * r**2 / 2) 
        circle = Circle(body, r)
        
        x = random.uniform(r, 240 - r)
        y = random.uniform(r, 180 - r)
        body.position = (x, y)
        
        vx = random.uniform(-L, L)
        vy = random.uniform(-L, L)
        body.velocity = (vx, vy)

        bodies.append(body)
        shapes.append(circle)
        circle.color = random.randint(1, 15)

    for shape in shapes:
        shape.elasticity = 1.0

    sp.add(floor, stick, *bodies, *shapes)
    return sp


def update():
    if pyxel.btn(pyxel.KEY_SPACE):
        space.step(1/60)


def draw():
    pyxel.cls(0)

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

space: Space = init_space()
pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
pyxel.run(update, draw)