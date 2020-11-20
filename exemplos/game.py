from math import pi
from camera import Camera, Follow, Sync, Combine
import random
from functools import partial
import pyxel
from pymunk import Vec2d
from world import PyxelWorld, paint


class Game(PyxelWorld):
    def __init__(self):
        super().__init__()
        self.space.gravity = (0, -200)
        self.space.damping = 0.95
        
        self.ground = self.platform((0, -90), 80, 30)
        self.platform((-200, 500), 4, height=600)
        self.target = self.circ(-50, -140, 10, static=True, color=pyxel.COLOR_RED, visible=False)
        self.player = self.circ(-120, 0, 8, color=pyxel.COLOR_RED, friction=0.5)
        self.ball = self.circ(-60, 50, 6, color=pyxel.COLOR_RED, velocity=(50, -50), elasticity=0)
        self.player.motor = self.motor(self.player, 0)
        
        tri = self.tri(-100, 0, -70, 0, -85, 20)
        self.pin(tri)
        self.gear(self.player, tri, -1)
        self.spring([self.player, self.ball], 1500, 25, damping=10)

        for i, pt in enumerate([(-50 + 35 * i, -30 + 20 * i) for i in range(10)]):
            p = self.platform(pt)
            if i % 2:
                p.angle = -pi / 4        
            else:
                p.angle = +pi / 4  
            self.space.reindex_shapes_for_body(p)      
        
        self.path([(70, -30), (110, -50), (130, -10)], static=True, radius=3)
        self.pin(self.platform((160, 0), static=False))

        p = self.platform((200, -70), width=4, static=False)
        self.pin(p, anchor=[p.position + (0, 0), p.position + (0, 20)])
        self.rotary_spring(p, 5e6, 10)

        p = self.platform((270, -70), width=3, static=False)
        s, *_ = p.shapes
        self.pin(p, offset=(-24, 0), anchor=(s.bb.left, 50), min=20)
        self.pin(p, offset=(+24, 0), anchor=(s.bb.right, 50), min=20)

        p1 = self.platform((270, 50), static=False)
        p2 = self.platform((302, 50), 1.4, static=False)
        self.pin([p1, p2], (16, 0), collide=False)
        self.pin(p1, (-16, 0))

        self.rect(0, 0, 20, 40, color=pyxel.COLOR_RED)
        self.tri(0, 0, -20, 0, -10, -20, color=pyxel.COLOR_RED)
            
        for i in range(10):
            self.rect(350, -90 + i * 21, 20, 20, color=pyxel.COLOR_RED, elasticity=0.1)
        
        cam1 = Camera(scale=0.2)
        cam2 = Camera(scale=0.5)
        self.bg = [
            partial(
                [cam1.rectb, cam2.rectb][i % 2],
                100 * random.uniform(i, i + 1),
                random.uniform(-200, 800),
                random.uniform(100, 200),
                random.uniform(100, 200),
                pyxel.COLOR_NAVY,
            )
            for i in range(-20, 200)
        ]
        self.camera_ctrl = Combine(
            Follow(self.camera, self.player, margin=50),
            Sync(self.camera, cam1, cam2),
        )


    def platform(self, start, width=2, height=4, **kwargs):
        x, y = start
        delta = width * 8
        kwargs.setdefault('static', True)
        kwargs.setdefault('color', pyxel.COLOR_WHITE)
        return self.rect(x - delta, y - height, 2 * delta, height, **kwargs)

    def update(self):
        p = self.player
        has_contact = False
        def incr(a):
            nonlocal has_contact
            has_contact = True
        p.each_arbiter(incr)

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            pos = self.camera.mouse_pos
            self.circ(*pos, 3, color=pyxel.COLOR_YELLOW)
        if pyxel.btn(pyxel.KEY_SPACE):
            J = Vec2d(-1, 0)
            if has_contact and p.velocity.dot(J.rotated(p.angle)) <= 100:
                p.apply_impulse_at_local_point(5e4 * J, (0, 0))

        if pyxel.btn(pyxel.KEY_A):
            self.camera.zoom(1.01)
        if pyxel.btn(pyxel.KEY_Z):
            self.camera.zoom(1 / 1.01)

        J = max(2e3 - p.velocity.length * 10, 0)
        if pyxel.btn(pyxel.KEY_LEFT):
            if has_contact:
                p.motor.rate = 10
            else:
                p.motor.rate = 2
                p.apply_impulse_at_world_point((-J, 0), p.position)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if has_contact:
                p.motor.rate = -10
            else:
                p.motor.rate = -2
                p.apply_impulse_at_world_point((J, 0), p.position)
        else:
            p.motor.rate *= 0.5
        
        self.space.step(1/60)
        self.camera_ctrl.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for fn in self.bg:
            fn()
        cam = self.camera
        for shape in self.space.shapes:
            paint(shape, cam)
        pyxel.text(0, 0, f"x = {int(cam.x)}, y = {int(cam.y)}", pyxel.COLOR_WHITE)

        pos = self.target.position
        red = pyxel.COLOR_RED
        cam.line(*self.player.position, *self.ball.position, red)
        cam.circ(*pos, 3, red)
        cam.circb(*pos, 1 + (pyxel.frame_count // 2) % 20, red)
        

pyxel.init(240, 180, fps=60)
pyxel.mouse(True)
game = Game()
pyxel.run(game.update, game.draw)