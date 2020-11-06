import pyxel

pyxel.init(160, 120, caption="Meu Jogo!", fullscreen=True)
step = 0

def update():
    global step
    step += 1
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    # pyxel.cls(0)
    for i in range(10):
        pyxel.circ(10 + step + i * 15, 20 + i * 15, 5, ((step + i) // 5) % 16)

    pyxel.text(10, 60, 'Hello Pyxel!', 7)

pyxel.run(update, draw)