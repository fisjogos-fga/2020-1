import pyxel
from math import sqrt


def update():
    global x, y

    dx = pyxel.mouse_x - x
    dy = pyxel.mouse_y - y
    length = sqrt(dx**2 + dy**2)
    
    vx = SPEED * dx / length
    vy = SPEED * dy / length
    
    x += vx * dt
    y += vy * dt 

def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.circ(x, y, 5, pyxel.COLOR_RED)


SPEED = 100
FPS = 60
dt = 1 / 60
x, y = 0, 0

pyxel.init(180, 120, fps=FPS)
pyxel.mouse(True)
pyxel.run(update, draw)