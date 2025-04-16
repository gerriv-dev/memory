import pygame as gui
from pygame.surface import Surface


class Grid(Surface):
    def __init__(self, display: Surface, cols, lines, bg, color, accent, data):
        super().__init__(display.get_size())
        self.rect = self.get_rect(topleft=(0, 0))
        self.cols, self.lines = cols, lines
        self.bg = bg
        self.color = color
        self.accent = accent
        self.data = data
        self.front_cells = []
        self.control_delay = 0
        self.build_front_cells()

    def build_front_cells(self):
        cell_width = round(self.get_width() / self.cols)
        cell_height = round(self.get_height() / self.lines)
        font = gui.font.Font(None, 32)

        for line_index, _ in enumerate(range(self.lines)):
            for col_index, _ in enumerate(range(self.cols)):
                cell = Surface((cell_width, cell_height))
                cell.fill(self.bg)
                cell_rect = cell.get_rect(
                    topleft=(col_index * cell_width, line_index * cell_height)
                )
                text = font.render(
                    str(col_index + line_index * self.cols + 1), True, self.color
                )
                text_rect = text.get_rect(
                    center=(cell.get_width() / 2, cell.get_height() / 2)
                )
                cell.blit(text, text_rect)
                self.front_cells.append([cell, cell_rect, True])

    def handle_user_input(self):
        mouse_pos = gui.mouse.get_pos()
        click = gui.mouse.get_pressed()[0]

        for cell_index, (_, cell_rect, status) in enumerate(self.front_cells):
            if cell_rect.collidepoint(mouse_pos) and click:
                self.front_cells[cell_index][2] = not status
                self.control_delay = 5

    def show_front_cells(self):
        for cell, cell_rect, status in self.front_cells:
            if status:
                self.blit(cell, cell_rect)
            gui.draw.rect(self, self.accent, cell_rect, 2)

    def update(self):
        self.fill((0, 0, 0, 0))

        if self.control_delay > 0:
            self.control_delay -= 1
        else:
            self.handle_user_input()

        self.show_front_cells()
