#Home Screen

from pathlib import Path
import os

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\tkinter\assets\frame3")
#Retorna o caminho absoluto do ficheiro Python atualmente em execução.
root_dir = os.path.dirname(os.path.abspath(__file__))
#Altera o diretório atual para o diretório do ficheiro python
os.chdir(root_dir)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
canvas.create_rectangle(
    127.20412110427878,
    150.17338001728058,
    128.03076171875,
    623.0,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#121212",
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=33.0,
    y=151.0,
    width=73.0,
    height=83.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#121212",
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=32.96923828125,
    y=278.0,
    width=71.0,
    height=90.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#121212",
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=32.96923828125,
    y=408.0,
    width=70.0,
    height=80.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#121212",
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=32.96923828125,
    y=533.6724853515625,
    width=72,
    height=87
)

canvas.create_text(
    187.0,
    29.0,
    anchor="nw",
    text="OLÁ,",
    fill="#FFFFFF",
    font=("Helvetica", 37 * -1)
)

canvas.create_text(
    290.0,
    29.0,
    anchor="nw",
    text="USERNAME",
    fill="#FFFFFF",
    font=("Helvetica Bold", 37 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    68.0,
    50.0,
    image=image_image_1
)
window.resizable(False, False)
window.mainloop()
