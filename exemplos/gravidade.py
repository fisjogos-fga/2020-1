import pyxel
import random
from math import sqrt


class Body:
    def __init__(self, pos=(0, 0), vel=(0, 0), mass=1.0, color=0):
        self.position_x, self.position_y = pos
        self.velocity_x, self.velocity_y = vel
        self.mass = mass
        self.color = color

        self.force_x = 0.0
        self.force_y = 0.0

    def apply_force(self, fx, fy):
        self.force_x += fx
        self.force_y += fy        

    def update_velocity(self, dt):
        acc_x = self.force_x / self.mass
        acc_y = self.force_y / self.mass
        
        self.velocity_x += acc_x * dt
        self.velocity_y += acc_y * dt

        self.force_x = self.force_y = 0.0

    def update_position(self, dt):
        self.position_x += self.velocity_x * dt
        self.position_y += self.velocity_y * dt

    def draw(self):
        pyxel.pset(self.position_x, self.position_y, self.color)


class Circle(Body):
    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)
    
    def draw(self):
        pyxel.circ(self.position_x, self.position_y, self.radius, self.color)


class Space:
    def __init__(self):
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def add_circle(self, *args, **kwargs):
        circle = Circle(*args, **kwargs)
        self.add_body(circle)
        return circle

    ... # rect, tri, lines, ...

    def update(self, dt):
        for body in self.bodies:
            body.update_velocity(dt)

        for body in self.bodies:
            body.update_position(dt)

    def draw(self):
        for body in self.bodies:
            body.draw()

FPS = 60
dt = 1 / FPS
pyxel.init(180, 120, fps=FPS)

sp = Space()
bodies = [
    sp.add_circle(radius=5, pos=(x, 60), vel=vel, 
                  color=random.randint(1, 15))
    for x, vel in [
        (30, (10, 20)), 
        (90, (-10, -40)), 
        (150, (0, 20)),
        (60, (-20, -30)),
        (120, (20, 30)),
        ]
]

def update():
    for i, body1 in enumerate(bodies):
        for j in range(i + 1, 3):
            body2 = bodies[j]
            dx = body1.position_x - body2.position_x
            dy = body1.position_y - body2.position_y
            r = sqrt(dx**2 + dy**2 + 1e-50)

            # Aqui vocês podem colocar várias outras expressões: isso representa o módulo da força
            cte = 250000
            F = -cte / (r + 50)**2
            Fx = dx / r * F
            Fy = dy / r * F

            body1.apply_force(Fx, Fy)
            body2.apply_force(-Fx, -Fy)

    sp.update(dt)

def draw():
    pyxel.cls(0)
    sp.draw()

pyxel.run(update, draw)
