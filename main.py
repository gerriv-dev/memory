import pygame as gui
import sys

gui.init()

display = gui.display.set_mode((0, 0), gui.FULLSCREEN)
gui.display.set_caption("Memory")

clock = gui.time.Clock()

while True:
    clock.tick(30)
    display.fill("#" + "2" * 6)

    for event in gui.event.get():
        if (
            event.type == gui.QUIT
            or event.type == gui.KEYDOWN
            and event.key == gui.K_ESCAPE
        ):
            gui.quit()
            sys.exit()

    gui.display.update()
