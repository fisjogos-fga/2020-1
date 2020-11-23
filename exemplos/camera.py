from pymunk import Vec2d
import pymunk
import pyxel
from math import sin, cos


class Camera:
    @property
    def left(self):
        return self.x - pyxel.width / (2 * self.scale) 

    @property
    def right(self):
        return self.x + pyxel.width / (2 * self.scale) 

    @property
    def top(self):
        return self.y + pyxel.height / (2 * self.scale) 

    @property
    def bottom(self):
        return self.y - pyxel.height / (2 * self.scale) 

    @property
    def mouse_pos(self):
        return self.inv(pyxel.mouse_x, pyxel.mouse_y) 

    @property
    def mouse_x(self):
        return self.mouse_pos.x

    @property
    def mouse_y(self):
        return self.mouse_pos.y

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self._cos = cos(value)
        self._sin = sin(value)

    def __init__(self, x=0, y=0, scale=1.0, angle=0.0):
        self.x = x
        self.y = y
        self.scale = scale
        self._angle = angle
        self._cos = cos(angle)
        self._sin = sin(angle)

    def pan(self, x, y):
        self.x -= x
        self.y -= y

    def zoom(self, scale):
        self.scale *= scale

    def rotate(self, angle):
        self.angle += angle

    def transform(self, x, y):
        W = pyxel.width
        H = pyxel.height
        s = self.scale
        x_ = (x - self.x) * s + W / 2
        y_ = H / 2 - (y - self.y) * s

        cos, sin = self._cos, self._sin
        xt = cos * x_ - sin * y_ 
        yt = sin * x_ + cos * y_
        return Vec2d(xt, yt)

    def inv(self, x, y):
        W = pyxel.width
        H = pyxel.height
        s = self.scale
        x_ = (x - W / 2) / s + self.x
        y_ = self.y - (y - H / 2) / s
        return Vec2d(x_ , y_)

    def pset(self, x, y, col):
        pyxel.pset(*self.transform(x, y), col)

    def line(self, x1, y1, x2, y2, col):
        pyxel.line(*self.transform(x1, y1), *self.transform(x2, y2), col)

    def rect(self, x, y, w, h, col):
        s = self.scale
        pyxel.rect(*self.transform(x, y - h * s), w * s, h * s, col)

    def rectb(self, x, y, w, h, col):
        s = self.scale
        pyxel.rectb(*self.transform(x, y - h * s), w * s, h * s, col)

    def circ(self, x, y, r, col):
        pyxel.circ(*self.transform(x, y), r * self.scale, col)

    def circb(self, x, y, r, col):
        pyxel.circb(*self.transform(x, y), r * self.scale, col)
    
    def tri(self, x1, y1, x2, y2, x3, y3, col):
        pyxel.tri(
            *self.transform(x1, y1), 
            *self.transform(x2, y2), 
            *self.transform(x3, y3), 
            col)

    def trib(self, x1, y1, x2, y2, x3, y3, col):
        pyxel.trib(
            *self.transform(x1, y1), 
            *self.transform(x2, y2), 
            *self.transform(x3, y3), 
            col)

    def blt(self, x, y, img, u, v, w, h, colkey=None):
        args = () if colkey is None else (colkey,)
        pyxel.blt(*self.transform(x, y - h), img, u, v, w, h, *args)

    def bltm(self, x, y, tm, u, v, w, h, colkey=None):
        args = () if colkey is None else (colkey,)
        pyxel.bltm(*self.transform(x, y - h), tm, u, v, w, h, *args)

    def text(self, x, y, s, col):
        pyxel.text(*self.transform(x, y), s, col)


class CameraBehavior:
    def __init__(self, camera):
        self.camera = camera

    def update(self):
        """
        Override in sub-classes.
        """

class Select:
    def __init__(self, behavior1, behavior2):
        self.behavior1 = behavior1
        self.behavior2 = behavior2

    def update(self):
        self.behavior1.update()
    
    def toggle(self):
        self.behavior1, self.behavior2 = self.behavior2, self.behavior1


class Combine:
    def __init__(self, *behaviors):
        self.behaviors = behaviors

    def update(self):
        for b in self.behaviors:
            b.update()


class Sync(CameraBehavior):
    """
    Synchronize cameras center position. 
    """
    def __init__(self, camera, *other):
        super().__init__(camera)
        self._other = other 
    
    def update(self):
        x, y = self.camera.x, self.camera.y
        for cam in self._other:
            cam.x = x
            cam.y = y 


class Follow(CameraBehavior):
    """
    Camera follows object.
    """
    def __init__(self, camera, obj, offset=(0, 0), margin=0, bias=0):
        super().__init__(camera)
        self.object = obj
        self.bias = bias
        self._xtol, self._ytol = (margin, margin) if isinstance(margin, (int, float)) else margin

    def update(self):
        camera = self.camera
        obj = self.object

        xtol, ytol = self._xtol, self._ytol
        shape, *other = obj.shapes
        bb = shape.bb
        for shape in other:
            bb = bb.merge(shape.bb)

        dx = max(bb.right + xtol - camera.right, 0) or min(bb.left - xtol - camera.left, 0)
        dy = max(bb.top + ytol - camera.top, 0) or min(bb.bottom - ytol - camera.bottom, 0) 
        dx += self.bias * (obj.position.x - camera.x)
        dy += self.bias * (obj.position.y - camera.y)
        camera.pan(-dx, -dy)
