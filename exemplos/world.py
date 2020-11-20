import pyxel
from pymunk import Space, Body, Circle, Poly, Segment, Vec2d
from pymunk import constraint
from camera import Camera
from math import pi, sin, cos
from functools import singledispatch
DEGREES = pi / 180


class delegate(property):
    """
    Delegate attribute to other attribute.
    """
    
    def __init__(self, name, attr=None):
        super().__init__(
            lambda obj: getattr(getattr(obj, name), self.attr),
            lambda obj, value: setattr(getattr(obj, name), self.attr, value),
        )
        self.attr = attr

    def __set_name__(self, cls, name):
        if self.attr is None:
            self.attr = name 


class PyxelWorld:
    """
    A place to store Pyxel and Pymunk objects
    """
    add = delegate('space')

    def __init__(self, space=None, camera=None, steps=1):
        self.space = space or Space()
        self.camera = camera or Camera()
        self.camera_ctrl = None

    def _make_body(self, static=False, kinematic=False, mass=None, moment=None, velocity=(0, 0), **kwargs):
        extra = {}
        if static is True: 
            kind = Body.STATIC
        elif mass == float('inf') or kinematic:
            kind = Body.KINEMATIC
            mass = moment = 1.0
        else:
            kind = Body.DYNAMIC
            extra = {'mass': mass or 0, 'moment': moment or 0}
        
        body = Body(body_type=kind, **extra)
        body.velocity = velocity
        return body

    def _make_shape(self, shape, color=None, mass=None, moment=None, visible=True, **kwargs):
        body = shape.body

        shape._has_friction = 'friction' in kwargs
        shape._has_elasticity = 'elasticity' in kwargs
        shape.elasticity = kwargs.get('elasticity', 0.5)
        shape.friction = kwargs.get('friction', 0.5)
        shape.visible = visible
        
        if color is not None:
            shape.color = color
        
        if body.body_type == Body.DYNAMIC and mass is None:
            shape.mass = shape.area
        if body.body_type == Body.DYNAMIC and moment is None:
            shape.mass = shape.mass or body.mass
            bb = shape.bb
            rog2 = 0.25 * ((bb.top - bb.bottom) ** 2 + (bb.right - bb.left) ** 2)
            body.moment = (shape.mass or body.mass) * rog2
        
        return shape

    def _add_constraint(self, cons, collide=True, max_bias=None, error_bias=None, max_force=None):
        cons.collide_bodies = collide
        if error_bias is not None:
            cons.error_bias = error_bias
        if max_bias is not None:
            cons.max_bias = max_bias
        if max_force is not None:
            cons.max_force = max_force
        self.add(cons)
        return cons

    def circ(self, x, y, r, **kwargs):
        """
        Creates a circle at radius r centered at (x, y).
        """

        body = self._make_body(**kwargs)
        shape = self._make_shape(Circle(body, r), **kwargs)
        body.position = (x, y)
        self.space.add(body, shape)
        return body

    def line(self, x1, y1, x2, y2, radius=1, **kwargs):
        """
        Creates a line segment from (x1, y1) to (x2, y2).
        """
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        body = self._make_body(**kwargs)
        shape = Segment(body, (x1 - xm, y1 - ym), (x2 - xm, y2 - ym), radius)
        shape = self._make_shape(shape, **kwargs)
        
        body.position = (xm, ym)
        self.space.add(body, shape)
        return body

    def rect(self, x, y, w, h, **kwargs):
        """
        Creates a rectangular polygon starting at (x, y) with given width and height.
        """
        return self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], **kwargs)

    def rectb(self, x, y, w, h, radius=1, **kwargs):
        """
        Like rect(), but create an wireframe path with several line segments.
        """
        a, b, c, d = (x, y), (x + w, y), (x + w, y + h), (x, y + h)
        return self.path([a, b, c, d, a], **kwargs)

    def tri(self, x1, y1, x2, y2, x3, y3, **kwargs):
        """
        Creates a solid triangle from the given vertice coordinates.
        """
        return self.poly([(x1, y1), (x2, y2), (x3, y3)], **kwargs)

    def trib(self, x1, y1, x2, y2, x3, y3, **kwargs):
        """
        Like tri(), but create an wireframe path with several line segments.
        """
        return self.path([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], **kwargs)

    def poly(self, vertices, *, radius=0, **kwargs):
        """
        Creates polygon from the given list of vertices.
        """
        cm = center_of_mass(vertices)
        vertices = [v - cm for v in vertices]
        
        body = self._make_body(**kwargs)
        shape = Poly(body, vertices, radius=radius)
        shape = self._make_shape(shape, **kwargs)
        
        body.position = cm
        self.space.add(body, shape)
        return body

    def path(self, vertices, *, radius=0, **kwargs):
        """
        Creates path of segments from the given list of vertices.
        """
        body = self._make_body(**kwargs)
        cm = path_center_of_mass(vertices)
        vs = vertices[:-1]
        us = vertices[1:]
        shapes = [self._make_shape(Segment(body, a - cm, b - cm, radius), **kwargs)
                  for a, b in zip(vs, us)]
        body.position = cm
        self.space.add(body, *shapes)
        return body

    def pin(self, obj, offset=(0, 0), anchor=None, min=None, max=None, world=False, **kwargs):
        """
        Pin object into space so it can rotate around the center of mass.
        """
        a, b = (obj, self.space.static_body) if isinstance(obj, Body) else obj 
        
        if anchor is None and max is None and min is None:
            if not world:
                offset = a.local_to_world(offset)
            joint = constraint.PivotJoint(a, b, offset)
        elif min is None and max is None:
            if world:
                offset = a.world_to_local(offset)
                anchor = b.world_to_local(anchor)
            a1, a2 = anchor
            if isinstance(a1, (float, int)):
                joint = constraint.PinJoint(a, b, offset, anchor)
            elif world:
                a1 = b.world_to_local(a1)
                a2 = b.world_to_0local(a2)
                joint = constraint.GrooveJoint(b, a, a1, a2, offset)
            else:
                joint = constraint.GrooveJoint(b, a, a1, a2, offset)
        else:
            anchor = anchor or (0, 0)
            L = (a.local_to_world(offset) - b.local_to_world(anchor)).length
            min = L if min is None else min
            max = L if max is None else max
            if world:
                offset = a.world_to_local(offset)
                anchor = b.world_to_local(anchor)
            joint = constraint.SlideJoint(a, b, offset, anchor, min, max)

        return self._add_constraint(joint, **kwargs)

    def spring(self, obj, stiffness, length=None, offset=(0, 0), anchor=(0, 0), damping=0.0, world=False, **kwargs):
        """
        Connect object or pair of objects with a string.
        """
        a, b = (obj, self.space.static_body) if isinstance(obj, Body) else obj 
        if world:
            offset = a.world_to_local(offset)
            anchor = a.world_to_local(anchor)
        if length is None:
            length = (Vec2d(anchor) - offset).length
        joint = constraint.DampedSpring(a, b, offset, anchor, length, stiffness, damping)
        return self._add_constraint(joint, **kwargs)

    def rotary_spring(self, obj, stiffness, damping=0.0, angle=0.0, **kwargs):
        """
        Connect object or pair of objects with a rotary string.
        """
        a, b = (obj, self.space.static_body) if isinstance(obj, Body) else obj 
        joint = constraint.DampedRotarySpring(a, b, angle, stiffness, damping)
        return self._add_constraint(joint, **kwargs)
    
    def rotary_limit(self, obj, min, max, degrees=False, **kwargs):
        """
        Limit rotation of object.
        """
        a, b = (obj, self.space.static_body) if isinstance(obj, Body) else obj 
        if degrees:
            min, max = min * DEGREES, max * DEGREES
        joint = constraint.RotaryLimitJoint(a, b, min, max)
        return self._add_constraint(joint, **kwargs)

    def gear(self, a, b, ratio=1.0, phase=0.0, degrees=False, **kwargs):
        """
        Connect two objects as a gear, synchronazing their rotations.
        """
        if degrees:
            phase = phase * DEGREES
        else:
            joint = constraint.GearJoint(b, a, phase, ratio)
        return self._add_constraint(joint, **kwargs)

    def ratchet(self, a, b, ratchet=1.0, phase=0.0, degrees=False, **kwargs):
        """
        Connect two objects as a ratchet, synchronazing their rotations if done
        in some specific direction.
        """
        if degrees:
            phase = phase * DEGREES
        else:
            joint = constraint.RatchetJoint(b, a, phase, ratchet)
        return self._add_constraint(joint, **kwargs)

    def motor(self, obj, rate, degrees=False, **kwargs):
        """
        Fix rotation rate of object (or relative rotations of a pair).
        """
        a, b = (obj, self.space.static_body) if isinstance(obj, Body) else obj 
        if degrees:
            rate = rate * DEGREES
        joint = constraint.SimpleMotor(a, b, rate)
        return self._add_constraint(joint, **kwargs)


