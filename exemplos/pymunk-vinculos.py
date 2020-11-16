from pymunk import Vec2d, Space, Body, Circle, Segment, Poly, constraint
import re
import string
import pymunk
import pyxel
import random
from math import pi, sqrt


def make_pivot_chain(space, a, b, n, mass=1):
    a, b = map(Vec2d, (a, b))
    delta = (b - a) / n
    L = delta.length
    pos = a
    
    objs = []
    prev_body = None
    for _ in range(n):
        final = pos + delta
        body = Body(mass=mass / n, moment=(mass / n) * L**2 / 2)
        shape = Segment(body, -delta / 2, delta / 2, 2)
        body.position = pos + delta / 2
        objs.append(body)
        
        if prev_body is not None:
           joint = constraint.PivotJoint(body, prev_body, pos)
           joint.collide_bodies = False
           space.add(joint)
        space.add(body, shape)
        pos = final
        prev_body = body
    
    return objs

def init_space():
    sp = Space()
    sp.gravity = (0, 50)

    chain = make_pivot_chain(sp, (0, 0), (240, 30), 30)
    sp.add(constraint.PivotJoint(chain[0], sp.static_body, chain[0].position))

    # Cria quadrado    
    L = 25
    player = Body(mass=1, moment=100)
    shape = Poly(player, [(-L, -L), (L, -L), (L, L), (-L, L)])
    player.position = (90, 60)
    player.velocity = (-25, 25)
    shape.elasticity = 1.0
    shape.color = pyxel.COLOR_RED
    shape.collision_type = 42

    ball = Body(mass=1, moment=200)
    ball_shape = Circle(ball, 20)
    ball.position = (player.position.x, 130)
    ball_shape.elasticity = 1.0
    shape.color = pyxel.COLOR_NAVY
    ball_shape.collision_type = 42

    joint1 = constraint.DampedSpring(player, ball, (0, 0), (20, 0), 20, 3, 0.5)
    joint2 = constraint.PivotJoint(sp.static_body, player, (65, 35))
    joint1.collide_bodies = False
    sp.add(joint1, joint2)

    body2 = Body(1, 100)
    sp.add(body2)
    sp.add(Poly(body2, [(-3, 3), (3, 3), (3, -3), (-3, -3)]))
    body2.position = 220, 50
    sp.add(constraint.DampedRotarySpring(body2, ball, 0, 2, 1))
    sp.body2 = body2

    # Cria margens
    line = Body(body_type=Body.STATIC)
    e = 0
    lines = [
        Segment(line, (-e, -e), (240 + e, -e), 2),
        Segment(line, (-e, 180 + e), (240 + e, 180 + e), 2),
        Segment(line, (-e, -e), (-e, 180 + e), 2),
        Segment(line, (240 + e, -e), (240 + e, 180 + e), 2),
    ]
    for line in lines:
        line.elasticity = 1.0
    lines = []

    # Adiciona elementos ao espaço
    sp.add(player, shape, ball, ball_shape, *lines)
    sp.player = player

    #handler = sp.add_collision_handler(42, 42)
    #handler.begin = lambda *args: False
    return sp


def update():
    p = space.player

    # Modifica velocidade
    factor = 1.05
    if pyxel.btn(pyxel.KEY_UP):
        p.velocity = factor * p.velocity
    if pyxel.btn(pyxel.KEY_DOWN):
        p.velocity = p.velocity / factor

    b2 = space.body2
    b2.apply_force_at_world_point(-space.gravity * b2.mass, b2.position)
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
                ax, ay = body.local_to_world(shape.a)
                bx, by = body.local_to_world(shape.b)
                pyxel.line(ax, ay, bx, by, pyxel.COLOR_RED)
            elif isinstance(shape, Poly):
                color = getattr(shape, 'color', pyxel.COLOR_WHITE)
                for tri in group_tri(shape.get_vertices()):
                    coords = []
                    for v in tri:
                        x,y = v.rotated(body.angle) + body.position
                        coords.extend((x, y))
                    pyxel.tri(*coords, color)

    for cons in space.constraints:
        if isinstance(cons, (constraint.PivotJoint,
                             constraint.GrooveJoint)):
            x, y = cons.b.local_to_world(cons.anchor_b)
            pyxel.circ(x, y, 2, pyxel.COLOR_YELLOW)
        if isinstance(cons, (constraint.PinJoint, 
                             constraint.SlideJoint,
                             constraint.DampedSpring)):
            xa, ya = cons.a.local_to_world(cons.anchor_a)
            xb, yb = cons.b.local_to_world(cons.anchor_b)
            pyxel.line(xa, ya, xb, yb, pyxel.COLOR_YELLOW)
            pyxel.circ(xa, ya, 2, pyxel.COLOR_YELLOW)
            pyxel.circ(xb, yb, 2, pyxel.COLOR_YELLOW)

def group_tri(seq):
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z


pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
space: Space = init_space()
pyxel.run(update, draw)