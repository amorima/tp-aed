#Log in Window

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1200x675")
window.configure(bg = "#E6F2F0")


canvas = Canvas(
    window,
    bg = "#E6F2F0",
    height = 675,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    738.5,
    131.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=521.0,
    y=110.0,
    width=435.0,
    height=41.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    738.5,
    212.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=521.0,
    y=191.0,
    width=435.0,
    height=41.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    234.0,
    337.0,
    image=image_image_1
)

canvas.create_text(
    513.0,
    246.4549560546875,
    anchor="nw",
    text="Esqueceste-te da tua palavra passe?",
    fill="#4F8377",
    font=("Helvetica", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=513.0,
    y=297.0,
    width=173.0,
    height=35.7931022644043
)

canvas.create_text(
    514.0,
    92.0,
    anchor="nw",
    text="E-MAIL",
    fill="#000000",
    font=("Helvetica Bold", 10 * -1)
)

canvas.create_text(
    513.0,
    173.0,
    anchor="nw",
    text="PALAVRA-PASSE*",
    fill="#000000",
    font=("Helvetica Bold", 10 * -1)
)

canvas.create_text(
    93.0,
    351.0,
    anchor="nw",
    text="A tua biblioteca ",
    fill="#E6F2F0",
    font=("Helvetica Bold", 34 * -1)
)

canvas.create_text(
    93.0,
    393.0,
    anchor="nw",
    text="de filmes",
    fill="#E6F2F0",
    font=("Helvetica Bold", 34 * -1)
)

canvas.create_text(
    93.0,
    435.0,
    anchor="nw",
    text="e séries",
    fill="#E6F2F0",
    font=("Helvetica Bold", 34 * -1)
)

canvas.create_text(
    513.0,
    36.0,
    anchor="nw",
    text="Iniciar Sessão",
    fill="#4F8377",
    font=("Helvetica Bold", 24 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=513.0,
    y=601.0,
    width=173.0,
    height=35.7931022644043
)

canvas.create_text(
    514.0,
    540.0,
    anchor="nw",
    text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores ",
    fill="#121212",
    font=("Helvetica Bold", 16 * -1)
)

canvas.create_text(
    514.0,
    565.0,
    anchor="nw",
    text="vantagens na Hoot.",
    fill="#121212",
    font=("Helvetica Bold", 16 * -1)
)

canvas.create_text(
    513.0,
    494.0,
    anchor="nw",
    text="Ainda não tens conta?",
    fill="#4F8377",
    font=("Helvetica Bold", 24 * -1)
)
window.resizable(False, False)
window.mainloop()
