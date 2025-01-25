import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import datetime
import webbrowser
import users
import CTkMessagebox  # Para exibir mensagens de erro/sucesso
from tkinter import ttk  # Para usar Treeview
from tkcalendar import Calendar # Para o selecionador de datas


# ---------- Variáveis Globais ---------- #
app = None
app_width = 1200
app_height = 675

frames = {}
selected_button = None
username = None
is_admin = False

dados_geral = []
dados_series = []
dados_filmes = []

avatar_label = None
label_username_top = None

# As referências para os scrollables de séries/filmes
scroll_left_series = None
scroll_right_series = None
scroll_left_filmes = None
scroll_right_filmes = None

root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

# Modo escuro e tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ----------------- Inicialização da Janela (app) ----------------- #
app = ctk.CTk()
app.title("Hoot - Gestor de Filmes e Séries")
app.iconbitmap("./images/hoot.ico")

# Dimensões fixas + centragem
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()
pos_x = int((screen_w / 2) - (app_width / 2))
pos_y = int((screen_h / 2) - (app_height / 2))
app.geometry(f"{app_width}x{app_height}+{pos_x}+{pos_y}")
app.resizable(False, False)

# Carrega os dados iniciais
dados_geral = []


def splashscreen():
    """Ecrã inicial de splash com logo e barra de progresso."""
    clear_window()

    logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
    label_logo = ctk.CTkLabel(app, text="", image=logo)
    label_logo.place(relx=0.5, rely=0.4, anchor="center")

    progress_bar = ctk.CTkProgressBar(app, mode="indeterminate")
    progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
    progress_bar.start()

    # Após 2 segundos, avança para o ecrã de login
    app.after(2000, ecra_login)


def ecra_login():
    """Ecrã de login."""
    clear_window()
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
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

    # Botão de toggle para visibilidade da password
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
        command=lambda: toggle_password_visibility(entry_password)
    )
    toggle_button.place(x=923, y=195)

    clickable_text = ctk.CTkLabel(
        app,
        text="Esqueceste-te da tua palavra passe?",
        text_color="#4F8377",
        font=("Helvetica", 16, "underline")
    )
    clickable_text.place(x=513, y=246)
    clickable_text.bind("<Button-1>", lambda e: ecra_recuperar_password())

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
            login_success,
            login_fail
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
        command=criar_conta
    )
    button_criar_conta.place(x=513, y=601)


def ecra_recuperar_password():
    """Ecrã para recuperar palavra-passe."""
    clear_window()
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
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
        command=lambda: simular_envio_instrucoes(entry_email.get())
    )
    button_criar_conta.place(x=513, y=314)

    button_cancelar = ctk.CTkButton(
        app,
        text='CANCELAR',
        font=("Helvetica", 14.3, "bold"),
        text_color="#fff",
        hover_color="#3F685F",
        fg_color="#4F8377",
        command=ecra_login,
        width=173,
        height=36
    )
    button_cancelar.place(x=713, y=314)


def simular_envio_instrucoes(email):
    """Simulação de envio de instruções de recuperação."""
    print(f"A enviar e-mail de recuperação para {email}...")
    ecra_login()


def criar_conta():
    """Ecrã de criação de conta."""
    clear_window()
    ctk.set_appearance_mode("light")

    promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
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
        command=lambda: toggle_password_visibility(entry_password)
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
            ecra_login
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
        command=ecra_login,
        width=173,
        height=36
    )
    button_cancelar.place(x=713, y=414)


