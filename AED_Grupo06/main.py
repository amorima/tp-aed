#Ficheiro .py apresentação da aplicação
#Biblioteca
#-----------
import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import users


#######################
####### FUNÇÕES #######
#######################
# Global variable to keep track of the currently selected button
selected_button = None

def toggle_password_visibility(entry):
    """Mostra ou oculta a palavra passe

    Args:
        entry (_type_): _description_
    """
    if entry.cget("show") == "*":
        entry.configure(show="")  # Show the text
    else:
        entry.configure(show="*")  # Hide the text

def limpar_area_central():
    """Remove todos os widgets da área central, mas mantém o menu lateral."""
    for widget in app.winfo_children():
        # Mantém os widgets que fazem parte do menu lateral
        if widget.winfo_x() > 145:  # Assume que o menu lateral ocupa x <= 145
            widget.destroy()

def limpar_todos_widgets():
    for widget in app.winfo_children():
        widget.destroy()
    menu_lateral()

def update_active_screen(button):
    global selected_button
    if selected_button:
        selected_button.configure(fg_color="transparent")  # Reset the previous button's color
    button.configure(fg_color="#181818")  # Set the selected button's color
    selected_button = button

def menu_lateral():
    logo_p = ctk.CTkImage(Image.open('./images/logo_ui.png'), size=(83, 48))
    label_logo_p = ctk.CTkLabel(app, text="", image=logo_p)
    label_logo_p.place(x=29, y=26)

    linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=145, y=151)

    # Carregar a imagem e redimensionar
    botao_series_image = ctk.CTkImage(
        Image.open("./images/button_series.png"),
        size=(68, 89))
    botao_series = ctk.CTkButton(
        app,
        width=68,
        height=89,
        text="",               # Sem texto, apenas a imagem
        image=botao_series_image,
        command=lambda: [update_active_screen(botao_series), ecra_series()],
        fg_color="transparent",   # Fundo transparente para só aparecer a imagem
        hover_color="#181818"     # Cor ao passar o rato (opcional)
    ) 
    # Posicionar o botão
    botao_series.place(x=28, y=151)

    # Carregar a imagem e redimensionar
    botao_filmes_image = ctk.CTkImage(
        Image.open("./images/button_filmes.png"),
        size=(68, 89))
    botao_filmes = ctk.CTkButton(
        app,
        width=68,
        height=89,
        text="",               # Sem texto, apenas a imagem
        image=botao_filmes_image,
        command=lambda: [update_active_screen(botao_filmes), ecra_filmes()],
        fg_color="transparent",   # Fundo transparente para só aparecer a imagem
        hover_color="#181818"     # Cor ao passar o rato (opcional)
    ) 
    # Posicionar o botão
    botao_filmes.place(x=28, y=278)

    # Carregar a imagem e redimensionar
    botao_explorar_image = ctk.CTkImage(
        Image.open("./images/button_explorar.png"),
        size=(68, 89))
    botao_explorar = ctk.CTkButton(
        app,
        width=68,
        height=89,
        text="",               # Sem texto, apenas a imagem
        image=botao_explorar_image,
        command=lambda: [update_active_screen(botao_explorar), ecra_series()],
        fg_color="transparent",   # Fundo transparente para só aparecer a imagem
        hover_color="#181818"     # Cor ao passar o rato (opcional)
    )
    # Posicionar o botão
    botao_explorar.place(x=28, y=408)

    # Carregar a imagem e redimensionar
    botao_perfil_image = ctk.CTkImage(
        Image.open("./images/button_perfil.png"),
        size=(68, 89))
    botao_perfil = ctk.CTkButton(
        app,
        width=68,
        height=89,
        text="",               # Sem texto, apenas a imagem
        image=botao_perfil_image,
        command=lambda: [update_active_screen(botao_perfil), ecra_perfil()],
        fg_color="transparent",   # Fundo transparente para só aparecer a imagem
        hover_color="#181818"     # Cor ao passar o rato (opcional)
    )
    # Posicionar o botão
    botao_perfil.place(x=28, y=534)

def splashscreen():
    """Cria a splashscreen da app."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    # Adicionar o logótipo
    logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
    label_logo = ctk.CTkLabel(app, text="", image=logo)
    label_logo.place(relx=0.5, rely=0.5, anchor="center")  

    # Agendar a transição para a próxima função
    app.after(1500, ecra_login)  # Transita para `iniciar_app` após 3 segundos

def ecra_login():
    """Inicializa a aplicação principal."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
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

    # Button to toggle password visibility
    toggle_button = ctk.CTkButton(app,
                        text="👁",  # Use an eye emoji or another icon
                        font=("Helvetica", 14),
                        width=35,
                        height=35,
                        fg_color="#D9D9D9",
                        bg_color= "#D9D9D9",
                        hover_color="#B0B0B0",
                        text_color="#000",
                        command=lambda:toggle_password_visibility(entry_password))
    toggle_button.place(x=923, y=195)  # Position the button near the password field

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
                           command= lambda:users.logIn(entry_password.get(),entry_email.get(),ecra_series,limpar_todos_widgets),
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
                           hover_color="#3F685F",
                           fg_color="#4F8377",
                           command=lambda:criar_conta(),
                           width=173,
                           height=36)
    button_criar_conta.place(x=513, y=601)

