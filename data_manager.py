from tkinter import filedialog
from json import loads


def get_data():
    file = filedialog.askopenfile(
        title="Wähle eine kompatible Konfigurationsdatei . . .",
        defaultextension=".json",
        filetypes=[("Konfigurationsdateien", "*.memory")],
        initialdir=".",
    )
    content = loads(file.read())
    name = content["name"]
    cols = content["cols"]
    lines = content["lines"]
    front_bg = content["front-background-color"]
    back_bg = content["back-background-color"]
    color = content["color"]
    accent = content["accent-color"]
    data = content["data"]
    return name, cols, lines, front_bg, back_bg, color, accent, data
