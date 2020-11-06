import pyxel


def update():
    global x, y
    
    vx, vy = 0, 0
    
    if pyxel.btnp(pyxel.KEY_UP, hold=160):
        vy = -SPEED
    if pyxel.btnp(pyxel.KEY_DOWN, hold=160):
        vy = +SPEED
    if pyxel.btnp(pyxel.KEY_LEFT, hold=160):
        vx = -SPEED
    if pyxel.btnp(pyxel.KEY_RIGHT, hold=160):
        vx = +SPEED

    x += vx * dt
    y += vy * dt
        

def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.circ(x, y, 5, pyxel.COLOR_RED)


SPEED = 100
FPS = 60
dt = 1 / FPS
x, y = 90, 60


pyxel.init(180, 120, fps=FPS)
pyxel.run(update, draw)