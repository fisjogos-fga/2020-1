from world import PyxelWorld, paint
from pymunk import Body, Segment, Space
from camera import Camera, Follow
import random
import pyxel
import threading
from time import sleep


max_time = 0.0
max_time_PID = (0, 0, 0)
LOCK = threading.Lock()


def sign(x):
    return 1.0 if x >= 0 else -1.0


class World(PyxelWorld):
    def __init__(self):
        super().__init__()
        self.space = Space(threaded=True)
        self.space.collision_slop = 0.7
        self.iter = 0
        self.time = 0.0
        self.on_reset = []
        self.P, self.I, self.D = 4.25347222, 0.0001041666, -4.67881944
        self.I = 0.0

        y = 0
        L = 500
        self.ground = self.line(-L, y, L, y, static=True, friction=0.75, radius=5)
        handler = self.space.add_wildcard_collision_handler(1)
        handler.begin = self.on_collision

    def update(self):
        dt = 1 / 30
        with LOCK:
            self.space.step(dt)
            self.time += dt

    def on_collision(self, arbiter, space, data):
        for fn in self.on_reset:
            fn(self)
        return True

    def reset(self):
        global segway

        self.time = 0.0
        self.iter += 1
        self.clear()
        ctrl.object = segway = self.segway()

    def clear(self):
        for shape in self.space.shapes:
            if shape not in self.ground.shapes:
                self.space.remove(shape)

        for cons in self.space.constraints:
            self.space.remove(cons)

        for body in self.space.bodies:
            if body is not self.ground:
                self.space.remove(body)

    def segway(self):
        R = 12
        L = 60
        segway = self.circ(0, R, R, mass=1, moment=1, friction=2.0)
        arm = self.line(0, R, 0, R + L, mass=2, moment=50)
        head = self.circ(0, R + L, R, mass=8, moment=8, velocity=(-1, 0), friction=0.1)
        self.pin([head, arm], collide=False)

        next(iter(head.shapes)).collision_type = 1

        self.pin([segway, arm], anchor=(0, -L / 2), collide=False)

        segway.update = iter(self.pid(segway, arm)).__next__
        segway.radius = R
        segway.arm = arm
        segway.head = head
        return segway

    def pid(self, wheel, arm):
        P, I, D = self.P, self.I, self.D
        cte = 100
        R = wheel.radius
        err_ = 0.0
        err_i = 0.0
        gamma = 0.02

        while True:
            err = arm.angle
            err_i = err + 0.9 * err_i
            err_d = err - err_

            w = cte * (P * err - I * err_i - D * err_d)
            if w == 0:
                F = 0
            else:
                F = 100 * (1 if w > wheel.angular_velocity else -1)
            F -= gamma * abs(F) * wheel.angular_velocity

            wheel.apply_force_at_local_point((0, +F), (+R, 0))
            wheel.apply_force_at_local_point((0, -F), (-R, 0))
            err_ = err
            yield


def draw():
    pyxel.cls(0)
    for poly in BG:
        camera.rectb(*poly, pyxel.COLOR_DARKBLUE)
    for s in w.space.shapes:
        paint(s, camera)
    for c in w.space.constraints:
        if hasattr(c, "anchor_a"):
            pt = c.a.local_to_world(c.anchor_a)
            camera.circ(*pt, 1, pyxel.COLOR_YELLOW)
        if hasattr(c, "anchor_b"):
            pt = c.b.local_to_world(c.anchor_b)
            camera.circ(*pt, 1, pyxel.COLOR_YELLOW)

    P, I, D = max_time_PID
    pyxel.text(210, 0, f"iter = {w.iter}", pyxel.COLOR_WHITE)
    pyxel.text(0, 0, f"omega = {segway.angular_velocity}", pyxel.COLOR_RED)
    pyxel.text(0, 7, f"P = {w.P}", pyxel.COLOR_RED)
    pyxel.text(0, 14, f"I = {w.I}", pyxel.COLOR_RED)
    pyxel.text(0, 21, f"D = {w.D}", pyxel.COLOR_RED)
    pyxel.text(0, 28, f"t = {w.time:.1f}", pyxel.COLOR_RED)
    pyxel.text(0, 35, f"Best time = {max_time:.1f}", pyxel.COLOR_RED)
    pyxel.text(0, 42, f"Best PID = {P:.2f}, {I:.2f}, {D:.2f}", pyxel.COLOR_RED)


def update():
    if full_speed:
        if pyxel.frame_count % 8 != 0:
            return

    segway.update()
    w.update()
    ctrl.update()


def fn(P, I, D):
    global max_time, max_time_PID

    stop = False

    def do_stop(w):
        nonlocal stop
        stop = True

    with LOCK:
        w.reset()
    w.P, w.I, w.D = P, I, D
    w.on_reset.append(do_stop)

    time = 0.0
    while not stop:
        sleep(1 / 100)
        time = max(time, w.time)

    w.on_reset.remove(do_stop)

    if time > max_time:
        max_time = time
        max_time_PID = [P, I, D]

    print(f"{P:.2f}, {I:.2f}, {D:.2f}, {time:.2f}")
    return -time


def opt(opt=True):
    global full_speed, max_time_PID
    from scipy import optimize

    P, I, D = max_time_PID = w.P, w.I, w.D
    if opt:
        # optimize.fmin(lambda p: fn(*p), [P, I, D])
        optimize.brute(lambda x: fn(*x), [(0, 100), (-5, 0), (-5, 0)], Ns=25)

    w.P, w.I, w.D = max_time_PID

    def reset():
        w.reset()
        segway.head.velocity = (random.uniform(-40, 30), 0)

    w.on_reset.append(lambda s: w.reset())
    w.reset()
    full_speed = True


pyxel.init(256, 192, fps=240, fullscreen=False)
BG = [
    (
        random.uniform(-500, 500),
        random.uniform(0, 200),
        random.uniform(15, 50),
        random.uniform(15, 50),
    )
    for _ in range(50)
]
w = World()
w.space.gravity = (0, -100)
w.space.damping = 0.9
segway = w.segway()
full_speed = False

camera = Camera()
ctrl = Follow(camera, segway.arm, margin=50, bias=0.0)


t = threading.Thread(target=opt, daemon=True, kwargs={"opt": False})
full_speed = True
t.start()

pyxel.run(update, draw)