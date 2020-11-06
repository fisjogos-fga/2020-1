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


def random_velocity():
    vx = random.uniform(-SPEED, SPEED)
    vy = random.uniform(-SPEED, SPEED)
    return Vec2d(vx, vy)


def random_position():
    x = random.uniform(RADIUS, pyxel.width - RADIUS)
    y = random.uniform(RADIUS + 21, pyxel.height - RADIUS)
    return Vec2d(x, y)


def init_space():
    sp = Space()
    
    floor = Body(body_type=Body.STATIC)

    sp.add(
        floor,
        Segment(floor, (1, 179), (239, 179), 1),
        Segment(floor, (1, 1), (239, 1), 1),
        Segment(floor, (1, 1), (1, 179), 1),
        Segment(floor, (239, 1), (239, 179), 1),
    )

    weight = Body(mass=100, moment=float('inf'))
    sp.add(
        weight, 
        Poly(weight, [(2, 2), (2, 22), (238, 22), (238, 2)])
    )

    for shape in sp.shapes:
        shape.elasticity = 1
    
    for _ in range(N):
        body = Body(mass=MASS, moment=MOMENT) 
        circle = Circle(body, RADIUS)
        
        body.position = random_position()
        body.velocity = random_velocity()
        circle.elasticity = 1

        sp.add(circle, body)

    sp.weight = weight
    return sp


def update():
    if pyxel.btn(pyxel.KEY_SPACE):
        space.step(1/60)

        space.weight.apply_force_at_local_point((0, space.weight.mass * 50), (0, 0))
        moment = Vec2d(0, 0)
        energy = 0

        for body in space.bodies:
            if body.body_type == body.DYNAMIC:
                moment += body.mass * body.velocity
                energy += (body.mass*body.velocity.length**2)/2 
                if not body.moment == float('inf'):
                    energy += (body.moment*body.angular_velocity**2)/2

        print(energy)
        print(moment)


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

pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
space: Space = init_space()
pyxel.run(update, draw)