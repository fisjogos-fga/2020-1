import pyxel

x = 0
color = 7


def update():
    global x, color
    
    x = pyxel.frame_count
    if pyxel.btn(pyxel.KEY_A):
        color = 9
    else:
        color = 7


def draw():
    pyxel.cls(0)
    pyxel.circ(x, 60, 5, color)
    

pyxel.init(180, 120, fps=60)
pyxel.run(update, draw)