def criar_conta():
    """Inicializa a aplicação principal."""
    # Limpar a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
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

    # Button to toggle password visibility
    toggle_button = ctk.CTkButton(app,
                        text="👁",  # Use an eye emoji or another icon
                        font=("Helvetica", 14),
                        width=35,
                        height=35,
                        fg_color="#D9D9D9",
                        bg_color= "#D9D9D9",
                        hover_color="#B0B0B0",
                        text_color="#000",
                        command=lambda:toggle_password_visibility(entry_password))
    toggle_button.place(x=923, y=332)  # Position the button near the password field


    button_criar_conta = ctk.CTkButton(app,
                           text='CRIAR CONTA',
                           font=("Helvetica", 14.3, "bold"),
                           text_color="#fff",
                           hover_color="#3F685F",
                           fg_color="#4F8377",
                           command=lambda:sign(entry_username.get(),entry_password.get(),entry_email.get(),ecra_login),
                           width=173,
                           height=36)
    button_criar_conta.place(x=513, y=414)

def ecra_series():
    """Renderiza o ecrã principal
    """
    # Limpar a janela atual
    limpar_area_central()
    
    ctk.set_appearance_mode("dark")

    linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=145, y=151)

    mock = ctk.CTkImage(Image.open('./images/series_mockup.png'), size=(894, 521))
    label_mock = ctk.CTkLabel(app, text="", image=mock)
    label_mock.place(x=224, y=108)

def ecra_filmes():
    """Renderiza o ecrã principal
    """
    # Limpar a janela atual
    limpar_area_central()

    linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=145, y=151)

    mock = ctk.CTkImage(Image.open('./images/filmes_mock.png'), size=(894, 521))
    label_mock = ctk.CTkLabel(app, text="", image=mock)
    label_mock.place(x=224, y=108)

def ecra_perfil():
    """Renderiza a dashboard do utilizador
    """
    # Limpar a janela atual
    limpar_area_central()

    # Circular placeholder frame
    placeholder_frame = ctk.CTkFrame(master=app, width=100, height=100, corner_radius=110)
    placeholder_frame.place(x=179, y=151)

    # Label for displaying the image
    global image_label
    image_label = ctk.CTkLabel(master=placeholder_frame, text="", width=100, height=100, bg_color="#242424")
    image_label.place(relx=0.5, rely=0.5, anchor="center")

    # Button for uploading the image (centered in the placeholder)
    upload_button = ctk.CTkButton(
    master=placeholder_frame,
    text="Mudar",
    command=upload_and_save_image,
    font=ctk.CTkFont(size=10, weight="bold"),
    fg_color="transparent",
    bg_color="transparent",  # Transparent button background
    hover_color="#242424",    # Optional hover effect
    text_color="#FFFFFF",     # Text remains visible
    border_width=1,           # Optional border
    border_color="white",   # Border color matches the placeholder
    width=10,
    height=30
    )
    upload_button.place(relx=0.5, rely=0.5, anchor="center")

def ensure_user_folder_exists(username):
    """Garante que a pasta para o utilizador ativo existe."""
    user_folder = os.path.join(root_dir, "files", "users", username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        print(f"Pasta criada para o utilizador: {user_folder}")
    return user_folder

def crop_to_square(image_path):
    """Crop the uploaded image to a square and return the cropped image."""
    with Image.open(image_path) as img:
        width, height = img.size
        side_length = min(width, height)
        left = (width - side_length) // 2
        top = (height - side_length) // 2
        right = left + side_length
        bottom = top + side_length
        return img.crop((left, top, right, bottom))

def apply_circle_mask(image):
    """Apply a circular mask to the image and return it."""
    size = (200, 200)
    image = image.resize(size, Image.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    circular_image = Image.new("RGBA", size)
    circular_image.paste(image, (0, 0), mask)
    return circular_image

def upload_and_save_image():
    """Upload an image, save the cropped version, and render it in a circular frame."""
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        user_folder = ensure_user_folder_exists(users.user_ativo)
        
       
        cropped_image = crop_to_square(file_path)
        
      
        save_path = os.path.join(user_folder, "profile_picture.png")
        cropped_image.save(save_path)
        print(f"Imagem guardada aqui: {save_path}")
        
        # Display the circular version of the cropped image
        circular_image = apply_circle_mask(cropped_image)
        display_image(circular_image)

def display_image(image):
    """Display the circular image in the placeholder."""
    ctk_image = ctk.CTkImage(image, size=(100, 100))
    image_label.configure(image=ctk_image, text="")
    image_label.image = ctk_image

#########################
#### CONFIGURAÇÕES ######
#########################

# Retorna o caminho absoluto do ficheiro Python atualmente em execução
root_dir = os.path.dirname(os.path.abspath(__file__))
# Altera o diretório atual para o diretório do ficheiro Python
os.chdir(root_dir)
#Diretorio dos Ficheiros
USERS_DIR = os.path.join(root_dir, "files", "users")

#######################
#### INÍCIO DA GUI ####
#######################

# Criar a aplicação (app)
app = ctk.CTk()

# Definir o título da janela
app.title("Hoot - Gestor de Filmes e Séries")

# Iniciar o CustomTkinter
ctk.set_appearance_mode("dark")  # Modo claro ou escuro (Pode ser "system", "dark", "light")
ctk.set_default_color_theme("green")  # Tema padrão (Pode ser "blue", "dark-blue", "green")

# Alterar o ícone da aplicação
app.iconbitmap("./images/hoot.ico")

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

# Iniciar o loop da interface gráfica
app.mainloop()