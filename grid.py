import pygame as gui
from pygame.surface import Surface
from random import shuffle


class Grid(Surface):
    def __init__(self, display: Surface, cols, lines, front_bg, back_bg, accent, data):
        super().__init__(display.get_size())
        self.rect = self.get_rect(topleft=(0, 0))
        self.cols, self.lines = cols, lines
        self.front_bg = front_bg
        self.back_bg = back_bg
        self.accent = accent
        self.data = data
        self.back_cells = []
        self.front_cells = []
        self.control_delay = 0
        self.build_back_cells()
        self.build_front_cells()

    def load_image(self, surf: Surface, path):
        img = gui.image.load(path).convert_alpha()

        if img.get_width() < img.get_height():
            scale_factor = surf.get_width() / img.get_width()
        else:
            scale_factor = surf.get_height() / img.get_height()

        img = gui.transform.rotozoom(img, 0, scale_factor)
        img_rect = img.get_rect(center=(surf.get_width() / 2, surf.get_height() / 2))
        surf.blit(img, img_rect)

    def create_text(self, surf: Surface, text: str, color, bg):
        font = gui.font.Font("NotoSans.ttf", 24)

        words = text.split()
        words.append("")

        line_surfs = []

        line = ""
        for word in words:
            line += " " + word
            temp_surf = font.render(line, True, color, bg)

            if temp_surf.get_width() <= surf.get_width() - 5:
                line_surf = temp_surf
            else:
                line_surfs.append(line_surf)
                temp_surf = None
                line = word

        if temp_surf:
            line_surfs.append(temp_surf)

        base_surf = Surface(
            (surf.get_width(), sum([s.get_height() for s in line_surfs]))
        )
        base_surf.fill(bg)

        y = 0
        for line_surf in line_surfs:
            rect = line_surf.get_rect(midtop=(base_surf.get_width() / 2, y))
            base_surf.blit(line_surf, rect)
            y += line_surf.get_height()

        base_rect = base_surf.get_rect(
            center=(surf.get_width() / 2, surf.get_height() / 2)
        )
        surf.blit(base_surf, base_rect)

    def build_back_cells(self):
        cell_width = round(self.get_width() / self.cols)
        cell_height = round(self.get_height() / self.lines)

        color = self.back_bg[1:]
        color = tuple(255 - int(color[i : i + 2], 16) for i in (0, 2, 4))

        while len(self.data) < self.cols * self.lines:
            self.data.append({"type": "text", "value": "Joker"})

        shuffle(self.data)

        for line_index, _ in enumerate(range(self.lines)):
            for col_index, _ in enumerate(range(self.cols)):
                cell = Surface((cell_width, cell_height))
                cell.fill(self.back_bg)
                cell_rect = cell.get_rect(
                    topleft=(col_index * cell_width, line_index * cell_height)
                )
                if self.data[col_index + line_index * self.cols]["type"] == "text":
                    self.create_text(
                        cell,
                        self.data[col_index + line_index * self.cols]["value"],
                        color,
                        self.back_bg,
                    )
                else:
                    self.load_image(
                        cell, self.data[col_index + line_index * self.cols]["value"]
                    )
                self.back_cells.append([cell, cell_rect])

    def build_front_cells(self):
        cell_width = round(self.get_width() / self.cols)
        cell_height = round(self.get_height() / self.lines)

        color = self.front_bg[1:]
        color = tuple(255 - int(color[i : i + 2], 16) for i in (0, 2, 4))

        for line_index, _ in enumerate(range(self.lines)):
            for col_index, _ in enumerate(range(self.cols)):
                cell = Surface((cell_width, cell_height))
                cell.fill(self.front_bg)
                cell_rect = cell.get_rect(
                    topleft=(col_index * cell_width, line_index * cell_height)
                )
                self.create_text(
                    cell,
                    str(col_index + line_index * self.cols + 1),
                    color,
                    self.front_bg,
                )
                self.front_cells.append([cell, cell_rect, True])

    def handle_user_input(self):
        mouse_pos = gui.mouse.get_pos()
        click = gui.mouse.get_pressed()[0]

        for cell_index, (_, cell_rect, status) in enumerate(self.front_cells):
            if cell_rect.collidepoint(mouse_pos) and click:
                self.front_cells[cell_index][2] = not status
                self.control_delay = 5

    def show_back_cells(self):
        for cell, cell_rect in self.back_cells:
            self.blit(cell, cell_rect)

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

        self.show_back_cells()
        self.show_front_cells()
