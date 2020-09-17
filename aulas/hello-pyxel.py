import pyxel
import math


def update():
    global x, y, vx, vy

    if pyxel.btn(pyxel.KEY_SPACE):
        g = 0.0
    else:
        g = gamma
        
    Fx = - k * (x - pyxel.mouse_x) - g * vx
    Fy = - k * (y - pyxel.mouse_y) - g * vy

    ax = Fx / m
    ay = Fy / m

    vx += ax * dt
    vy += ay * dt

    # Testa colisão
    if x < r:
        vx = e * abs(vx)
    if x > pyxel.width - r:
        vx = -e * abs(vx)
    if y < r:
        vy = e * abs(vy)
    if y > pyxel.height - r:
        vy = -e * abs(vy)
        
    x += vx * dt
    y += vy * dt



def draw():
    pyxel.cls(10)
    pyxel.line(x, y, pyxel.mouse_x, pyxel.mouse_y, pyxel.COLOR_WHITE)
    pyxel.blt(x - r, y - r, 0, 4, 3, 11, 11, pyxel.COLOR_BLACK)


# Inicializa o objeto
k = 20
r = 11 / 2
e = 0.5
gamma = 5
dt = 1 / 30
m = 10
x, y = (10, 60)
vx, vy = (0, 100)


pyxel.init(180, 120, fps=30, caption="Meu Jogo!")
pyxel.mouse(True)
pyxel.load("assets.pyxres")
pyxel.run(update, draw)
