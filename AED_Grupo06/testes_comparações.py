import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def criar_grafico(frame):
    labels = ['Aventura', 'Fantasia', 'Drama', 'Romance']
    sizes = [48, 22, 18, 12]
    explode = (0.1, 0, 0, 0)

    # Cria a Figure e o Ax
    fig, ax = plt.subplots()

    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=["#ffddff", "red"],  # Exemplos de cores
        explode=explode,
        shadow=True,
        labeldistance=.4
    )

    # Embed do gráfico no Frame
    canvas = FigureCanvasTkAgg(fig, master=frame)  # Frame onde quer colocar o plot
    canvas.draw()  # Renderiza o gráfico no canvas

    # O get_tk_widget() retorna o widget Tk que contém o canvas
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

# Exemplo de uso no CustomTkinter
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Exemplo Matplotlib no Frame")

    # Frame para colocar o gráfico
    grafico_frame = ctk.CTkFrame(app, width=600, height=400)
    grafico_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Função que cria e adiciona o gráfico no frame
    criar_grafico(grafico_frame)

    app.mainloop()
