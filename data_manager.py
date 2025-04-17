from tkinter import filedialog, messagebox
from json import loads
import sys


def get_data():
    while True:
        path = filedialog.askopenfilename(
            title="Wähle eine kompatible Konfigurationsdatei . . .",
            defaultextension=".json",
            filetypes=[("Konfigurationsdateien", "*.memory")],
            initialdir=".",
        )

        if path == "":
            sys.exit()

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = loads(file.read())

            name = content["name"]
            cols = content["cols"]
            lines = content["lines"]
            front_bg = content["front-background-color"]
            back_bg = content["back-background-color"]
            accent = content["accent-color"]
            data = content["data"]

            if len(data) <= cols * lines:
                return name, cols, lines, front_bg, back_bg, accent, data
            else:
                messagebox.showwarning(
                    "Achtung",
                    "Die Zahl der Zeilen und Spalten stimmt nicht mit der Anzahl der Datensätze überein.",
                )

        except:
            messagebox.showerror(
                "Fehler",
                "Die geöffnete Datei ist leider nicht kompatibel. Bitte öffnen Sie eine kompatible Datei.",
            )
