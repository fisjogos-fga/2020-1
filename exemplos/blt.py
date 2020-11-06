import pyxel


def update():
    ...

def draw():
    x = 10 + pyxel.frame_count / 4
    pyxel.cls(1)
    pyxel.blt(x, 60, 0, 3, 0, 10, 16, 0)

pyxel.init(180, 120)
pyxel.load("assets.pyxres")
pyxel.run(update, draw)
