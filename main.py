import pygame as gui
import sys

from data_manager import get_data
from grid import Grid

name, cols, lines, front_bg, back_bg, color, accent, data = get_data()

gui.init()

display = gui.display.set_mode((0, 0), gui.FULLSCREEN)
gui.display.set_caption(name)

clock = gui.time.Clock()

items = [Grid(display, cols, lines, front_bg, back_bg, color, accent, data)]

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

    for item in items:
        item.update()
        display.blit(item, item.rect)

    gui.display.update()