@singledispatch
def paint(obj, camera=pyxel):
    try:
        method = obj.draw
    except AttributeError:
        pass
    else:
        return method(camera)
    name = type(obj).__name__
    raise TypeError(f'cannot draw {name} instances')


@paint.register(Circle)
def _(shape, camera=pyxel):
    if not shape.visible:
        return 
    body = shape.body
    x, y = body.local_to_world(shape.offset)
    color = getattr(shape, 'color', pyxel.COLOR_WHITE)
    camera.circ(x, y, shape.radius, color)
    x_ = shape.radius * cos(body.angle) + x
    y_ = shape.radius * sin(body.angle) + y
    camera.line(x, y, x_, y_, 0)


@paint.register(Segment)
def _(shape, camera=pyxel, wireframe=False):
    if not shape.visible:
        return 
    
    body = shape.body
    color = getattr(shape, 'color', pyxel.COLOR_WHITE)
    a = body.local_to_world(shape.a)
    b = body.local_to_world(shape.b)
    radius = shape.radius
    wireframe = getattr(shape, 'wireframe', wireframe)
    
    if wireframe or radius < 1:
        camera.line(*a, *b, color)
    else:
        camera.circ(*a, radius, color)
        camera.circ(*b, radius, color)
        n = (b - a).normalized().rotated(pi/2)
        
        v1 = a + n * radius
        v2 = a - n * radius
        v3 = b - n * radius
        v4 = b + n * radius

        camera.tri(*v1, *v2, *v3, color)
        camera.tri(*v3, *v4, *v1, color)


@paint.register(Poly)
def _(shape, camera=pyxel):
    if not shape.visible:
        return 
    body = shape.body
    color = getattr(shape, 'color', pyxel.COLOR_WHITE)
    for tri in group_tri(shape.get_vertices()):
        coords = []
        for v in tri:
            x,y = v.rotated(body.angle) + body.position
            coords.extend((x, y))
        camera.tri(*coords, color)


def group_tri(seq):
    """
    Rotate sequence in groups of tree.
    """
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z


def center_of_mass(seq):
    """
    Center of mass of a polygon.
    """

    M = 0.0
    cm = Vec2d(0, 0)
    for a, b, c in group_tri(seq):
        a, b, c = map(Vec2d, (a, b, c))
        A = abs((b - a).cross(c - a))
        M += A
        cm += (A / 3) * (a + b + c)        
    return cm / M


def path_center_of_mass(seq):
    """
    Center of mass of a path.
    """
    M = 0.0
    cm = Vec2d(0, 0)
    for a, b in zip(seq[:-1], seq[1:]):
        a, b = map(Vec2d, (a, b))
        m = (b - a).length
        M += m
        cm += (m / 2) * (a + b)       
    return cm / M

