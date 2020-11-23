from pymunk import Space, Body, Circle, Poly, Vec2d
from camera import Follow
from world import PyxelWorld, paint
import pyxel
import random
from pymunk.constraint import GrooveJoint, SimpleMotor, DampedSpring, GearJoint
from math import pi, exp
DEGREES = pi / 180


class Wheel(Body):
    def __init__(self, x, y, car, mass=1, radius=8, delta=None):
        super().__init__()
        self.position = car.position + (x, y)
        self.offset = Vec2d(x, y)
        
        self.car = car
        
        self.shape = Circle(self, radius)
        self.shape.mass = mass
        self.shape.visible = True
        self.shape.friction = 0.9 
        
    def init(self, space):
        space.add(self, self.shape)
        self.moment *= 3
        
        # Suspensão
        a, b = self.offset + (0, 8), self.offset - (0, 4)
        joint = GrooveJoint(self.car, self, a, b, (0, 0))
        joint.collide_bodies = False
        space.add(joint)
        
        # Amortecedor
        spring = DampedSpring(self, self.car, 
                             (0, 0), self.offset + (0, 12), 16, 
                             stiffness=30, 
                             damping=3)        
        space.add(spring)


class Car(Body):
    @property
    def rpm(self):
        w = self.motor_wheel.angular_velocity
        return int(abs(300 * w / self.gear_ratios[self.gear]))

    def __init__(self, x, y, mass=1):
        super().__init__()

        self.position = (x, y)
        self.motors = []
        
        self.shape = Poly(self, [(-30, -5), (+40, -5), (+30, +5), (-30, +10)], radius=2)
        self.shape.mass = mass
        self.shape.visible = True
        self.shape.color = pyxel.COLOR_RED
        
        self.front_wheel = Wheel(+25, -6, self, mass=1/10)
        self.back_wheel = Wheel(-20, -6, self, mass=1/10, radius=12)
        self.motor_wheel = self.back_wheel

        self.gear = 0
        self.gear_ratios = [1, 2, 3, 5, 7]

    def init(self, space):
        space.add(self, self.shape)
        
        self.front_wheel.init(space)
        self.back_wheel.init(space)

        # Motor
        m = self.motor = SimpleMotor(self.motor_wheel, self, 0)
        m.max_force = 0.0
        space.add(m)

        # 4 x 4
        rate = self.back_wheel.shape.radius / self.front_wheel.shape.radius
        gear = GearJoint(self.front_wheel, self.back_wheel, 0, rate)
        space.add(gear)

    def accelerate(self):
        x = self.rpm / 2000
        force = 2500 * (0.75 * x * exp(-2 * (x - 1)) + 0.25 * exp(-3 * x))
        ratio = self.gear_ratios[self.gear]
        self.motor.max_force = force / ratio
        self.motor.rate = -100

    def break_(self):
        self.motor.max_force = 500
        self.motor.rate = 0

    def coast(self):
        self.motor.max_force = 0
        self.motor.rate = 0
    
    def gear_up(self):
        self.gear = min(self.gear + 1, 4)

    def gear_down(self):
        self.gear = max(self.gear - 1, 0)


class VehicleWorld(PyxelWorld):
    def car(self, x, y, mass=1):
        car = Car(x, y, mass=1)
        car.init(self)
        return car

    def ground(self, x=0, y=0, n=100, angle=(-20, 20), step=40, radius=2, bump_prob=0.2):
        v = Vec2d(x, y) 
        L = [v + (-140, 280), v + (-70, 70), v]
        for _ in range(n):
            step_ = random.uniform(step / 2, step * 2)
            theta_ = random.uniform(*angle) * DEGREES
            delta_ = Vec2d(step, 0).rotated(theta_)
            v = v + delta_
            L.append(v)

            if random.random() < bump_prob:
                thetas = [5 * abs(random.uniform(*angle)) * DEGREES for a in (-1, 1)]
                steps = [random.uniform(step / 7, step / 4) for _ in (-1, 1)] 
                for s, t in zip(thetas, steps):
                    v = v + Vec2d(s, 0).rotated(t)
                    L.append(v)

        n_circ = 16
        size = 70
        for a in range(1, n_circ + 1):
            v = v + Vec2d(size, 0).rotated(2.25 * pi * (a / n_circ))
            size -= 2
            L.append(v)

        b = self.path(L, radius=radius, static=True, friction=0.8)
        for s in b.shapes:
            s.wireframe = True
        return b


def draw():
    pyxel.cls(0)
    for s in w.space.shapes:
        paint(s, w.camera)
    for c in w.space.constraints:
        if hasattr(c, 'anchor_a'):
            pt = c.a.local_to_world(c.anchor_a)
            w.camera.circ(*pt, 1, pyxel.COLOR_YELLOW)
        if hasattr(c, 'anchor_b'):
            pt = c.b.local_to_world(c.anchor_b)
            w.camera.circ(*pt, 1, pyxel.COLOR_YELLOW)
        if hasattr(c, 'groove_a'):
            a = c.a.local_to_world(c.groove_a)
            b = c.a.local_to_world(c.groove_b)
            w.camera.line(*a, *b, pyxel.COLOR_DARKBLUE)

    pyxel.text(5, 5, f"Gear: {car.gear + 1}", pyxel.COLOR_WHITE)
    pyxel.text(5, 12, f"Speed: {car.velocity.length:.0f}", pyxel.COLOR_WHITE)
    pyxel.text(5, 19, f"RPM: {car.rpm:.0f}", pyxel.COLOR_WHITE)
    pyxel.text(5, 26, f"Max Speed: {max_speed:.0f}", pyxel.COLOR_WHITE)
     
def update():
    global max_speed

    w.space.step(1/90)
    w.space.step(1/90)
    w.space.step(1/90)
    max_speed = max(car.velocity.length, max_speed)

    # Zoom
    if pyxel.btn(pyxel.KEY_Z):
        w.camera.zoom(1.1)
    if pyxel.btn(pyxel.KEY_A):
        w.camera.zoom(1 / 1.1)
    
    # Acelera/Freia
    if pyxel.btn(pyxel.KEY_RIGHT):
        car.accelerate()
    elif pyxel.btn(pyxel.KEY_LEFT):
        car.break_()
    else:
        car.coast()

    # Passa marcha
    if pyxel.btnp(pyxel.KEY_UP):
        car.gear_up()
    if pyxel.btnp(pyxel.KEY_DOWN):
        car.gear_down()

    w.camera_ctrl.update()


pyxel.init(256, 192, fps=30)
pyxel.mouse(True)
max_speed = 0.0

w = VehicleWorld()
w.space.gravity = (0, -100)
w.space.damping = 0.95

w.ground(n=75, angle=(-7, 5), step=50)
car = w.car(50, 30)

w.camera.pan(-128, 30)
w.camera_ctrl = Follow(w.camera, car, margin=50, bias=0.1)

pyxel.run(update, draw)