def carregar_dados():
    """
    Lê o ficheiro 'data.txt' no formato:
    Título;Data de Lançamento;Data Atual;Rating IMDB;URL do Trailer;Sinopse;Duração;Género;Tipo;Caminho da Imagem
    """
    caminho_ficheiro = os.path.join(root_dir, "files", "data.txt")
    lista = []
    if not os.path.exists(caminho_ficheiro):
        return lista

    with open(caminho_ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(";")
            if len(partes) < 10:
                print(f"Linha inválida no ficheiro: {linha}")
                continue

            # Descompactando conforme a nova ordem
            (titulo, data_lancamento, data_atual, rating,
             trailer, sinopse, duracao, genero, tipo, img_path) = partes

            try:
                rating = float(rating)
            except ValueError:
                print(f"Rating inválido para '{titulo}': {rating}")
                rating = 0.0

            item = {
                "titulo": titulo,
                "data_lancamento": data_lancamento,
                "data_atual": data_atual,
                "rating": rating,
                "trailer": trailer,
                "sinopse": sinopse,
                "duracao": duracao,
                "genero": genero,
                "tipo": tipo.lower(),   # "serie" ou "filme"
                "img_path": img_path
            }
            lista.append(item)
    return lista


def login_success(user):
    """
    Callback de sucesso de login. Armazena o username e
    verifica se o utilizador é admin, depois inicializa frames.
    """
    global username, is_admin
    username = user
    is_admin = users.is_admin(user) if hasattr(users, 'is_admin') else False
    iniciar_frames()


def login_fail():
    """Callback de falha de login."""
    print("Falha de login.")
    ecra_login()


def iniciar_frames():
    """
    Limpa a janela e inicializa todos os frames (series, filmes, explorar, perfil/admin).
    Coloca-os em (relx=1.0, rely=1.0, anchor="se") para usar tkraise().
    """
    global frames, dados_geral
    clear_window()
    ctk.set_appearance_mode("dark")

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

    if is_admin:
        frame_admin = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
        frame_admin.place(relx=1.0, rely=1.0, anchor="se")
        frames["admin"] = frame_admin

    top_cover_frame = ctk.CTkFrame(app, width=1050, height=100, fg_color="#242424")
    top_cover_frame.place(x=150, y=0)

    criar_menu_lateral()
    atualizar_informacoes_topo()

    # Carregar/Recarregar dados
    global dados_series, dados_filmes
    dados_geral[:] = carregar_dados()  # substitui o conteúdo em caso de re-inserção

    ecra_series(frame_series)
    ecra_filmes(frame_filmes)
    ecra_explorar(frame_explorar)

    if is_admin:
        ecra_admin(frames["admin"])
    else:
        ecra_perfil(frame_perfil)

    frame_series.tkraise()  # levanta por omissão o ecrã de séries


def criar_menu_lateral():
    """Cria o menu lateral com botões para navegar entre as diferentes abas."""
    logo_p = ctk.CTkImage(Image.open('./images/logo_ui.png'), size=(83, 48))
    label_logo_p = ctk.CTkLabel(app, text="", image=logo_p)
    label_logo_p.place(x=29, y=26)

    linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=130, y=151)

    botao_series_image = ctk.CTkImage(Image.open("./images/button_series.png"), size=(68, 89))
    botao_series = ctk.CTkButton(
        app,
        width=68, height=89,
        text="",
        image=botao_series_image,
        fg_color="transparent",
        hover_color="#181818",
        command=lambda: update_active_screen("series")
    )
    botao_series.place(x=28, y=151)

    botao_filmes_image = ctk.CTkImage(Image.open("./images/button_filmes.png"), size=(68, 89))
    botao_filmes = ctk.CTkButton(
        app,
        width=68, height=89,
        text="",
        image=botao_filmes_image,
        fg_color="transparent",
        hover_color="#181818",
        command=lambda: update_active_screen("filmes")
    )
    botao_filmes.place(x=28, y=278)

    botao_explorar_image = ctk.CTkImage(Image.open("./images/button_explorar.png"), size=(68, 89))
    botao_explorar = ctk.CTkButton(
        app,
        width=68, height=89,
        text="",
        image=botao_explorar_image,
        fg_color="transparent",
        hover_color="#181818",
        command=lambda: update_active_screen("explorar")
    )
    botao_explorar.place(x=28, y=408)

    botao_perfil_image = ctk.CTkImage(Image.open("./images/button_perfil.png"), size=(68, 89))
    botao_perfil = ctk.CTkButton(
        app,
        width=68, height=89,
        text="",
        image=botao_perfil_image,
        fg_color="transparent",
        hover_color="#181818",
        command=lambda: update_active_screen("admin" if is_admin else "perfil")
    )
    botao_perfil.place(x=28, y=534)


def atualizar_informacoes_topo():
    """Atualiza a zona de topo com o avatar e o username do utilizador."""
    global avatar_label, label_username_top

    user_folder = os.path.join(root_dir, "files", "users", username)
    profile_picture_path = os.path.join(user_folder, "profile_picture.png")

    if os.path.isfile(profile_picture_path):
        image_path = profile_picture_path
    else:
        image_path = './images/default_avatar.png'

    image = Image.open(image_path)
    avatar = ctk.CTkImage(image, size=(55, 55))

    avatar_label = ctk.CTkLabel(app, text="", image=avatar)
    avatar_label.place(x=1100, y=23)

    label_username_top = ctk.CTkLabel(
        app,
        text=username,
        font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
        anchor="e",
        text_color="#a3d9c8",
        width=200
    )
    label_username_top.place(x=1075 - 200, y=38)  # x = posição final - largura do label


def ecra_series(parent_frame):
    """
    Aba de Séries. Apresenta duas colunas (Para ver / Brevemente),
    com filtragem por género e ano. Filtra apenas tipo="serie".
    """
    global scroll_left_series, scroll_right_series, dados_series

    label_series_ver = ctk.CTkLabel(
        parent_frame,
        text='Para ver',
        font=("Helvetica", 18, "bold"),
        fg_color='transparent'
    )
    label_series_ver.place(x=10, y=0)

    label_series_brev = ctk.CTkLabel(
        parent_frame,
        text='Brevemente',
        font=("Helvetica", 18, "bold"),
        fg_color='transparent'
    )
    label_series_brev.place(x=520, y=0)

    scroll_left_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
    scroll_left_series.place(x=10, y=30)

    scroll_right_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
    scroll_right_series.place(x=520, y=30)

    # Gera lista de séries
    dados_series = [x for x in dados_geral if x["tipo"] == "serie"]

    filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    filtro_frame.place(relx=1.0, y=0, x=-48, anchor="ne")

    generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance", "Ação", "Comédia", "Ficção Científica", "Terror"]
    filtro_genero_series = ctk.CTkOptionMenu(filtro_frame, values=generos_possiveis, width=80)
    filtro_genero_series.set("Todos")
    filtro_genero_series.grid(row=0, column=0, padx=5)

    filtro_ano_series = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
    filtro_ano_series.grid(row=0, column=1, padx=5)

    botao_filtrar_series = ctk.CTkButton(
        filtro_frame,
        text="Filtrar",
        width=60,
        command=lambda: aplicar_filtro_series(filtro_genero_series.get(),
                                              filtro_ano_series.get())
    )
    botao_filtrar_series.grid(row=0, column=2, padx=5)

    mostrar_series_filtradas()


