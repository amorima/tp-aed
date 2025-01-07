#Window Loading Screen in the Begining

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def openLoad():
    window = Tk()

    window.geometry("1200x675")
    window.configure(bg = "#121212")


    canvas = Canvas(
        window,
        bg = "#121212",
        height = 675,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        600.0,
        338.0,
        image=image_image_1
    )
    window.resizable(False, False)
    window.mainloop()
