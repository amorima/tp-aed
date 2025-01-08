import customtkinter as ctk
from PIL import Image
import os

#######################
####### FUNÇÕES #######
#######################

def splashscreen():
    """Cria a splashscreen da app."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    # Adicionar o logótipo
    logo = ctk.CTkImage(Image.open('./img/logo.png'), size=(373, 142))
    label_logo = ctk.CTkLabel(app, text="", image=logo)
    label_logo.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o logótipo

    # Agendar a transição para a próxima função
    app.after(3000, iniciar_app)  # Transita para `iniciar_app` após 3 segundos


def iniciar_app():
    """Inicializa a aplicação principal."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./img/promo.png'), size=(468, 675))
    label_promo = ctk.CTkLabel(app, text="", image=promo)
    label_promo.place(relx=0.0, rely=0.5, anchor="w")

    rotulo = ctk.CTkLabel(app, text="Iniciar Sessão", font=("Helvetica", 24, "bold"), text_color="#4F8377")
    rotulo.place(x=513, y=36)

    rotulo = ctk.CTkLabel(app, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo.place(x=513, y=92)

    entry_email = ctk.CTkEntry(app,
                         width=451,
                         height=43,
                         border_width=0,
                         placeholder_text="Insira o seu e-mail",
                         fg_color="#D9D9D9",
                         font=("Helvetica", 16),
                         )
    entry_email.place(x=513, y=115)  # Posicionar a textbox no local desejado

    rotulo = ctk.CTkLabel(app, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo.place(x=513, y=169)

    entry_password = ctk.CTkEntry(app,
                         width=451,
                         height=43,
                         border_width=0,
                         placeholder_text="Insira a sua palavra-passe",
                         show="*",
                         fg_color="#D9D9D9",
                         font=("Helvetica", 16),
                         )
    entry_password.place(x=513, y=191)  # Posicionar a textbox no local desejado

    # Criar o texto clicável
    clickable_text = ctk.CTkLabel(app,
                                  text="Esqueceste-te da tua palavra passe?",
                                  text_color="#4F8377",
                                  font=("Helvetica", 16, "underline"))
    clickable_text.place(x=513, y=246)
    # Associe a função de clique ao texto
    clickable_text.bind("<Button-1>", lambda event: on_text_click())
    
    button_iniciar_sessao = ctk.CTkButton(app,
                           text='INICIAR SESSÃO',
                           font=("Helvetica", 14.3, "bold"),
                           text_color="#000",
                           hover_color="#D59C2A",
                           fg_color="#F2C94C",
                           width=173,
                           height=36)
    button_iniciar_sessao.place(x=513, y=297)

    rotulo = ctk.CTkLabel(app, text="Ainda não tens conta?", font=("Helvetica", 24, "bold"), text_color="#4F8377")
    rotulo.place(x=513, y=494)

    rotulo = ctk.CTkLabel(app, text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores ", font=("Helvetica", 16, "bold"), text_color="#000")
    rotulo.place(x=513, y=540)

    rotulo = ctk.CTkLabel(app, text="vantagens na Hoot.", font=("Helvetica", 16, "bold"), text_color="#000")
    rotulo.place(x=513, y=565)

    button_criar_conta = ctk.CTkButton(app,
                           text='CRIAR CONTA',
                           font=("Helvetica", 14.3, "bold"),
                           text_color="#fff",
                           hover_color="#E1B037",
                           fg_color="#4F8377",
                           width=173,
                           height=36)
    button_criar_conta.place(x=513, y=601)

def criar_conta():
    """Inicializa a aplicação principal."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./img/promo.png'), size=(468, 675))
    label_promo = ctk.CTkLabel(app, text="", image=promo)
    label_promo.place(relx=0.0, rely=0.5, anchor="w")

    rotulo = ctk.CTkLabel(app, text="Criar Conta", font=("Helvetica", 24, "bold"), text_color="#4F8377")
    rotulo.place(x=513, y=36)

    rotulo = ctk.CTkLabel(app, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo.place(x=513, y=112)

    entry_username = ctk.CTkEntry(app,
                         width=451,
                         height=43,
                         border_width=0,
                         placeholder_text="Insira um username",
                         fg_color="#D9D9D9",
                         font=("Helvetica", 16),
                         )
    entry_username.place(x=513, y=134)  # Posicionar a textbox no local desejado

    rotulo = ctk.CTkLabel(app, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo.place(x=513, y=208)

    entry_email = ctk.CTkEntry(app,
                         width=451,
                         height=43,
                         border_width=0,
                         placeholder_text="Insira um e-mail",
                         fg_color="#D9D9D9",
                         font=("Helvetica", 16),
                         )
    entry_email.place(x=513, y=231)  # Posicionar a textbox no local desejado

    rotulo = ctk.CTkLabel(app, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo.place(x=513, y=305)

    entry_password = ctk.CTkEntry(app,
                         width=451,
                         height=43,
                         border_width=0,
                         placeholder_text="Insira uma palavra-passe",
                         show="*",
                         fg_color="#D9D9D9",
                         font=("Helvetica", 16),
                         )
    entry_password.place(x=513, y=328)  # Posicionar a textbox no local desejado

    button_criar_conta = ctk.CTkButton(app,
                           text='CRIAR CONTA',
                           font=("Helvetica", 14.3, "bold"),
                           text_color="#fff",
                           hover_color="#E1B037",
                           fg_color="#4F8377",
                           width=173,
                           height=36)
    button_criar_conta.place(x=513, y=414)

#########################
#### CONFIGURAÇÕES ######
#########################

# Retorna o caminho absoluto do ficheiro Python atualmente em execução
root_dir = os.path.dirname(os.path.abspath(__file__))
# Altera o diretório atual para o diretório do ficheiro Python
os.chdir(root_dir)

#######################
#### INÍCIO DA GUI ####
#######################

# Criar a aplicação (app)
app = ctk.CTk()

# Definir o título da janela
app.title("Hoot - Gestor de Filmes e Séries")

# Iniciar o CustomTkinter
ctk.set_appearance_mode("dark")  # Modo claro ou escuro (Pode ser "system", "dark", "light")
ctk.set_default_color_theme("blue")  # Tema padrão (Pode ser "blue", "dark-blue", "green")

# Alterar o ícone da aplicação
app.iconbitmap("./img/hoot.ico")

# Dimensões da interface da app
app_width = 1200
app_height = 675

# Definir o tamanho da janela usando as variáveis
app.geometry(f"{app_width}x{app_height}")  # Largura x Altura

# Obter as dimensões do ecrã (em pixeis)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# App centrada no ecrã, em função das suas dimensões
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
app.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# Definir tamanho mínimo com as variáveis
app.minsize(app_width, app_height)

# Tornar a janela não redimensionável
app.resizable(False, False)

#######################
#### INÍCIO DA APP ####
#######################
splashscreen()
app.after(5000, criar_conta)

# Iniciar o loop da interface gráfica
app.mainloop()