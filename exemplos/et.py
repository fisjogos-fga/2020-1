import pyxel

def update():
    global x

    x = pyxel.frame_count / 2.0

def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.blt(x, 60, 0, 3, 0, 10, 16, pyxel.COLOR_BLACK)
    

x = 0.0
pyxel.init(180, 120)
pyxel.load("assets.pyxres")
pyxel.run(update, draw)
