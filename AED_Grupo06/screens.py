# screens.py
import os
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import datetime
import webbrowser
import users
import data_manager
import utils
import CTkMessagebox

root_dir = os.path.dirname(os.path.abspath(__file__))

# Variáveis globais se for preciso
frames = {}
username = None
is_admin = False
dados_geral = []

def splashscreen(app):
    """Ecrã inicial de splash."""
    utils.clear_window(app)

    logo = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'logo.png')), size=(373, 142))
    label_logo = ctk.CTkLabel(app, text="", image=logo)
    label_logo.place(relx=0.5, rely=0.4, anchor="center")

    progress_bar = ctk.CTkProgressBar(app, mode="indeterminate")
    progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
    progress_bar.start()

    # Após 2 segundos, avança para o ecrã de login
    app.after(2000, lambda: ecra_login(app))


def ecra_login(app):
    """Ecrã de login."""
    utils.clear_window(app)
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'promo.png')), size=(468, 675))
    label_promo = ctk.CTkLabel(app, text="", image=promo)
    label_promo.place(relx=0.0, rely=0.5, anchor="w")

    rotulo = ctk.CTkLabel(app, text="Iniciar Sessão",
                          font=("Helvetica", 24, "bold"),
                          text_color="#4F8377")
    rotulo.place(x=513, y=36)

    rotulo_email = ctk.CTkLabel(app, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_email.place(x=513, y=92)
    entry_email = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                               placeholder_text="Insira o seu e-mail",
                               fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_email.place(x=513, y=115)

    rotulo_senha = ctk.CTkLabel(app, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_senha.place(x=513, y=169)
    entry_password = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                                  placeholder_text="Insira a sua palavra-passe",
                                  show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_password.place(x=513, y=191)

    toggle_button = ctk.CTkButton(
        app,
        text="👁",
        font=("Helvetica", 14),
        width=35,
        height=35,
        fg_color="#D9D9D9",
        bg_color="#D9D9D9",
        hover_color="#B0B0B0",
        text_color="#000",
        command=lambda: utils.toggle_password_visibility(entry_password)
    )
    toggle_button.place(x=923, y=195)

    clickable_text = ctk.CTkLabel(
        app,
        text="Esqueceste-te da tua palavra passe?",
        text_color="#4F8377",
        font=("Helvetica", 16, "underline")
    )
    clickable_text.place(x=513, y=246)
    clickable_text.bind("<Button-1>", lambda e: ecra_recuperar_password(app))

    button_iniciar_sessao = ctk.CTkButton(
        app,
        text='INICIAR SESSÃO',
        font=("Helvetica", 14.3, "bold"),
        text_color="#000",
        hover_color="#D59C2A",
        fg_color="#F2C94C",
        width=173,
        height=36,
        command=lambda: users.logIn(
            entry_password.get(),
            entry_email.get(),
            lambda u: login_success(u, app),
            lambda: login_fail(app)
        )
    )
    button_iniciar_sessao.place(x=513, y=297)

    rotulo_criar = ctk.CTkLabel(app, text="Ainda não tens conta?",
                                font=("Helvetica", 24, "bold"),
                                text_color="#4F8377")
    rotulo_criar.place(x=513, y=494)

    rotulo_desc = ctk.CTkLabel(
        app,
        text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores vantagens na Hoot.",
        font=("Helvetica", 16, "bold"),
        text_color="#000",
        justify="left",
        anchor="w",
        wraplength=450
    )
    rotulo_desc.place(x=513, y=540)

    button_criar_conta = ctk.CTkButton(
        app,
        text='CRIAR CONTA',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        width=173,
        height=36,
        command=lambda: criar_conta(app)
    )
    button_criar_conta.place(x=513, y=601)


def ecra_recuperar_password(app):
    """Ecrã para recuperar palavra-passe."""
    utils.clear_window(app)
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'promo.png')), size=(468, 675))
    label_promo = ctk.CTkLabel(app, text="", image=promo)
    label_promo.place(relx=0.0, rely=0.5, anchor="w")

    rotulo = ctk.CTkLabel(app, text="Recuperar Palavra-Passe",
                          font=("Helvetica", 24, "bold"),
                          text_color="#4F8377")
    rotulo.place(x=513, y=36)

    rotulo_user = ctk.CTkLabel(app, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_user.place(x=513, y=112)
    entry_username = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                                  placeholder_text="Insira um username",
                                  fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_username.place(x=513, y=134)

    rotulo_email = ctk.CTkLabel(app, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_email.place(x=513, y=208)
    entry_email = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                               placeholder_text="Insira um e-mail",
                               fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_email.place(x=513, y=231)

    button_criar_conta = ctk.CTkButton(
        app,
        text='ENVIAR INSTRUÇÕES',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        width=173,
        height=36,
        command=lambda: simular_envio_instrucoes(entry_email.get(), app)
    )
    button_criar_conta.place(x=513, y=314)

    button_cancelar = ctk.CTkButton(
        app,
        text='CANCELAR',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        command=lambda: ecra_login(app),
        width=173,
        height=36
    )
    button_cancelar.place(x=713, y=314)


def simular_envio_instrucoes(email, app):
    """Simulação de envio de instruções de recuperação."""
    print(f"A enviar e-mail de recuperação para {email}...")
    ecra_login(app)


def criar_conta(app):
    """Ecrã de criação de conta."""
    utils.clear_window(app)
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'promo.png')), size=(468, 675))
    label_promo = ctk.CTkLabel(app, text="", image=promo)
    label_promo.place(relx=0.0, rely=0.5, anchor="w")

    rotulo = ctk.CTkLabel(app, text="Criar Conta", font=("Helvetica", 24, "bold"), text_color="#4F8377")
    rotulo.place(x=513, y=36)

    rotulo_user = ctk.CTkLabel(app, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_user.place(x=513, y=112)
    entry_username = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                                  placeholder_text="Insira um username",
                                  fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_username.place(x=513, y=134)

    rotulo_email = ctk.CTkLabel(app, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_email.place(x=513, y=208)
    entry_email = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                               placeholder_text="Insira um e-mail",
                               fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_email.place(x=513, y=231)

    rotulo_senha = ctk.CTkLabel(app, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
    rotulo_senha.place(x=513, y=305)
    entry_password = ctk.CTkEntry(app, width=451, height=43, border_width=0,
                                  placeholder_text="Insira uma palavra-passe",
                                  show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
    entry_password.place(x=513, y=328)

    toggle_button = ctk.CTkButton(
        app,
        text="👁",
        font=("Helvetica", 14),
        width=35,
        height=35,
        fg_color="#D9D9D9",
        bg_color="#D9D9D9",
        hover_color="#B0B0B0",
        text_color="#000",
        command=lambda: utils.toggle_password_visibility(entry_password)
    )
    toggle_button.place(x=923, y=332)

    button_criar_conta = ctk.CTkButton(
        app,
        text='CRIAR CONTA',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        width=173,
        height=36,
        command=lambda: users.sign(
            entry_username.get(),
            entry_password.get(),
            entry_email.get(),
            lambda: ecra_login(app)
        )
    )
    button_criar_conta.place(x=513, y=414)

    button_cancelar = ctk.CTkButton(
        app,
        text='CANCELAR',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        command=lambda: ecra_login(app),
        width=173,
        height=36
    )
    button_cancelar.place(x=713, y=414)


def login_success(user, app):
    """Callback de sucesso no login."""
    global username, is_admin, dados_geral
    username = user
    is_admin = users.is_admin(user) if hasattr(users, 'is_admin') else False
    iniciar_frames(app)


def login_fail(app):
    """Callback de falha no login."""
    print("Falha de login.")
    ecra_login(app)


def iniciar_frames(app):
    """Inicializa os frames principais da app."""
    utils.clear_window(app)
    ctk.set_appearance_mode("dark")

    # Criação dos frames para cada ecrã
    frame_series = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
    frame_filmes = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
    frame_explorar = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
    frame_perfil = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")

    frame_series.place(relx=1.0, rely=1.0, anchor="se")
    frame_filmes.place(relx=1.0, rely=1.0, anchor="se")
    frame_explorar.place(relx=1.0, rely=1.0, anchor="se")
    frame_perfil.place(relx=1.0, rely=1.0, anchor="se")

    frames["series"] = frame_series
    frames["filmes"] = frame_filmes
    frames["explorar"] = frame_explorar
    frames["perfil"] = frame_perfil

    # Se for admin, cria o frame_admin
    if is_admin:
        frame_admin = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
        frame_admin.place(relx=1.0, rely=1.0, anchor="se")
        frames["admin"] = frame_admin

    # Frame superior fixo
    top_cover_frame = ctk.CTkFrame(app, width=1050, height=100, fg_color="#242424")
    top_cover_frame.place(x=150, y=0)

    criar_menu_lateral(app)
    atualizar_informacoes_topo(top_cover_frame)

    # Carrega dados
    dados_geral = data_manager.carregar_dados()

    # Inicializa ecrãs
    ecra_series(frame_series)
    ecra_filmes(frame_filmes)
    ecra_explorar(frame_explorar)
    if is_admin:
        ecra_admin(frame_admin)
    else:
        ecra_perfil(frame_perfil)

    frame_series.tkraise()


def criar_menu_lateral(app):
    """Cria o menu lateral."""
    logo_p = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'logo_ui.png')), size=(83, 48))
    label_logo_p = ctk.CTkLabel(app, text="", image=logo_p)
    label_logo_p.place(x=29, y=26)

    linha = ctk.CTkImage(Image.open(os.path.join(root_dir, 'images', 'Line_ecra.png')), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=130, y=151)

    # Botão de séries
    botao_series_image = ctk.CTkImage(Image.open(os.path.join(root_dir, "images", "button_series.png")), size=(68, 89))
    botao_series = ctk.CTkButton(
        app, width=68, height=89, text="", image=botao_series_image,
        fg_color="transparent", hover_color="#181818",
        command=lambda: update_active_screen("series")
    )
    botao_series.place(x=28, y=151)

    # Botão de filmes
    botao_filmes_image = ctk.CTkImage(Image.open(os.path.join(root_dir, "images", "button_filmes.png")), size=(68, 89))
    botao_filmes = ctk.CTkButton(
        app, width=68, height=89, text="", image=botao_filmes_image,
        fg_color="transparent", hover_color="#181818",
        command=lambda: update_active_screen("filmes")
    )
    botao_filmes.place(x=28, y=278)

    # Botão de explorar
    botao_explorar_image = ctk.CTkImage(Image.open(os.path.join(root_dir, "images", "button_explorar.png")), size=(68, 89))
    botao_explorar = ctk.CTkButton(
        app, width=68, height=89, text="", image=botao_explorar_image,
        fg_color="transparent", hover_color="#181818",
        command=lambda: update_active_screen("explorar")
    )
    botao_explorar.place(x=28, y=408)

    # Botão de perfil/admin
    botao_perfil_image = ctk.CTkImage(Image.open(os.path.join(root_dir, "images", "button_perfil.png")), size=(68, 89))
    botao_perfil = ctk.CTkButton(
        app, width=68, height=89, text="", image=botao_perfil_image,
        fg_color="transparent", hover_color="#181818",
        command=lambda: update_active_screen("admin" if is_admin else "perfil")
    )
    botao_perfil.place(x=28, y=534)


def atualizar_informacoes_topo(parent):
    """Mostra avatar e username no top_cover_frame."""
    from PIL import Image
    global username

    user_folder = os.path.join(root_dir, "files", "users", username)
    profile_picture_path = os.path.join(user_folder, "profile_picture.png")
    if os.path.isfile(profile_picture_path):
        image_path = profile_picture_path
    else:
        image_path = os.path.join(root_dir, 'images', 'default_avatar.png')

    image = Image.open(image_path)
    avatar_ctk = ctk.CTkImage(image, size=(55, 55))

    avatar_label = ctk.CTkLabel(parent, text="", image=avatar_ctk)
    avatar_label.place(x=920, y=23)

    label_username_top = ctk.CTkLabel(
        parent,
        text=username,
        font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
        text_color="#a3d9c8"
    )
    label_username_top.place(x=980, y=38)


def update_active_screen(frame_name):
    """Levanta o frame correspondente no dicionário frames."""
    if frame_name in frames:
        frames[frame_name].tkraise()
    else:
        print(f"AVISO: O frame '{frame_name}' não foi encontrado.")


# ----------------- A partir daqui, tens as tuas ecra_series, ecra_filmes, etc. ----------------- #
def ecra_series(parent_frame):
    ...
    # Código adaptado do teu original


def ecra_filmes(parent_frame):
    ...
    # Código adaptado do teu original


def ecra_explorar(parent_frame):
    ...
    # Código adaptado do teu original


def ecra_perfil(parent_frame):
    ...
    # Código adaptado do teu original


def ecra_admin(parent_frame):
    ...
    # Código adaptado do teu original
