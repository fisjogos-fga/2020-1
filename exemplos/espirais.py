import pyxel
from math import cos, sin

pyxel.init(180, 120)
step = 0


def update():
    global step
    step += 1


def draw():
    pyxel.cls(3)

    
    radius = 5
    X = 90
    Y = 60
    for i in range(64):
        t = 20 + i
        r = t * step / 50 
        x = X + r * cos(t)
        y = Y + r * sin(t)
        pyxel.circ(x, y, radius, i % 16)
    
    pyxel.text(130, 110, f"Frames: {step}", 2)


pyxel.run(update, draw)