def aplicar_filtro_series(genero_selecionado, ano_texto):
    global scroll_left_series, scroll_right_series, dados_series

    lista_filtrada = []
    for item in dados_series:
        if genero_selecionado != "Todos" and item["genero"] != genero_selecionado:
            continue
        if ano_texto.strip():
            try:
                ano_int = int(ano_texto.strip())
                ano_lancamento = int(item["data_lancamento"].split("/")[-1])
                if ano_lancamento != ano_int:
                    continue
            except ValueError:
                print(f"Ano inválido: {ano_texto}")
                continue
        lista_filtrada.append(item)

    for child in scroll_left_series.winfo_children():
        child.destroy()
    for child in scroll_right_series.winfo_children():
        child.destroy()

    ano_hoje = datetime.date.today().year
    lista_passado = []
    lista_futuro = []

    for item in lista_filtrada:
        try:
            ano_lancamento = int(item["data_lancamento"].split("/")[-1])
            if ano_lancamento <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)
        except ValueError:
            print(f"Data inválida no item: {item['titulo']}")
            continue

    criar_cards(lista_passado, scroll_left_series)
    criar_cards(lista_futuro, scroll_right_series)


def mostrar_series_filtradas():
    global scroll_left_series, scroll_right_series, dados_series

    for child in scroll_left_series.winfo_children():
        child.destroy()
    for child in scroll_right_series.winfo_children():
        child.destroy()

    ano_hoje = datetime.date.today().year
    lista_passado = []
    lista_futuro = []

    for item in dados_series:
        try:
            ano_lancamento = int(item["data_lancamento"].split("/")[-1])
            if ano_lancamento <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)
        except ValueError:
            print(f"Data inválida no item: {item['titulo']}")
            continue

    criar_cards(lista_passado, scroll_left_series)
    criar_cards(lista_futuro, scroll_right_series)


def ecra_filmes(parent_frame):
    """
    Aba de Filmes, semelhante a séries mas filtra tipo="filme".
    """
    global scroll_left_filmes, scroll_right_filmes, dados_filmes

    label_filmes_ver = ctk.CTkLabel(
        parent_frame,
        text='Para ver',
        font=("Helvetica", 18, "bold"),
        fg_color='transparent'
    )
    label_filmes_ver.place(x=10, y=0)

    label_filmes_brev = ctk.CTkLabel(
        parent_frame,
        text='Brevemente',
        font=("Helvetica", 18, "bold"),
        fg_color='transparent'
    )
    label_filmes_brev.place(x=520, y=0)

    scroll_left_filmes = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
    scroll_left_filmes.place(x=10, y=30)

    scroll_right_filmes = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
    scroll_right_filmes.place(x=520, y=30)

    dados_filmes = [x for x in dados_geral if x["tipo"] == "filme"]

    filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    filtro_frame.place(relx=1.0, y=0, x=-48, anchor="ne")

    generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance", "Ação", "Comédia", "Ficção Científica", "Terror"]
    filtro_genero_filmes = ctk.CTkOptionMenu(filtro_frame, values=generos_possiveis, width=80)
    filtro_genero_filmes.set("Todos")
    filtro_genero_filmes.grid(row=0, column=0, padx=5)

    filtro_ano_filmes = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
    filtro_ano_filmes.grid(row=0, column=1, padx=5)

    botao_filtrar_filmes = ctk.CTkButton(
        filtro_frame,
        text="Filtrar",
        width=60,
        command=lambda: aplicar_filtro_filmes(filtro_genero_filmes.get(), filtro_ano_filmes.get())
    )
    botao_filtrar_filmes.grid(row=0, column=2, padx=5)

    mostrar_filmes_filtradas()


def aplicar_filtro_filmes(genero_selecionado, ano_texto):
    global scroll_left_filmes, scroll_right_filmes, dados_filmes

    lista_filtrada = []
    for item in dados_filmes:
        if genero_selecionado != "Todos" and item["genero"] != genero_selecionado:
            continue
        if ano_texto.strip():
            try:
                ano_int = int(ano_texto.strip())
                ano_lancamento = int(item["data_lancamento"].split("/")[-1])
                if ano_lancamento != ano_int:
                    continue
            except ValueError:
                print(f"Ano inválido: {ano_texto}")
                continue
        lista_filtrada.append(item)

    for child in scroll_left_filmes.winfo_children():
        child.destroy()
    for child in scroll_right_filmes.winfo_children():
        child.destroy()

    ano_hoje = datetime.date.today().year
    lista_passado = []
    lista_futuro = []

    for item in lista_filtrada:
        try:
            ano_lancamento = int(item["data_lancamento"].split("/")[-1])
            if ano_lancamento <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)
        except ValueError:
            print(f"Data inválida no item: {item['titulo']}")
            continue

    criar_cards(lista_passado, scroll_left_filmes)
    criar_cards(lista_futuro, scroll_right_filmes)


def mostrar_filmes_filtradas():
    global scroll_left_filmes, scroll_right_filmes, dados_filmes

    for child in scroll_left_filmes.winfo_children():
        child.destroy()
    for child in scroll_right_filmes.winfo_children():
        child.destroy()

    ano_hoje = datetime.date.today().year
    lista_passado = []
    lista_futuro = []

    for item in dados_filmes:
        try:
            ano_lancamento = int(item["data_lancamento"].split("/")[-1])
            if ano_lancamento <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)
        except ValueError:
            print(f"Data inválida no item: {item['titulo']}")
            continue

    criar_cards(lista_passado, scroll_left_filmes)
    criar_cards(lista_futuro, scroll_right_filmes)


def ecra_explorar(parent_frame):
    scroll_left = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
    scroll_left.place(x=10, y=0)

    scroll_right = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
    scroll_right.place(x=520, y=0)


def ecra_perfil(parent_frame):
    scrollable_content_perfil = ctk.CTkScrollableFrame(
        parent_frame,
        width=1050,
        height=540,
        fg_color="#242424"
    )
    scrollable_content_perfil.place(x=-1, y=-1)

    top_area = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    top_area.pack(fill="x", padx=20, pady=15)

    avatar_holder = ctk.CTkFrame(top_area, width=100, height=100, corner_radius=50, fg_color="#242424")
    avatar_holder.pack(side="left", anchor="nw")

    local_avatar_label = ctk.CTkLabel(avatar_holder, text="", width=100, height=100)
    local_avatar_label.place(relx=0.5, rely=0.5, anchor="center")

    user_folder = os.path.join(root_dir, "files", "users", username)
    if os.path.exists(user_folder):
        image_path = os.path.join(user_folder, "profile_picture.png")
    else:
        image_path = './images/default_avatar.png'
    avatar_image = ctk.CTkImage(Image.open(image_path), size=(100, 100))
    local_avatar_label.configure(image=avatar_image, text="")

    upload_button = ctk.CTkButton(
        avatar_holder,
        text="✍",
        command=lambda: upload_avatar(local_avatar_label),
        font=ctk.CTkFont(size=30, weight="bold"),
        fg_color="transparent",
        hover_color="#2A2A2A",
        text_color="#FFFFFF",
        border_width=1,
        border_color="white",
        width=10,
        height=30
    )
    upload_button.place(relx=0.5, rely=0.5, anchor="center")

    user_info_frame = ctk.CTkFrame(top_area, fg_color="#242424")
    user_info_frame.pack(side="left", padx=20)

    label_username_local = ctk.CTkLabel(
        user_info_frame,
        text=username,
        font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
        text_color="#a3d9c8"
    )
    label_username_local.pack(anchor="w")

    edit_button = ctk.CTkButton(
        user_info_frame,
        text="EDITAR",
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="transparent",
        hover_color="#1A1A1A",
        text_color="#FFFFFF",
        border_width=2,
        border_color="#FFFFFF",
        width=80,
        command=lambda: print("Ir para edição do perfil...")
    )
    edit_button.pack(anchor="w", pady=(10, 0))

    counters_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    counters_frame.pack(fill="x", padx=20)

    counters_data = [
        ("a seguir", "43"),
        ("seguidores", "43"),
        ("comentários", "43"),
        ("gostos", "43"),
        ("partilhas", "43"),
    ]

    for label_text, label_value in counters_data:
        container = ctk.CTkFrame(counters_frame, width=177, height=89, fg_color="#242424", border_color="#84C7B9", border_width=2)
        container.pack(side="left", padx=5)
        container.pack_propagate(False)
        valor = ctk.CTkLabel(container, text=label_value, font=("Helvetica", 20, "bold"))
        valor.pack(anchor="n", pady=(15, 0))
        texto = ctk.CTkLabel(container, text=label_text, font=("Helvetica", 12))
        texto.pack()

    stats_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Estatísticas",
        font=("Helvetica", 20, "bold"),
        text_color="#84C7B9"
    )
    stats_label.pack(anchor="w", padx=20, pady=(20, 5))

    stats_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    stats_frame.pack(fill="x", padx=20)

    stats_data = [
        ("horas a ver séries", "43"),
        ("episódios vistos", "43"),
        ("horas a ver filmes", "43"),
        ("filmes vistos", "43"),
    ]

    for label_text, label_value in stats_data:
        container = ctk.CTkFrame(stats_frame, width=177, height=89, fg_color="#242424", border_color="#84C7B9", border_width=2)
        container.pack(side="left", padx=5)
        container.pack_propagate(False)
        valor = ctk.CTkLabel(container, text=label_value, font=("Helvetica", 20, "bold"))
        valor.pack(anchor="n", pady=(15, 0))
        texto = ctk.CTkLabel(container, text=label_text, font=("Helvetica", 12))
        texto.pack()

    lists_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Listas",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    lists_label.pack(anchor="w", padx=20, pady=(20, 5))

    # Frame onde será mostrada a Treeview com as listas do utilizador
    lists_container = ctk.CTkFrame(scrollable_content_perfil, fg_color="#1A1A1A", width=750, height=150, corner_radius=6)
    lists_container.pack(anchor="w", padx=20, pady=5)

    # Cria a Treeview dentro do lists_container
    create_list_treeview(lists_container)

    # Botão para criar uma nova lista
    create_list_button = ctk.CTkButton(
        scrollable_content_perfil,
        text="+\nCRIAR NOVA LISTA",
        font=("Helvetica", 14, "bold"),
        fg_color="#4F8377",
        text_color="#FFFFFF",
        hover_color="#3F685F",
        height=150,
        command=lambda: criar_lista_modal()
    )
    # Ajuste de posição conforme seu layout (exemplo):
    create_list_button.place(x=793, y=lists_container.winfo_y() + 419)

    series_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Séries",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    series_label.pack(anchor="w", padx=20, pady=(20, 5))

    series_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    series_frame.pack(anchor="w", padx=20)

    series_posters = [
        "./images/catalog/hp1.jpg",
        "./images/terra_indomavel.png",
        "./images/agora_estamos.png",
        "./images/perfil_falso.png",
        "./images/got.png",
        "./images/breaking_bad.png",
        "./images/anne_with_e.png"
    ]
    for poster_path in series_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None

        lbl_poster = ctk.CTkLabel(series_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    fav_series_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Séries Favoritas",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    fav_series_label.pack(anchor="w", padx=20, pady=(20, 5))

    fav_series_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    fav_series_frame.pack(anchor="w", padx=20)

    fav_series_posters = [
        "./images/departure.png",
        "./images/from.png",
        "./images/tieta.png",
        "./images/o_mundo_dos_casados.png"
    ]
    for poster_path in fav_series_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None

        lbl_poster = ctk.CTkLabel(fav_series_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    movies_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Filmes",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    movies_label.pack(anchor="w", padx=20, pady=(20, 5))

    movies_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    movies_frame.pack(anchor="w", padx=20)

    movies_posters = [
        "./images/poderoso_chefao.png",
        "./images/sonho_de_liberdade.png",
        "./images/lista_de_schindler.png",
        "./images/forrest_gump.png",
        "./images/rei_leao.png",
        "./images/espera_de_um_milagre.png",
        "./images/senhor_anel.png"
    ]
    for poster_path in movies_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None

        lbl_poster = ctk.CTkLabel(movies_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    fav_movies_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Filmes Favoritos",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    fav_movies_label.pack(anchor="w", padx=20, pady=(20, 5))

    fav_movies_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    fav_movies_frame.pack(anchor="w", padx=20)

    fav_movies_posters = [
        "./images/senhor_aneis.png",
        "./images/batman_cavaleiro_trevas.png",
        "./images/a_vida_e_bela.png"
    ]
    for poster_path in fav_movies_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None

        lbl_poster = ctk.CTkLabel(fav_movies_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)


def ecra_admin(parent_frame):
    scrollable_content_admin = ctk.CTkScrollableFrame(
        parent_frame,
        width=1050,
        height=540,
        fg_color="#242424"
    )
    scrollable_content_admin.place(x=-1, y=-1)

    label = ctk.CTkLabel(scrollable_content_admin,
                         text="Área de Admin",
                         font=("Helvetica", 24, "bold"),
                         text_color="#4F8377")
    label.pack(pady=10)

    btn_users = ctk.CTkButton(
        scrollable_content_admin,
        text="Gerir Utilizadores",
        fg_color="#4F8377",
        command=gerir_utilizadores
    )
    btn_users.pack(pady=5)

    btn_categorias = ctk.CTkButton(
        scrollable_content_admin,
        text="Gerir Categorias",
        fg_color="#4F8377",
        command=gerir_categorias
    )
    btn_categorias.pack(pady=5)

    btn_dashboard = ctk.CTkButton(
        scrollable_content_admin,
        text="Dashboard Admin",
        fg_color="#4F8377",
        command=ecra_dashboard_admin
    )
    btn_dashboard.pack(pady=5)

    btn_inserir_conteudo = ctk.CTkButton(
        scrollable_content_admin,
        text="Inserir Filme/Série",
        fg_color="#4F8377",
        command=ecra_inserir
    )
    btn_inserir_conteudo.pack(pady=5)


def gerir_utilizadores():
    print("Gerir Utilizadores: criar ecrã/modal para listar, bloquear ou remover utilizadores.")


def gerir_categorias():
    print("Gerir Categorias: criar ecrã para adicionar/editar/remover categorias.")


def ecra_dashboard_admin():
    print("Dashboard Admin: criar gráficos e estatísticas para administradores.")


def ecra_inserir():
    """Cria um modal (CTkToplevel) para adicionar um filme/série."""
    global dados_geral

    # Criação do modal
    modal = ctk.CTkToplevel(app)
    modal.title("Adicionar Filme/Série")

    # Centrar o modal na janela principal
    modal_width = 500
    modal_height = 600
    x_app = app.winfo_x()
    y_app = app.winfo_y()
    new_x = x_app + (app_width // 2) - (modal_width // 2)
    new_y = y_app + (app_height // 2) - (modal_height // 2)
    modal.geometry(f"{modal_width}x{modal_height}+{new_x}+{new_y}")
    modal.resizable(False, False)
    modal.attributes("-topmost", True)
    modal.iconbitmap(bitmap=".//images//hoot.ico")

    # Frame principal scrollable
    scrollable_frame = ctk.CTkScrollableFrame(modal, width=modal_width, corner_radius=6, fg_color="#242424")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Título do modal
    ctk.CTkLabel(
        scrollable_frame,
        text="Adicionar Filme/Série",
        font=("Helvetica", 24, "bold"),
        text_color="#ffffff"
    ).pack(pady=(0, 20))  # Espaço maior abaixo do título principal

    # Campos de entrada
    entries = {}

    # Título
    ctk.CTkLabel(scrollable_frame, text="Título", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["titulo"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["titulo"].pack(pady=(0, 20))

    # Data de Lançamento
    ctk.CTkLabel(scrollable_frame, text="Data de Lançamento", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    date_button = ctk.CTkButton(scrollable_frame, text="Selecionar Data")
    date_button.pack(pady=(0, 5))
    entries["data_lancamento"] = ctk.CTkLabel(scrollable_frame, text="Sem data selecionada", text_color="#ffffff")
    entries["data_lancamento"].pack(pady=(0, 20))

    def escolher_data():
        """Abre um date picker e atualiza o label com a data selecionada."""
        from tkcalendar import Calendar

        date_picker = tk.Toplevel(app)
        date_picker.title("Escolher Data")

        def selecionar_data():
            selected_date = cal.get_date()
            entries["data_lancamento"].configure(text=selected_date)
            date_picker.destroy()

        cal = Calendar(date_picker, selectmode="day", date_pattern="dd/MM/yyyy")
        cal.pack(pady=20)

        tk.Button(date_picker, text="Confirmar", command=selecionar_data).pack(pady=10)

    date_button.configure(command=escolher_data)

    # Rating IMDB
    ctk.CTkLabel(scrollable_frame, text="Rating IMDB (0-10)", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["rating"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["rating"].pack(pady=(0, 20))

    # URL do Trailer
    ctk.CTkLabel(scrollable_frame, text="URL do Trailer", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["trailer"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["trailer"].pack(pady=(0, 20))

    # Sinopse
    ctk.CTkLabel(scrollable_frame, text="Sinopse", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["sinopse"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["sinopse"].pack(pady=(0, 20))

    # Duração
    ctk.CTkLabel(scrollable_frame, text="Duração (minutos)", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["duracao"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["duracao"].pack(pady=(0, 20))

    # Género
    ctk.CTkLabel(scrollable_frame, text="Género", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    generos_disponiveis = ["Ação", "Comédia", "Drama", "Fantasia", "Ficção Científica", "Terror", "Romance", "Aventura"]
    entries["genero"] = ctk.CTkOptionMenu(scrollable_frame, values=generos_disponiveis)
    entries["genero"].set("Ação")
    entries["genero"].pack(pady=(0, 20))

    # Tipo de Conteúdo (Radio Buttons)
    ctk.CTkLabel(scrollable_frame, text="Tipo de Conteúdo", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    tipo_var = tk.StringVar(value="serie")
    tipo_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    tipo_frame.pack(pady=(0, 20))
    radio_serie = ctk.CTkRadioButton(tipo_frame, text="Série", variable=tipo_var, value="serie")
    radio_filme = ctk.CTkRadioButton(tipo_frame, text="Filme", variable=tipo_var, value="filme")
    radio_serie.pack(side="left", padx=10)
    radio_filme.pack(side="left", padx=10)

    # Upload de Imagem
    ctk.CTkLabel(scrollable_frame, text="Carregar Imagem", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    img_label = ctk.CTkLabel(scrollable_frame, text="Nenhuma imagem carregada", text_color="#ffffff")
    img_label.pack(pady=(0, 10))

    def fazer_upload_imagem():
        file_path = filedialog.askopenfilename(
            title="Selecionar uma imagem",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            catalog_dir = os.path.join(root_dir, "images", "catalog")
            if not os.path.exists(catalog_dir):
                os.makedirs(catalog_dir)

            img_filename = os.path.basename(file_path)
            new_img_path = os.path.join(catalog_dir, img_filename)

            with Image.open(file_path) as img:
                img.save(new_img_path)

            img_label.configure(text=f"Imagem carregada: {img_filename}")
            entries["img_path"] = f".//images//catalog//{img_filename}"

    btn_upload = ctk.CTkButton(scrollable_frame, text="Selecionar Imagem", command=fazer_upload_imagem)
    btn_upload.pack(pady=(0, 20))

    # Botões para salvar ou cancelar
    def salvar_dados():
        """
        Salva os dados no ficheiro data.txt no formato:
        Título;Data de Lançamento;Data Atual;Rating IMDB;URL do Trailer;Sinopse;Duração;Género;Tipo;Caminho da Imagem
        """
        titulo = entries["titulo"].get().strip()
        data_lancamento = entries["data_lancamento"].cget("text").strip()
        rating = entries["rating"].get().strip()
        trailer = entries["trailer"].get().strip()
        sinopse = entries["sinopse"].get().strip()
        duracao = entries["duracao"].get().strip()
        genero = entries["genero"].get().strip()
        tipo = tipo_var.get()
        img_path = entries.get("img_path", "")

        if not (titulo and data_lancamento and rating and trailer and sinopse and duracao and genero and img_path):
            print("Por favor, preencha todos os campos.")
            return

        try:
            rating = float(rating)
        except ValueError:
            print("Rating inválido. Deve ser um número entre 0 e 10.")
            return

        # Data atual
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

        # Formato do registo
        novo_registo = (f"{titulo};{data_lancamento};{data_atual};{rating};"
                        f"{trailer};{sinopse};{duracao};{genero};{tipo};{img_path}\n")

        caminho_ficheiro = os.path.join(root_dir, "files", "data.txt")

        # Guardar o registo no ficheiro
        with open(caminho_ficheiro, "a", encoding="utf-8") as f:
            f.write(novo_registo)

        print("Dados guardados com sucesso.")
        modal.destroy()


    ctk.CTkButton(scrollable_frame, text="Guardar", command=salvar_dados, fg_color="#4F8377").pack(pady=(20, 10))
    ctk.CTkButton(scrollable_frame, text="Cancelar", command=modal.destroy, fg_color="#D9534F").pack(pady=(0, 20))


def escolher_data(entry):
    """Abre um date picker e insere a data selecionada no campo."""
    date_picker = tk.Toplevel(app)
    date_picker.title("Escolher Data")

    def selecionar_data():
        entry.delete(0, "end")
        entry.insert(0, cal.get_date())
        date_picker.destroy()

    cal = Calendar(date_picker, selectmode="day", date_pattern="dd/MM/yyyy")
    cal.pack(pady=20)

    tk.Button(date_picker, text="Confirmar", command=selecionar_data).pack(pady=10)


def clear_window():
    """Remove todos os widgets/frames da janela."""
    for widget in app.winfo_children():
        widget.destroy()


def update_active_screen(frame_name):
    global avatar_label, label_username_top

    if frame_name in frames:
        if frame_name in ["perfil", "admin", "inserir"]:
            if avatar_label:
                avatar_label.place_forget()
            if label_username_top:
                label_username_top.place_forget()
        else:
            if avatar_label:
                avatar_label.place(x=1100, y=23)
            if label_username_top:
                label_username_top.place(x=1000, y=38)

        frames[frame_name].tkraise()
    else:
        print(f"AVISO: O frame '{frame_name}' não foi encontrado em frames.")


def toggle_password_visibility(entry: ctk.CTkEntry):
    """Ativa/desativa a visibilidade do texto no campo de password."""
    if entry.cget("show") == "*":
        entry.configure(show="")
    else:
        entry.configure(show="*")


def upload_avatar(image_label: ctk.CTkLabel):
    """Seleciona e recorta uma imagem para usar como avatar."""
    global avatar_label
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not file_path:
        return

    user_folder = os.path.join(root_dir, "files", "users", username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    with Image.open(file_path) as img:
        largura, altura = img.size
        lado = min(largura, altura)
        esquerda = (largura - lado) // 2
        topo = (altura - lado) // 2
        direita = esquerda + lado
        fundo = topo + lado
        recortada = img.crop((esquerda, topo, direita, fundo))

    tamanho = (500, 500)
    recortada = recortada.resize(tamanho, Image.Resampling.LANCZOS)
    mascara = Image.new("L", tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho[0], tamanho[1]), fill=255)
    circular = Image.new("RGBA", tamanho)
    circular.paste(recortada, (0, 0), mascara)

    caminho_guardar = os.path.join(user_folder, "profile_picture.png")
    circular.save(caminho_guardar)

    ctk_image = ctk.CTkImage(circular, size=(100, 100))
    image_label.configure(image=ctk_image, text="")
    image_label.image = ctk_image

    if avatar_label is not None:
        topo_img = ctk.CTkImage(circular, size=(55, 55))
        avatar_label.configure(image=topo_img, text="")
        avatar_label.image = topo_img


def criar_cards(lista, parent_frame):
    """Cria 'cards' para cada item da lista, numa grelha dentro de um CTkScrollableFrame."""
    for item in lista:
        cat_img_path = item["img_path"]
        movie_name = item["titulo"]
        sinopse = item["sinopse"]
        trailer = item["trailer"]
        rating = str(item["rating"])
        duracao = item["duracao"]

        try:
            year = int(item["data_lancamento"].split("/")[-1])
        except ValueError:
            year = 0

        try:
            card_image = Image.open(cat_img_path).resize((100, 148), Image.Resampling.LANCZOS)
            mascara = Image.new("L", card_image.size, 0)
            draw = ImageDraw.Draw(mascara)
            draw.rounded_rectangle([(0, 0), card_image.size], radius=6, fill=255)
            arredondada = Image.new("RGBA", card_image.size)
            arredondada.paste(card_image, (0, 0), mascara)

            card_frame = ctk.CTkFrame(parent_frame, width=110, height=158)
            card_frame.grid_propagate(False)
            imagem_ctk = ctk.CTkImage(arredondada, size=(100, 148))
            card_label = ctk.CTkLabel(card_frame, image=imagem_ctk, text="")
            card_label.pack(expand=True)

            num_cards = len(parent_frame.winfo_children())
            colunas = 4
            linha = (num_cards - 1) // colunas
            coluna = (num_cards - 1) % colunas
            card_frame.grid(row=linha, column=coluna, padx=5, pady=5)

            def on_click(event):
                mostrar_detalhes_filme(movie_name, sinopse, trailer, rating, year, duracao)

            card_frame.bind("<Button-1>", on_click)
            card_label.bind("<Button-1>", on_click)

        except (FileNotFoundError, IOError):
            print(f"Erro ao carregar a imagem: {cat_img_path}")


def mostrar_detalhes_filme(movie_name, sinopse, trailer, rating, year, duracao):
    """Mostra detalhes do item num frame sobreposto (pop-up)."""
    detalhes_frame = ctk.CTkFrame(app, width=800, height=500, corner_radius=6, fg_color="#4f8377")
    detalhes_frame.place(relx=0.5, rely=0.5, anchor="center")

    botao_fechar = ctk.CTkButton(
        detalhes_frame,
        text="X",
        width=30,
        command=detalhes_frame.destroy,
        fg_color="#a3d9c8",
        text_color="#242424"
    )
    botao_fechar.place(x=760, y=10)

    titulo = ctk.CTkLabel(
        detalhes_frame,
        text=movie_name,
        font=("Helvetica", 24, "bold"),
        text_color="#ffffff"
    )
    titulo.place(x=20, y=20)

    lbl_sinopse = ctk.CTkLabel(
        detalhes_frame,
        text=sinopse,
        font=("Helvetica", 12),
        text_color="#ffffff",
        wraplength=700
    )
    lbl_sinopse.place(x=20, y=60)

    info = ctk.CTkLabel(
        detalhes_frame,
        text=f"Rating: {rating} | Ano: {year} | Duração: {duracao} min",
        font=("Helvetica", 12, "bold"),
        text_color="#ffffff"
    )
    info.place(x=20, y=460)



def criar_lista_modal():
    """
    Abre um CTkToplevel centrado em relação a 'app', com mesmo ícone,
    pedindo o nome da lista. Cria ficheiro .txt em ./files/users/<user>/listas/.
    """
    modal = ctk.CTkToplevel(app)
    modal.title("Criar Nova Lista")

    # Define o ícone igual ao da janela principal
    modal.iconbitmap(".//images//hoot.ico")

    # Dimensões do modal
    width_modal = 400
    height_modal = 200

    # Cálculo para centrar em relação a app
    x_app = app.winfo_x()
    y_app = app.winfo_y()
    new_x = x_app + (app_width // 2) - (width_modal // 2)
    new_y = y_app + (app_height // 2) - (height_modal // 2)

    modal.geometry(f"{width_modal}x{height_modal}+{new_x}+{new_y}")
    modal.resizable(False, False)
    modal.attributes("-topmost", True)

    label_info = ctk.CTkLabel(modal, text="Nome da Lista:", font=("Helvetica", 14))
    label_info.pack(padx=20, pady=10)

    entry_nome = ctk.CTkEntry(modal, width=250)
    entry_nome.pack(padx=20, pady=10)

    def criar():
        list_name = entry_nome.get().strip()
        if not list_name:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message="Introduza um nome válido para a lista.",
                icon="warning"
            )
            return

        user_folder = os.path.join(root_dir, "files", "users", username)
        lists_folder = os.path.join(user_folder, "listas")
        if not os.path.exists(lists_folder):
            os.makedirs(lists_folder)

        list_path = os.path.join(lists_folder, list_name + ".txt")

        if os.path.exists(list_path):
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message="A lista já existe, escolha outro nome.",
                icon="warning"
            )
            return

        # Cria o ficheiro (vazio)
        with open(list_path, "w", encoding="utf-8"):
            pass

        CTkMessagebox.CTkMessagebox(
            title="Sucesso",
            message=f"Lista '{list_name}' criada com sucesso!",
            icon="check"
        )
        modal.destroy()
        # Atualiza a treeview
        for widget in frames["perfil"].winfo_children():
            widget.destroy()
        ecra_perfil(frames["perfil"])

    btn_criar = ctk.CTkButton(modal, text="Criar", command=criar, fg_color="#4F8377")
    btn_criar.pack(padx=20, pady=(0, 5))

    btn_cancel = ctk.CTkButton(modal, text="Cancelar", command=modal.destroy, fg_color="#D9534F")
    btn_cancel.pack(padx=20, pady=(0, 10))


def create_list_treeview(lists_container):
    """
    Cria uma Treeview dentro do frame lists_container, preenchendo
    com os ficheiros (listas) existentes em ./files/users/<user>/listas/.
    """
    # Criar a tree e definir colunas
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#1A1A1A",
                    foreground="white",
                    rowheight=24,
                    fieldbackground="#1A1A1A")
    style.map("Treeview", background=[("selected", "#4F8377")])

    tree = ttk.Treeview(lists_container, columns=("Lista"), show="headings", selectmode="browse")
    tree.heading("Lista", text="Nome da Lista")
    tree.column("Lista", width=725, anchor="w")

    tree.place(x=0, y=0, width=750, height=150)

    # Carregar dados das listas
    user_folder = os.path.join(root_dir, "files", "users", username)
    lists_folder = os.path.join(user_folder, "listas")

    if not os.path.exists(lists_folder):
        os.makedirs(lists_folder)

    for ficheiro in os.listdir(lists_folder):
        if ficheiro.endswith(".txt"):
            lista_nome = ficheiro[:-4]
            tree.insert("", "end", values=(lista_nome,))

    # Ao dar duplo clique na row, abrimos o modal com o conteúdo
    def on_double_click(event):
        selected = tree.selection()
        if not selected:
            return
        item = selected[0]
        lista_nome = tree.item(item, "values")[0]
        ver_conteudo_lista(lista_nome)

    tree.bind("<Double-1>", on_double_click)


def ver_conteudo_lista(list_name):
    """
    Abre um CTkToplevel com todas as linhas (séries/filmes) contidas no ficheiro da lista,
    centrado e com o mesmo ícone que a app principal.
    """
    modal_lista = ctk.CTkToplevel(app)
    modal_lista.title(f"Conteúdo da lista: {list_name}")
    modal_lista.iconbitmap("./images/hoot.ico")

    width_modal = 400
    height_modal = 400

    x_app = app.winfo_x()
    y_app = app.winfo_y()
    new_x = x_app + (app_width // 2) - (width_modal // 2)
    new_y = y_app + (app_height // 2) - (height_modal // 2)

    modal_lista.geometry(f"{width_modal}x{height_modal}+{new_x}+{new_y}")
    modal_lista.resizable(False, False)

    user_folder = os.path.join(root_dir, "files", "users", username)
    lists_folder = os.path.join(user_folder, "listas")
    list_path = os.path.join(lists_folder, list_name + ".txt")

    label_titulo = ctk.CTkLabel(modal_lista,
                                text=f"Itens da lista '{list_name}'",
                                font=("Helvetica", 16, "bold"))
    label_titulo.pack(pady=10)

    frame_scroll = ctk.CTkScrollableFrame(modal_lista, width=360, height=300)
    frame_scroll.pack(padx=10, pady=5)

    if os.path.isfile(list_path):
        with open(list_path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]

        if lines:
            for line in lines:
                item_label = ctk.CTkLabel(frame_scroll, text=line, font=("Helvetica", 13))
                item_label.pack(anchor="w", padx=5, pady=2)
        else:
            ctk.CTkLabel(frame_scroll, text="(Lista vazia)", font=("Helvetica", 13)).pack(anchor="w", padx=5, pady=2)
    else:
        ctk.CTkLabel(frame_scroll, text="Ficheiro inexistente ou erro a aceder.", font=("Helvetica", 13)).pack(anchor="w", padx=5, pady=2)


# ----------------- Execução do Código ----------------- #
dados_geral = carregar_dados()
splashscreen()
app.mainloop()
