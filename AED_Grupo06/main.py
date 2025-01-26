# ------------------------------------------------------------------------
#                       TRABALHO DE GRUPO AED
#                             Grupo 6
# ------------------------------------------------------------------------
#
# António Amorim - 40240119
# Gabriel Paiva  - 40240137
# Henrique Silva - 40240132
#
# ------------------------------------------------------------------------
#
# Gestor de Filmes e Séries Online - HOOT
#
# ------------------------------------------------------------------------


import os  # Biblioteca padrão para operações relacionadas ao sistema de arquivos e caminhos.
import tkinter as tk  # Biblioteca padrão para criar interfaces gráficas simples em Python.
import webbrowser  # Biblioteca padrão para abrir URLs no navegador web do sistema.
import datetime  # Biblioteca padrão para manipular datas e horários.
import customtkinter as ctk  # Biblioteca de terceiros para criar interfaces gráficas modernas e customizadas.
from tkinter import filedialog, ttk  # filedialog: para janelas de seleção de arquivos; ttk: para widgets mais estilizados no Tkinter.
from PIL import Image, ImageDraw  # Biblioteca Pillow para manipulação de imagens; ImageDraw para desenhar em imagens.
from tkcalendar import Calendar  # Biblioteca para usar um widget de calendário no Tkinter.
import matplotlib  # Biblioteca padrão para criar gráficos e visualizações.
import matplotlib.pyplot as plt  # Submódulo do Matplotlib para criar gráficos de forma simples.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integra gráficos Matplotlib em interfaces gráficas Tkinter.


import users            # Módulo de gestão de utilizadores
import CTkMessagebox    # Para exibir mensagens de alerta/erro/sucesso

# ------------------------------------------------------------------------
#                       VARIÁVEIS GLOBAIS
# ------------------------------------------------------------------------
app = None
app_width = 1200
app_height = 675

frames = {}
username = None          # Guardará o nome do utilizador autenticado
is_admin = False         # Se o utilizador é administrador
current_screen = None    # Para sabermos qual o ecrã/aba atual

# Estas listas irão conter o catálogo carregado do ficheiro data.txt
dados_geral = []
dados_series = []
dados_filmes = []

# Elementos de interface que serão manipulados globalmente
avatar_label = None
label_username_top = None

# Referências para frames scrolláveis
scroll_left_series = None
scroll_right_series = None
scroll_left_filmes = None
scroll_right_filmes = None

# Diretório raiz do projeto (onde este script está localizado)
root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

# Definições de aparência do CustomTkinter
ctk.set_appearance_mode("dark")              # "light" ou "dark"
ctk.set_default_color_theme("green")         # Tema de cores

# ------------------------------------------------------------------------
#            CONFIGURAÇÃO E INICIALIZAÇÃO DA JANELA PRINCIPAL
# ------------------------------------------------------------------------
app = ctk.CTk()
app.title("Hoot - Gestor de Filmes e Séries")
app.iconbitmap("./images/hoot.ico")

# Dimensões fixas + centragem da janela no ecrã
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()
pos_x = int((screen_w / 2) - (app_width / 2))
pos_y = int((screen_h / 2) - (app_height / 2))
app.geometry(f"{app_width}x{app_height}+{pos_x}+{pos_y}")
app.resizable(False, False)

# ------------------------------------------------------------------------
#                      FUNÇÕES DE SUPORTE / UTILITÁRIAS
# ------------------------------------------------------------------------

def clear_window():
    """
    Remove todos os widgets/frames da janela principal.
    Útil para mudar de ecrã de forma limpa.
    """
    for widget in app.winfo_children():
        widget.destroy()

def toggle_password_visibility(entry: ctk.CTkEntry):
    """
    Altera a visibilidade do texto no campo de password.
    Se estava oculto, mostra. Se estava visível, oculta.
    """
    if entry.cget("show") == "*":
        entry.configure(show="")
    else:
        entry.configure(show="*")

def carregar_dados():
    """
    Lê o ficheiro 'data.txt' no formato:
      Título;Data de Lançamento;Data Atual;Rating IMDB;URL Trailer;Sinopse;Duração;Género;Tipo;Caminho Imagem
    Retorna uma lista de dicionários com essas chaves:
      titulo, data_lancamento, data_atual, rating, trailer, sinopse, duracao, genero, tipo, img_path
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
                "tipo": tipo.lower(),     # "serie" ou "filme"
                "img_path": img_path
            }
            lista.append(item)

    return lista

def get_user_item_state(movie_name):
    """
    Lê o ficheiro 'metricas.txt' do utilizador e devolve o estado do item (visto/para_ver).
    Se não existir registo para esse título, retorna None.
    """
    user_metric_path = os.path.join(root_dir, "files", "users", username, "metricas", "metricas.txt")
    if not os.path.isfile(user_metric_path):
        return None

    with open(user_metric_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split(";")
            if len(partes) >= 2:
                titulo_reg = partes[0]
                estado_reg = partes[1]
                if titulo_reg == movie_name:
                    return estado_reg
    return None

def get_user_watched_items(tipo):
    """
    Retorna uma lista de caminhos de imagem dos itens (tipo='serie' OU 'filme')
    que o user marcou como 'visto'.
    """
    lista = []
    for item in dados_geral:
        if item["tipo"] == tipo:
            estado = get_user_item_state(item["titulo"])
            if estado == "visto":
                lista.append(item["img_path"])
    return lista

def refresh_perfil():
    """
    Limpa e recria o frame de 'perfil' para atualizar a secção de séries/filmes
    marcados como 'visto' ou favoritos, entre outras coisas.
    """
    if "perfil" in frames:
        for widget in frames["perfil"].winfo_children():
            widget.destroy()
        ecra_perfil(frames["perfil"])

def update_active_screen(frame_name):
    """
    Atualiza o ecrã/aba atual (levanta o frame correspondente) e
    muda a cor do botão ativo no menu lateral.
    """
    global current_screen, frames
    if frame_name in frames:
        current_screen = frame_name
        atualizar_botoes_menu()
        frames[frame_name].tkraise()
    else:
        print(f"AVISO: O frame '{frame_name}' não foi encontrado em frames.")

def upload_avatar(image_label: ctk.CTkLabel):
    """
    Solicita ao utilizador que selecione uma imagem para o avatar,
    recorta-a como círculo e guarda-a em 'profile_picture.png' na pasta do user.
    Atualiza a imagem no label correspondente.
    """
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

# ------------------------------------------------------------------------
#            ECRÃS INICIAIS: SPLASHSCREEN E LOGIN/REGISTO
# ------------------------------------------------------------------------

def splashscreen():
    """
    Ecrã inicial de splash com logo e barra de progresso.
    Após 2 segundos, avança para o ecrã de login.
    """
    clear_window()

    logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
    label_logo = ctk.CTkLabel(app, text="", image=logo)
    label_logo.place(relx=0.5, rely=0.4, anchor="center")

    progress_bar = ctk.CTkProgressBar(app, mode="indeterminate")
    progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
    progress_bar.start()

    app.after(2000, ecra_login)

def ecra_login():
    """
    Ecrã de login, com campos para e-mail e password,
    bem como botões para iniciar sessão e criar conta.
    """
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

    # Botão de toggle para a password
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
    """
    Ecrã para recuperar a palavra-passe, simulando o envio de instruções por e-mail.
    """
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
    """
    Simula o envio de instruções de recuperação de palavra-passe por e-mail.
    Em contexto real, aqui estaria a lógica de envio de e-mail.
    """
    print(f"A enviar e-mail de recuperação para {email}...")
    ecra_login()

def criar_conta():
    """
    Ecrã de criação de conta, recolhendo username, e-mail e password.
    """
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

# ------------------------------------------------------------------------
#       CALLBACKS DE LOGIN: SUCESSO E FALHA
# ------------------------------------------------------------------------

def login_success(user):
    """
    Chamado em caso de sucesso no login (users.logIn).
    Guarda o username global, verifica se é admin e inicia os frames.
    """
    global username, is_admin
    username = user
    is_admin = users.is_admin(user) if hasattr(users, 'is_admin') else False
    iniciar_frames()

def login_fail():
    """
    Chamado em caso de falha no login (users.logIn).
    Retorna ao ecrã de login.
    """
    ecra_login()

# ------------------------------------------------------------------------
#          INICIALIZAÇÃO DOS FRAMES PRINCIPAIS (SÉRIES, FILMES, ETC.)
# ------------------------------------------------------------------------

def iniciar_frames():
    """
    Limpa a janela e cria todos os frames (series, filmes, explorar, perfil e admin se for admin).
    Em seguida, chama as funções de ecrã correspondentes e mostra 'series' por omissão.
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

    # Se for admin, criar também o frame "admin"
    if is_admin:
        frame_admin = ctk.CTkFrame(app, width=1050, height=540, fg_color="#242424")
        frame_admin.place(relx=1.0, rely=1.0, anchor="se")
        frames["admin"] = frame_admin

    criar_menu_lateral()
    atualizar_informacoes_topo()

    # Carregar/Recarregar dados do catálogo
    global dados_series, dados_filmes
    dados_geral[:] = carregar_dados()  # recarrega a lista global

    # Criar as "abas"
    ecra_series(frame_series)
    ecra_filmes(frame_filmes)
    ecra_explorar(frame_explorar)

    if is_admin:
        ecra_admin(frames["admin"])
    else:
        ecra_perfil(frame_perfil)

    # Mostrar por omissão o frame de séries
    frame_series.tkraise()

def criar_menu_lateral():
    """
    Cria o menu lateral com os botões para alternar entre as abas (séries, filmes, explorar, perfil/admin).
    """
    global botao_series, botao_filmes, botao_explorar, botao_perfil

    logo_p = ctk.CTkImage(Image.open('./images/logo_ui.png'), size=(83, 48))
    label_logo_p = ctk.CTkLabel(app, text="", image=logo_p)
    label_logo_p.place(x=29, y=26)

    linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
    label_linha = ctk.CTkLabel(app, text="", image=linha)
    label_linha.place(x=130, y=151)

    # Botão SÉRIES
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

    # Botão FILMES
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

    # Botão EXPLORAR
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

    # Botão PERFIL (ou ADMIN, se is_admin=True)
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

    atualizar_botoes_menu()

def atualizar_botoes_menu():
    """
    Atualiza o estado de hover/seleção dos botões do menu, de acordo com a aba selecionada.
    """
    botoes = {
        "series": botao_series,
        "filmes": botao_filmes,
        "explorar": botao_explorar,
        "perfil": botao_perfil if not is_admin else None,
        "admin": botao_perfil if is_admin else None,
    }

    for frame_name, botao in botoes.items():
        if botao:
            if frame_name == current_screen:
                botao.configure(fg_color="#181818")  # Botão selecionado
            else:
                botao.configure(fg_color="transparent")

def atualizar_informacoes_topo():
    """
    Atualiza a zona superior com o avatar e o username do utilizador.
    """
    global avatar_label, label_username_top

    user_folder = os.path.join(root_dir, "files", "users", username)
    profile_picture_path = os.path.join(user_folder, "profile_picture.png")

    if os.path.isfile(profile_picture_path):
        image_path = profile_picture_path
    else:
        image_path = './images/default_avatar.png'

    image = Image.open(image_path)
    avatar = ctk.CTkImage(image, size=(55, 55))

    if not avatar_label:
        avatar_label = ctk.CTkLabel(app, text="", image=avatar)
        avatar_label.place(x=1100, y=23)
    else:
        avatar_label.configure(image=avatar)

    if not label_username_top:
        label_username_top = ctk.CTkLabel(
            app,
            text=username,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            anchor="e",
            text_color="#a3d9c8",
            width=200
        )
        label_username_top.place(x=1075 - 200, y=38)
    else:
        label_username_top.configure(text=username)

# ------------------------------------------------------------------------
#           ABA SÉRIES
# ------------------------------------------------------------------------

def ecra_series(parent_frame):
    """
    Apresenta duas colunas de séries: 'Para Ver' (já lançadas) e 'Brevemente' (ano > atual).
    Filtra apenas séries do utilizador com estado='para_ver'.
    Permite aplicar filtros (género, ano).
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

    # Carregar apenas séries com estado 'para_ver'
    all_series = [x for x in dados_geral if x["tipo"] == "serie"]
    dados_series = []
    for s in all_series:
        estado = get_user_item_state(s["titulo"])
        if estado == "para_ver":
            dados_series.append(s)

    # Frame para filtros (género, ano)
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
        command=lambda: aplicar_filtro_series(filtro_genero_series.get(), filtro_ano_series.get())
    )
    botao_filtrar_series.grid(row=0, column=2, padx=5)

    mostrar_series_filtradas()

def aplicar_filtro_series(genero_selecionado, ano_texto):
    """
    Aplica filtro de género e ano às séries carregadas (estado='para_ver').
    Divide em listas: lançadas (<= ano atual) e futuras (> ano atual).
    """
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

    criar_cards(lista_passado, scroll_left_series, colunas=4)
    criar_cards(lista_futuro, scroll_right_series, colunas=4)

def mostrar_series_filtradas():
    """
    Limpa as duas colunas e distribui as séries entre:
      'Passado/Para Ver' e 'Futuro/Brevemente'.
    """
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

    criar_cards(lista_passado, scroll_left_series, colunas=4)
    criar_cards(lista_futuro, scroll_right_series, colunas=4)

# ------------------------------------------------------------------------
#           ABA FILMES
# ------------------------------------------------------------------------

def ecra_filmes(parent_frame):
    """
    Apresenta duas colunas de filmes: 'Para Ver' e 'Brevemente'.
    Filtra apenas filmes do utilizador com estado='para_ver'.
    Permite aplicar filtros (género, ano).
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

    # Carregar apenas filmes com estado 'para_ver'
    all_filmes = [x for x in dados_geral if x["tipo"] == "filme"]
    dados_filmes = []
    for f in all_filmes:
        estado = get_user_item_state(f["titulo"])
        if estado == "para_ver":
            dados_filmes.append(f)

    # Filtros
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
    """
    Aplica filtro de género e ano aos filmes carregados (estado='para_ver').
    Divide em listas: lançados (<= ano atual) e futuros (> ano atual).
    """
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

    criar_cards(lista_passado, scroll_left_filmes, colunas=4)
    criar_cards(lista_futuro, scroll_right_filmes, colunas=4)

def mostrar_filmes_filtradas():
    """
    Limpa as duas colunas e distribui os filmes entre:
      'Passado/Para Ver' e 'Futuro/Brevemente'.
    """
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

    criar_cards(lista_passado, scroll_left_filmes, colunas=4)
    criar_cards(lista_futuro, scroll_right_filmes, colunas=4)

# ------------------------------------------------------------------------
#           ABA EXPLORAR (FILMES E SÉRIES NUM SÓ LUGAR)
# ------------------------------------------------------------------------

def ecra_explorar(parent_frame):
    """
    Mostra todos os filmes e séries (dados_geral), com possibilidade de pesquisa
    por género, ano e título.
    """
    global dados_geral

    label_titulo = ctk.CTkLabel(
        parent_frame,
        text="Filmes e Séries",
        font=("Helvetica", 18, "bold"),
        fg_color="transparent"
    )
    label_titulo.place(x=10, y=0)

    scroll_frame = ctk.CTkScrollableFrame(parent_frame, width=960, height=450)
    scroll_frame.place(x=10, y=50)

    filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    filtro_frame.place(relx=1.0, y=0, x=-48, anchor="ne")

    generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance", "Ação", "Comédia", "Ficção Científica", "Terror"]
    filtro_genero = ctk.CTkOptionMenu(filtro_frame, values=generos_possiveis, width=100)
    filtro_genero.set("Todos")
    filtro_genero.grid(row=0, column=0, padx=5)

    filtro_ano = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
    filtro_ano.grid(row=0, column=1, padx=5)

    filtro_titulo = ctk.CTkEntry(filtro_frame, placeholder_text="Título", width=200)
    filtro_titulo.grid(row=0, column=2, padx=5)

    botao_filtrar = ctk.CTkButton(
        filtro_frame,
        text="Filtrar",
        width=80,
        command=lambda: aplicar_filtro_filmes_series(
            filtro_genero.get(),
            filtro_ano.get(),
            filtro_titulo.get(),
            scroll_frame
        )
    )
    botao_filtrar.grid(row=0, column=3, padx=5)

    # Mostrar todos ao iniciar
    mostrar_filmes_series(scroll_frame)

def aplicar_filtro_filmes_series(genero, ano, titulo, parent_frame):
    """
    Aplica filtros de género, ano e título à lista global dados_geral.
    Em seguida, limpa o frame e mostra os resultados em formato de "cards".
    """
    global dados_geral

    lista_filtrada = []
    for item in dados_geral:
        if genero != "Todos" and item["genero"] != genero:
            continue
        if ano.strip():
            try:
                ano_int = int(ano.strip())
                ano_lancamento = int(item["data_lancamento"].split("/")[-1])
                if ano_lancamento != ano_int:
                    continue
            except ValueError:
                print(f"Ano inválido: {ano}")
                continue
        if titulo.strip() and titulo.lower() not in item["titulo"].lower():
            continue
        lista_filtrada.append(item)

    # Limpar o frame antes de adicionar
    for child in parent_frame.winfo_children():
        child.destroy()

    criar_cards(lista_filtrada, parent_frame, colunas=4)

def mostrar_filmes_series(parent_frame):
    """
    Mostra todos os filmes e séries (dados_geral) em cards.
    """
    global dados_geral

    for child in parent_frame.winfo_children():
        child.destroy()

    criar_cards(dados_geral, parent_frame, colunas=8)

# ------------------------------------------------------------------------
#           ABA PERFIL (UTILIZADOR NORMAL)
# ------------------------------------------------------------------------

def get_user_metrics_and_stats():
    """
    Lê os ficheiros de métricas para calcular:
      - comentários, gostos, partilhas do user
      - horas a ver séries, episódios vistos
      - horas a ver filmes, filmes vistos
    Retorna um dicionário com esses valores.
    """
    catalog_metricas_dir = os.path.join(root_dir, "files", "catalog", "metricas")
    num_comments = 0
    num_likes = 0
    num_shares = 0

    if not os.path.exists(catalog_metricas_dir):
        os.makedirs(catalog_metricas_dir)

    # 1) Contagem de comentários/gostos/partilhas
    for ficheiro in os.listdir(catalog_metricas_dir):
        if ficheiro.endswith(".txt"):
            full_path = os.path.join(catalog_metricas_dir, ficheiro)
            with open(full_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    partes = line.split(";")
                    if len(partes) < 5:
                        continue
                    user_ = partes[0]
                    gostou_ = partes[2]
                    partilhou_ = partes[3]
                    comentario_ = partes[4]

                    if user_ == username:
                        if comentario_.strip():
                            num_comments += 1
                        if gostou_ == "True":
                            num_likes += 1
                        if partilhou_ == "True":
                            num_shares += 1

    # 2) Contagem horas/episódios/filmes vistos
    series_minutes = 0
    filmes_minutes = 0
    filmes_count = 0

    for item in dados_geral:
        estado = get_user_item_state(item["titulo"])
        if estado == "visto":
            try:
                dur = int(item["duracao"])
            except:
                dur = 0

            if item["tipo"] == "serie":
                series_minutes += dur
            elif item["tipo"] == "filme":
                filmes_minutes += dur
                filmes_count += 1

    horas_series = series_minutes // 60
    horas_filmes = filmes_minutes // 60
    episodios_vistos = series_minutes // 40  # Exemplo: 1 episódio ~ 40min

    stats = {
        "comentarios": num_comments,
        "gostos": num_likes,
        "partilhas": num_shares,
        "horas_series": horas_series,
        "episodios_vistos": episodios_vistos,
        "horas_filmes": horas_filmes,
        "filmes_vistos": filmes_count
    }
    return stats

def ecra_perfil(parent_frame):
    """
    Ecrã de perfil para utilizadores não-admin:
      - Mostra métricas (comentários, gostos, etc.)
      - Mostra séries/filmes vistos, favoritos, e listas personalizadas.
      - Possibilidade de editar avatar.
    """
    stats_dict = get_user_metrics_and_stats()
    comentarios = stats_dict["comentarios"]
    gostos = stats_dict["gostos"]
    partilhas = stats_dict["partilhas"]
    horas_series = stats_dict["horas_series"]
    episodios_vistos = stats_dict["episodios_vistos"]
    horas_filmes = stats_dict["horas_filmes"]
    filmes_vistos = stats_dict["filmes_vistos"]

    scrollable_content_perfil = ctk.CTkScrollableFrame(
        parent_frame,
        width=1050,
        height=540,
        fg_color="#242424"
    )
    scrollable_content_perfil.place(x=-1, y=-1)

    # ----------------- Zona Topo: Avatar + Botão Upload + Nome + EDITAR ----------------- #
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

    # ----------------- Contadores (Comentários/Gostos/Partilhas) ----------------- #
    counters_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    counters_frame.pack(fill="x", padx=20)

    counters_data = [
        ("comentários", str(comentarios)),
        ("gostos", str(gostos)),
        ("partilhas", str(partilhas)),
    ]
    for label_text, label_value in counters_data:
        container = ctk.CTkFrame(counters_frame, width=177, height=89,
                                 fg_color="#242424", border_color="#84C7B9", border_width=2)
        container.pack(side="left", padx=5)
        container.pack_propagate(False)

        valor = ctk.CTkLabel(container, text=label_value, font=("Helvetica", 20, "bold"))
        valor.pack(anchor="n", pady=(15, 0))
        texto = ctk.CTkLabel(container, text=label_text, font=("Helvetica", 12))
        texto.pack()

    # ----------------- Estatísticas (horas séries, episódios, horas filmes, filmes) ----------------- #
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
        ("horas a ver séries", str(horas_series)),
        ("episódios vistos", str(episodios_vistos)),
        ("horas a ver filmes", str(horas_filmes)),
        ("filmes vistos", str(filmes_vistos)),
    ]
    for label_text, label_value in stats_data:
        container = ctk.CTkFrame(stats_frame, width=177, height=89,
                                 fg_color="#242424", border_color="#84C7B9", border_width=2)
        container.pack(side="left", padx=5)
        container.pack_propagate(False)

        valor = ctk.CTkLabel(container, text=label_value, font=("Helvetica", 20, "bold"))
        valor.pack(anchor="n", pady=(15, 0))
        texto = ctk.CTkLabel(container, text=label_text, font=("Helvetica", 12))
        texto.pack()

    # ----------------- Secção de Listas ----------------- #
    lists_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Listas",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    lists_label.pack(anchor="w", padx=20, pady=(20, 5))

    lists_container = ctk.CTkFrame(scrollable_content_perfil, fg_color="#1A1A1A", width=750, height=150, corner_radius=6)
    lists_container.pack(anchor="w", padx=20, pady=5)

    create_list_treeview(lists_container)

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
    # Ajuste manual da posição (para o lado direito das listas):
    create_list_button.place(x=793, y=lists_container.winfo_y() + 419)

    # ----------------- Séries Vistas ----------------- #
    series_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Séries",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    series_label.pack(anchor="w", padx=20, pady=(20, 5))

    series_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    series_frame.pack(anchor="w", padx=20)

    series_posters = get_user_watched_items("serie")
    for poster_path in series_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None
        lbl_poster = ctk.CTkLabel(series_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    # ----------------- Séries Favoritas ----------------- #
    fav_series_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Séries Favoritas",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    fav_series_label.pack(anchor="w", padx=20, pady=(20, 5))

    fav_series_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    fav_series_frame.pack(anchor="w", padx=20)

    fav_series_path = os.path.join(user_folder, "fav_series.txt")
    if os.path.isfile(fav_series_path):
        with open(fav_series_path, "r", encoding="utf-8") as f:
            fav_series_titles = [ln.strip() for ln in f if ln.strip()]
    else:
        fav_series_titles = []

    fav_series_images = []
    for title in fav_series_titles:
        item = next((x for x in dados_geral if x["titulo"] == title), None)
        if item and os.path.exists(item["img_path"]):
            fav_series_images.append(item["img_path"])

    for poster_path in fav_series_images:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None
        lbl_poster = ctk.CTkLabel(fav_series_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    # ----------------- Filmes Vistos ----------------- #
    movies_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Filmes",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    movies_label.pack(anchor="w", padx=20, pady=(20, 5))

    movies_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    movies_frame.pack(anchor="w", padx=20)

    movies_posters = get_user_watched_items("filme")
    for poster_path in movies_posters:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None
        lbl_poster = ctk.CTkLabel(movies_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

    # ----------------- Filmes Favoritos ----------------- #
    fav_movies_label = ctk.CTkLabel(
        scrollable_content_perfil,
        text="Filmes Favoritos",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    fav_movies_label.pack(anchor="w", padx=20, pady=(20, 5))

    fav_movies_frame = ctk.CTkFrame(scrollable_content_perfil, fg_color="#242424")
    fav_movies_frame.pack(anchor="w", padx=20)

    fav_movies_path = os.path.join(user_folder, "fav_filmes.txt")
    if os.path.isfile(fav_movies_path):
        with open(fav_movies_path, "r", encoding="utf-8") as f:
            fav_movies_titles = [ln.strip() for ln in f if ln.strip()]
    else:
        fav_movies_titles = []

    fav_movies_images = []
    for title in fav_movies_titles:
        item = next((x for x in dados_geral if x["titulo"] == title), None)
        if item and os.path.exists(item["img_path"]):
            fav_movies_images.append(item["img_path"])

    for poster_path in fav_movies_images:
        try:
            img = Image.open(poster_path).resize((100, 148), Image.Resampling.LANCZOS)
            poster_ctk = ctk.CTkImage(img, size=(100, 148))
        except:
            poster_ctk = None
        lbl_poster = ctk.CTkLabel(fav_movies_frame, text="", image=poster_ctk)
        lbl_poster.pack(side="left", padx=5)

# ------------------------------------------------------------------------
#           ABA ADMINISTRAÇÃO
# ------------------------------------------------------------------------

def ecra_admin(parent_frame):
    """
    Ecrã para administradores, com gráficos de séries/filmes mais vistos,
    botões de adicionar conteúdo e utilizador, e gestão de utilizadores.
    """
    for w in parent_frame.winfo_children():
        w.destroy()

    admin_frame = ctk.CTkScrollableFrame(parent_frame, width=1050, height=540, fg_color="#242424")
    admin_frame.place(x=-1, y=-1)

    label_titulo = ctk.CTkLabel(
        admin_frame,
        text="Consola de Administração",
        font=("Helvetica", 24, "bold"),
        text_color="#84C7B9"
    )
    label_titulo.pack(pady=10, anchor="w", padx=20)

    top_section = ctk.CTkFrame(admin_frame, fg_color="#242424")
    top_section.pack(fill="x", padx=10, pady=10)

    # Zona de gráficos
    charts_frame = ctk.CTkFrame(top_section, fg_color="#2A2A2A", width=850, height=400)
    charts_frame.pack(side="left", padx=5, pady=5)
    charts_frame.pack_propagate(False)

    # Gráfico: Séries Mais Vistas
    series_data = obter_series_mais_vistas()  # dict: {titulo: contagem}
    series_nomes = list(series_data.keys())
    series_valores = list(series_data.values())

    fig_series = plt.Figure(figsize=(3.5, 3), dpi=100)
    ax_series = fig_series.add_subplot(111)
    ax_series.barh(series_nomes, series_valores, color="#84C7B9")
    ax_series.set_title("Séries Mais Vistas", color="white")
    ax_series.tick_params(axis='x', colors='white')
    ax_series.tick_params(axis='y', colors='white')
    ax_series.spines[:].set_color("white")
    fig_series.patch.set_facecolor("#2A2A2A")
    ax_series.set_facecolor("#2A2A2A")

    canvas_series = FigureCanvasTkAgg(fig_series, master=charts_frame)
    canvas_series.draw()
    canvas_series.get_tk_widget().pack(side="left", padx=10)

    # Gráfico: Filmes Mais Vistos (Line Chart)
    filmes_data = obter_filmes_mais_vistos()
    filmes_nomes = list(filmes_data.keys())
    filmes_valores = list(filmes_data.values())

    fig_filmes = plt.Figure(figsize=(3.5, 3), dpi=100)
    ax_filmes = fig_filmes.add_subplot(111)
    ax_filmes.plot(filmes_valores, color="#84C7B9", marker="o")
    ax_filmes.set_title("Filmes Mais Vistos", color="white")
    ax_filmes.tick_params(axis='x', colors='white')
    ax_filmes.tick_params(axis='y', colors='white')
    ax_filmes.spines[:].set_color("white")
    fig_filmes.patch.set_facecolor("#2A2A2A")
    ax_filmes.set_facecolor("#2A2A2A")

    ax_filmes.set_xticks(range(len(filmes_nomes)))
    ax_filmes.set_xticklabels(filmes_nomes, rotation=45, ha="right", color="white")

    canvas_filmes = FigureCanvasTkAgg(fig_filmes, master=charts_frame)
    canvas_filmes.draw()
    canvas_filmes.get_tk_widget().pack(side="left", padx=10)

    # Zona de botões (Admin)
    buttons_frame = ctk.CTkFrame(top_section, fg_color="#242424", width=250)
    buttons_frame.pack(side="left", fill="y", padx=5, pady=5)

    btn_add_conteudo = ctk.CTkButton(
        buttons_frame,
        text="+ Adicionar Série/Filme",
        fg_color="#4F8377",
        command=ecra_inserir
    )
    btn_add_conteudo.pack(fill="x", pady=5)

    btn_add_user = ctk.CTkButton(
        buttons_frame,
        text="+ Adicionar Utilizador",
        fg_color="#4F8377",
        command=abrir_modal_adicionar_user
    )
    btn_add_user.pack(fill="x", pady=5)

    btn_notif = ctk.CTkButton(
        buttons_frame,
        text="+ Notificação Global",
        fg_color="#4F8377",
        command=lambda: print("Futura funcionalidade de notificação global...")
    )
    btn_notif.pack(fill="x", pady=5)

    # Gestão de utilizadores (Treeview)
    label_gestao = ctk.CTkLabel(
        admin_frame,
        text="Gestão de Utilizadores",
        font=("Helvetica", 18, "bold"),
        text_color="#84C7B9"
    )
    label_gestao.pack(anchor="w", padx=20, pady=(20, 5))

    tree_frame = ctk.CTkFrame(admin_frame, fg_color="#1A1A1A", width=1000, height=200)
    tree_frame.pack(padx=10, pady=5)
    tree_frame.pack_propagate(False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#1A1A1A",
                    foreground="white",
                    rowheight=24,
                    fieldbackground="#1A1A1A")
    style.map("Treeview", background=[("selected", "#4F8377")])

    columns = ("username", "email", "estado", "acoes")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("username", text="Username")
    tree.heading("email", text="Email")
    tree.heading("estado", text="Estado")

    tree.column("username", width=150)
    tree.column("email", width=200)
    tree.column("estado", width=80)

    tree.pack(fill="both", expand=True)

    # Carregar utilizadores
    all_users = users.get_all_users()  # Ajustar à implementação real
    for usr in all_users:
        username_ = usr.get("username", "")
        email_ = usr.get("email", "")
        estado_ = usr.get("estado", "ativo")
        tree.insert("", "end", values=(username_, email_, estado_))

    def on_tree_double_click(event):
        sel = tree.selection()
        if not sel:
            return
        item_id = sel[0]
        row = tree.item(item_id)
        vals = row["values"]
        username_clicado = vals[0]
        abrir_modal_acoes_user(username_clicado)

    tree.bind("<Double-1>", on_tree_double_click)

def obter_series_mais_vistas():
    """
    Retorna um dicionário {titulo_serie: contagem_vistos} para todas as séries.
    A contagem baseia-se no número de utilizadores que têm estado='visto' para cada título.
    """
    contagens = {}
    for item in dados_geral:
        if item["tipo"] == "serie":
            titulo = item["titulo"]
            count = 0
            all_users = users.get_all_users()
            for u in all_users:
                user_metric_path = os.path.join(root_dir, "files", "users", u["username"], "metricas", "metricas.txt")
                if os.path.isfile(user_metric_path):
                    with open(user_metric_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            parts = line.split(";")
                            if len(parts) >= 2:
                                if parts[0] == titulo and parts[1] == "visto":
                                    count += 1
                                    break
            contagens[titulo] = count
    return contagens

def obter_filmes_mais_vistos():
    """
    Retorna um dicionário {titulo_filme: contagem_vistos} para todos os filmes.
    A contagem baseia-se no número de utilizadores que têm estado='visto' para cada título.
    """
    contagens = {}
    for item in dados_geral:
        if item["tipo"] == "filme":
            titulo = item["titulo"]
            count = 0
            all_users = users.get_all_users()
            for u in all_users:
                user_metric_path = os.path.join(root_dir, "files", "users", u["username"], "metricas", "metricas.txt")
                if os.path.isfile(user_metric_path):
                    with open(user_metric_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            parts = line.split(";")
                            if len(parts) >= 2:
                                if parts[0] == titulo and parts[1] == "visto":
                                    count += 1
                                    break
            contagens[titulo] = count
    return contagens

def abrir_modal_acoes_user(username_clicado):
    """
    Abre um Toplevel com opções de promover a admin, bloquear 15 dias ou remover utilizador.
    """
    popup = ctk.CTkToplevel(app)
    popup.title(f"Ações: {username_clicado}")
    popup.geometry("200x200+650+350")
    popup.iconbitmap(".//images//hoot.ico")
    popup.resizable(False, False)

    ctk.CTkLabel(popup, text=f"Ações para {username_clicado}").pack(pady=10)

    def promover():
        users.set_admin(username_clicado)
        popup.destroy()
        ecra_admin(frames["admin"])

    def bloquear_15dias():
        users.block_user(username_clicado, 15)
        popup.destroy()
        ecra_admin(frames["admin"])

    def remover():
        users.remove_user(username_clicado)
        popup.destroy()
        ecra_admin(frames["admin"])

    btn_promover = ctk.CTkButton(popup, text="Promover Admin", command=promover)
    btn_promover.pack(pady=5)
    btn_bloquear = ctk.CTkButton(popup, text="Bloquear 15 dias", command=bloquear_15dias, fg_color="#D9A92E")
    btn_bloquear.pack(pady=5)
    btn_remover = ctk.CTkButton(popup, text="Remover User", command=remover, fg_color="#D9534F")
    btn_remover.pack(pady=5)

def abrir_modal_adicionar_user():
    """
    Abre um Toplevel para inserir dados de um novo utilizador (username, email, password),
    e opcionalmente marcá-lo como administrador.
    """
    modal = ctk.CTkToplevel(app)
    modal.title("Adicionar Utilizador")
    modal.geometry("400x300+600+300")
    modal.iconbitmap(".//images//hoot.ico")
    modal.resizable(False, False)

    lbl = ctk.CTkLabel(modal, text="Adicionar novo utilizador", font=("Helvetica", 18, "bold"))
    lbl.pack(pady=10)

    frame_form = ctk.CTkFrame(modal)
    frame_form.pack(pady=10, padx=10, fill="x")

    # Username
    ctk.CTkLabel(frame_form, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ent_user = ctk.CTkEntry(frame_form, width=200)
    ent_user.grid(row=0, column=1, padx=5, pady=5)

    # Email
    ctk.CTkLabel(frame_form, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ent_email = ctk.CTkEntry(frame_form, width=200)
    ent_email.grid(row=1, column=1, padx=5, pady=5)

    # Password
    ctk.CTkLabel(frame_form, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    ent_pass = ctk.CTkEntry(frame_form, width=200, show="*")
    ent_pass.grid(row=2, column=1, padx=5, pady=5)

    var_admin = tk.BooleanVar(value=False)
    chk_admin = ctk.CTkCheckBox(frame_form, text="Administrador?", variable=var_admin)
    chk_admin.grid(row=3, column=0, padx=5, pady=5)

    def guardar():
        user_ = ent_user.get().strip()
        email_ = ent_email.get().strip()
        pass_ = ent_pass.get().strip()
        is_admin_flag = var_admin.get()

        if not user_ or not email_ or not pass_:
            print("Preencha todos campos!")
            return

        users.sign(user_, pass_, email_, None)
        if is_admin_flag:
            users.set_admin(user_)

        modal.destroy()
        if "admin" in frames:
            ecra_admin(frames["admin"])

    btn_save = ctk.CTkButton(modal, text="Guardar", fg_color="#4F8377", command=guardar)
    btn_save.pack(pady=5)

    btn_cancel = ctk.CTkButton(modal, text="Cancelar", fg_color="gray", command=modal.destroy)
    btn_cancel.pack(pady=5)

# ------------------------------------------------------------------------
#        FUNÇÃO PARA INSERIR NOVO FILME/SÉRIE (ADMIN)
# ------------------------------------------------------------------------

def ecra_inserir():
    """
    Abre um Toplevel para inserir um novo conteúdo (filme ou série) no ficheiro data.txt.
    """
    global dados_geral

    modal = ctk.CTkToplevel(app)
    modal.title("Adicionar Filme/Série")

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

    scrollable_frame = ctk.CTkScrollableFrame(modal, width=modal_width, corner_radius=6, fg_color="#242424")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(
        scrollable_frame,
        text="Adicionar Filme/Série",
        font=("Helvetica", 24, "bold"),
        text_color="#ffffff"
    ).pack(pady=(0, 20))

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
        """
        Abre um date picker (tkcalendar) e atualiza o label com a data selecionada.
        """
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

    # Rating
    ctk.CTkLabel(scrollable_frame, text="Rating IMDB (0-10)", font=("Helvetica", 14, "bold"), text_color="#ffffff").pack(pady=(0, 5))
    entries["rating"] = ctk.CTkEntry(scrollable_frame, width=400)
    entries["rating"].pack(pady=(0, 20))

    # Trailer
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

    # Tipo
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

    def salvar_dados():
        """
        Guarda os dados no ficheiro data.txt e fecha o modal.
        Formato:
          Título;Data Lançamento;Data Atual;Rating;Trailer;Sinopse;Duração;Género;Tipo;Caminho Imagem
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

        data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
        novo_registo = (f"{titulo};{data_lancamento};{data_atual};{rating};"
                        f"{trailer};{sinopse};{duracao};{genero};{tipo};{img_path}\n")

        caminho_ficheiro = os.path.join(root_dir, "files", "data.txt")
        with open(caminho_ficheiro, "a", encoding="utf-8") as f:
            f.write(novo_registo)

        print("Dados guardados com sucesso.")
        modal.destroy()

    ctk.CTkButton(scrollable_frame, text="Guardar", command=salvar_dados, fg_color="#4F8377").pack(pady=(20, 10))
    ctk.CTkButton(scrollable_frame, text="Cancelar", command=modal.destroy, fg_color="#D9534F").pack(pady=(0, 20))

# ------------------------------------------------------------------------
#         FUNÇÕES PARA VISUALIZAR DETALHES (CARDS, COMENTÁRIOS)
# ------------------------------------------------------------------------

def criar_cards(lista, parent_frame, colunas=4):
    """
    Cria "cards" para cada item da lista no frame, organizando numa grelha.
    Cada card é a capa (poster) do filme/série, e ao clicar abre os detalhes.
    """
    for item in lista:
        cat_img_path = item["img_path"]
        movie_name = item["titulo"]

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
            linha = (num_cards - 1) // colunas
            coluna = (num_cards - 1) % colunas
            card_frame.grid(row=linha, column=coluna, padx=5, pady=5)

            def on_click(event, nome=movie_name):
                mostrar_detalhes_filme(nome)

            card_frame.bind("<Button-1>", on_click)
            card_label.bind("<Button-1>", on_click)

        except (FileNotFoundError, IOError):
            print(f"Erro ao carregar a imagem: {cat_img_path}")

def mostrar_detalhes_filme(movie_name):
    """
    Abre um Toplevel para mostrar os detalhes de um filme/série:
      - sinopse, género, duração, rating, data lançamento
      - marcar como visto/para ver, trailer, favoritos
      - rating interno (1-5 estrelas), gostou, partilhou
      - comentários
    """
    # 1) Obter dados do item
    info = next((d for d in dados_geral if d["titulo"] == movie_name), None)
    if not info:
        CTkMessagebox.CTkMessagebox(
            title="Erro",
            message=f"Não encontrei '{movie_name}' em dados_geral!",
            icon="warning"
        )
        return

    data_lancamento = info["data_lancamento"]
    rating_imdb = info["rating"]
    trailer_url = info["trailer"]
    sinopse = info["sinopse"]
    duracao = info["duracao"]
    genero = info["genero"]
    img_path = info["img_path"]

    # 2) Criar Toplevel
    detalhes_modal = ctk.CTkToplevel()
    detalhes_modal.title(movie_name)
    detalhes_modal.iconbitmap(".//images//hoot.ico")
    w_modal, h_modal = 800, 600
    detalhes_modal.geometry(f"{w_modal}x{h_modal}+400+80")
    detalhes_modal.resizable(False, False)
    detalhes_modal.attributes("-topmost", True)

    scroll_main = ctk.CTkScrollableFrame(detalhes_modal, width=w_modal, height=h_modal)
    scroll_main.pack(fill="both", expand=True)

    # 3) Ficheiro de métricas do item
    metricas_path = os.path.join(root_dir, "files", "catalog", "metricas", f"{movie_name}.txt")
    os.makedirs(os.path.dirname(metricas_path), exist_ok=True)

    def load_all_userdata():
        """
        Lê o ficheiro e devolve um dicionário: { user: {"rating": int, "gostou": bool, "partilhou": bool, "comentario": str} }
        """
        if not os.path.isfile(metricas_path):
            with open(metricas_path, "w", encoding="utf-8"):
                pass
            return {}
        data = {}
        with open(metricas_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(";")
                if len(parts) < 5:
                    continue
                user_ = parts[0]
                rating_ = parts[1]
                gostou_ = parts[2]
                partilhou_ = parts[3]
                coment_ = parts[4]

                try:
                    rating_int = int(rating_) if rating_ else 0
                except:
                    rating_int = 0
                data[user_] = {
                    "rating": rating_int,
                    "gostou": (gostou_ == "True"),
                    "partilhou": (partilhou_ == "True"),
                    "comentario": coment_
                }
        return data

    def save_all_userdata(d):
        """
        Grava o dicionário 'd' no ficheiro, no formato:
          user;rating;gostou;partilhou;comentario
        """
        with open(metricas_path, "w", encoding="utf-8") as f:
            for user_, vals in d.items():
                linha = (
                    f"{user_};"
                    f"{vals['rating'] if vals['rating'] else ''};"
                    f"{'True' if vals['gostou'] else ''};"
                    f"{'True' if vals['partilhou'] else ''};"
                    f"{vals['comentario']}"
                )
                f.write(linha + "\n")

    all_data = load_all_userdata()
    if username not in all_data:
        all_data[username] = {"rating": 0, "gostou": False, "partilhou": False, "comentario": ""}

    user_data = all_data[username]

    # 4) Top Frame: Imagem + Info
    top_frame = ctk.CTkFrame(scroll_main)
    top_frame.pack(fill="x", padx=10, pady=10)

    frame_img = ctk.CTkFrame(top_frame)
    frame_img.pack(side="left", padx=10)
    try:
        if os.path.exists(img_path):
            pil_img = Image.open(img_path).resize((220, 320), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(pil_img, size=(220, 320))
            lbl_img = ctk.CTkLabel(frame_img, image=ctk_img, text="")
            lbl_img.pack()
        else:
            ctk.CTkLabel(frame_img, text="(Imagem indisponível)").pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        ctk.CTkLabel(frame_img, text="(Falha ao carregar imagem)").pack(pady=20)

    frame_info = ctk.CTkFrame(top_frame)
    frame_info.pack(side="left", fill="both", expand=True, padx=10)

    lbl_sinopse = ctk.CTkLabel(frame_info, text=f"Sinopse: {sinopse}", font=("Helvetica", 12), anchor="w", justify="left", wraplength=450)
    lbl_sinopse.pack(anchor="nw", padx=10)

    lbl_genero = ctk.CTkLabel(frame_info, text=f"Género: {genero}", font=("Helvetica", 12), anchor="w", justify="left", wraplength=450)
    lbl_genero.pack(anchor="nw", padx=10)

    lbl_dur = ctk.CTkLabel(frame_info, text=f"Duração: {duracao}", font=("Helvetica", 12), anchor="w", justify="left", wraplength=450)
    lbl_dur.pack(anchor="nw", padx=10)

    lbl_rat = ctk.CTkLabel(frame_info, text=f"Pontuação IMDB: {rating_imdb}", font=("Helvetica", 12), anchor="w", justify="left", wraplength=450)
    lbl_rat.pack(anchor="nw", padx=10)

    lbl_dl = ctk.CTkLabel(frame_info, text=f"Data de Lançamento: {data_lancamento}", font=("Helvetica", 12), anchor="w", justify="left", wraplength=450)
    lbl_dl.pack(anchor="nw", padx=10)

    # 5) Botões: Visto / Para Ver / Trailer / Favorito
    actions_frame = ctk.CTkFrame(scroll_main)
    actions_frame.pack(fill="x", padx=10, pady=5)

    def marcar_estado(novo_estado):
        user_metric_path = os.path.join(root_dir, "files", "users", username, "metricas", "metricas.txt")
        os.makedirs(os.path.dirname(user_metric_path), exist_ok=True)
        linhas = []
        if os.path.exists(user_metric_path):
            with open(user_metric_path, "r", encoding="utf-8") as f:
                linhas = f.readlines()

        filtradas = []
        for ln in linhas:
            ln_strip = ln.strip()
            if not ln_strip:
                continue
            partes = ln_strip.split(";")
            if len(partes) >= 2 and partes[0] == movie_name:
                continue
            filtradas.append(ln_strip)

        filtradas.append(f"{movie_name};{novo_estado}")
        with open(user_metric_path, "w", encoding="utf-8") as f:
            for l in filtradas:
                f.write(l + "\n")

        CTkMessagebox.CTkMessagebox(
            title="Estado atualizado",
            message=f"'{movie_name}' -> {novo_estado}",
            icon="check"
        )
        refresh_perfil()

    btn_visto = ctk.CTkButton(actions_frame, text="Marcar como Visto", command=lambda: marcar_estado("visto"))
    btn_visto.pack(side="left", padx=5)

    btn_paraver = ctk.CTkButton(actions_frame, text="Marcar para Ver", command=lambda: marcar_estado("para_ver"))
    btn_paraver.pack(side="left", padx=5)

    def abrir_trailer():
        if trailer_url and trailer_url.startswith("http"):
            webbrowser.open(trailer_url)
        else:
            CTkMessagebox.CTkMessagebox(
                title="Trailer indisponível",
                message="URL inválido ou não disponível.",
                icon="warning"
            )

    btn_trailer = ctk.CTkButton(actions_frame, text="Trailer", fg_color="#F2C94C", text_color="black", command=abrir_trailer)
    btn_trailer.pack(side="left", padx=5)

    def marcar_favorito():
        user_folder = os.path.join(root_dir, "files", "users", username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        if info["tipo"] == "serie":
            fav_file_path = os.path.join(user_folder, "fav_series.txt")
        else:
            fav_file_path = os.path.join(user_folder, "fav_filmes.txt")

        favoritos_existentes = []
        if os.path.isfile(fav_file_path):
            with open(fav_file_path, "r", encoding="utf-8") as f:
                favoritos_existentes = [ln.strip() for ln in f if ln.strip()]

        if movie_name not in favoritos_existentes:
            with open(fav_file_path, "a", encoding="utf-8") as f:
                f.write(movie_name + "\n")

            CTkMessagebox.CTkMessagebox(
                title="Favorito",
                message=f"'{movie_name}' foi adicionado aos favoritos!",
                icon="check"
            )
        else:
            CTkMessagebox.CTkMessagebox(
                title="Favorito",
                message=f"'{movie_name}' já está nos favoritos!",
                icon="info"
            )
        refresh_perfil()

    btn_favorito = ctk.CTkButton(
        actions_frame,
        text="Marcar como Favorito",
        fg_color="#F2C94C",
        text_color="black",
        command=marcar_favorito
    )
    btn_favorito.pack(side="left", padx=5)

    # Adicionar a lista pessoal
    lists_folder = os.path.join(root_dir, "files", "users", username, "listas")
    if not os.path.exists(lists_folder):
        os.makedirs(lists_folder)
    listas = [
        f[:-4] for f in os.listdir(lists_folder)
        if f.endswith(".txt")
    ]
    if not listas:
        listas = ["(Nenhuma lista)"]

    lista_var = tk.StringVar(value=listas[0])
    dropdown_listas = ctk.CTkOptionMenu(actions_frame, values=listas, variable=lista_var, width=150)
    dropdown_listas.pack(fill="x", padx=10, pady=5)

    def adicionar_a_lista():
        lista_escolhida = lista_var.get()
        if lista_escolhida == "(Nenhuma lista)":
            CTkMessagebox.CTkMessagebox(
                title="Listas",
                message="Não existe nenhuma lista criada. Crie primeiro na área pessoal.",
                icon="warning"
            )
            return

        list_path = os.path.join(lists_folder, lista_escolhida + ".txt")
        if not os.path.isfile(list_path):
            CTkMessagebox.CTkMessagebox(
                title="Listas",
                message="A lista escolhida já não existe!",
                icon="warning"
            )
            return

        with open(list_path, "r", encoding="utf-8") as f:
            conteudo = [ln.strip() for ln in f if ln.strip()]

        if movie_name not in conteudo:
            with open(list_path, "a", encoding="utf-8") as f:
                f.write(movie_name + "\n")

            CTkMessagebox.CTkMessagebox(
                title="Listas",
                message=f"'{movie_name}' adicionado à lista '{lista_escolhida}'.",
                icon="check"
            )
        else:
            CTkMessagebox.CTkMessagebox(
                title="Listas",
                message=f"'{movie_name}' já está na lista '{lista_escolhida}'.",
                icon="info"
            )

    btn_add_lista = ctk.CTkButton(
        actions_frame,
        text="Adicionar à Lista",
        fg_color="#4F8377",
        command=adicionar_a_lista
    )
    btn_add_lista.pack(side="left", padx=5)

    # 7) Avaliação interna (1-5), Gostar, Partilhar
    rating_frame = ctk.CTkFrame(scroll_main)
    rating_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(rating_frame, text="Avaliação (1-5): ", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

    estrelas_btns = []
    def set_rating(n):
        for i in range(5):
            if i < n:
                estrelas_btns[i].configure(fg_color="yellow")
            else:
                estrelas_btns[i].configure(fg_color="gray")

        user_data["rating"] = n
        all_data[username] = user_data
        save_all_userdata(all_data)

    current_rating = user_data["rating"]
    for i in range(5):
        b = ctk.CTkButton(rating_frame, text="★", width=40, height=40, fg_color="gray",
                          command=lambda x=i: set_rating(x + 1))
        b.pack(side="left", padx=2)
        estrelas_btns.append(b)
    set_rating(current_rating)

    gostou_var = tk.BooleanVar(value=user_data["gostou"])
    partilhou_var = tk.BooleanVar(value=user_data["partilhou"])

    def toggle_gostou():
        new_val = not gostou_var.get()
        gostou_var.set(new_val)
        btn_gostar.configure(fg_color=("green" if new_val else "gray"))
        user_data["gostou"] = new_val
        all_data[username] = user_data
        save_all_userdata(all_data)

    def toggle_partilhou():
        new_val = not partilhou_var.get()
        partilhou_var.set(new_val)
        btn_partilhar.configure(fg_color=("green" if new_val else "gray"))
        user_data["partilhou"] = new_val
        all_data[username] = user_data
        save_all_userdata(all_data)

    btn_gostar = ctk.CTkButton(
        rating_frame,
        text="Gostar",
        width=40, height=40,
        fg_color=("green" if gostou_var.get() else "gray"),
        command=toggle_gostou
    )
    btn_gostar.pack(side="left", padx=5)

    btn_partilhar = ctk.CTkButton(
        rating_frame,
        text="Partilhar",
        width=40, height=40,
        fg_color=("green" if partilhou_var.get() else "gray"),
        command=toggle_partilhou
    )
    btn_partilhar.pack(side="left", padx=5)

    # 8) Comentários
    comments_frame = ctk.CTkFrame(scroll_main)
    comments_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(comments_frame, text="Comentário:", font=("Helvetica", 12, "bold")).pack(anchor="nw", pady=(10, 5))

    comment_line = ctk.CTkFrame(comments_frame)
    comment_line.pack(anchor="nw", pady=(0, 10))

    comment_entry = ctk.CTkEntry(comment_line, width=600)
    comment_entry.pack(side="left", padx=(0, 5))

    if user_data["comentario"]:
        comment_entry.insert(0, user_data["comentario"])

    def submeter_comentario():
        texto = comment_entry.get().strip()
        user_data["comentario"] = texto
        all_data[username] = user_data
        save_all_userdata(all_data)
        CTkMessagebox.CTkMessagebox(
            title="Comentário",
            message="O seu comentário foi registado/atualizado.",
            icon="check"
        )
        exibir_comentarios()

    btn_submeter = ctk.CTkButton(comment_line, text="Submeter", command=submeter_comentario)
    btn_submeter.pack(side="left")

    list_frame = ctk.CTkScrollableFrame(comments_frame, width=760, height=250)
    list_frame.pack(fill="both", expand=True)

    def get_user_avatar(u):
        """
        Retorna um ctk.CTkImage (40x40) do avatar do user ou default se não existir.
        """
        avatar_path = os.path.join(root_dir, "files", "users", u, "profile_picture.png")
        if not os.path.isfile(avatar_path):
            avatar_path = "./images/default_avatar.png"

        try:
            pil_ava = Image.open(avatar_path).resize((40, 40), Image.Resampling.LANCZOS)
            return ctk.CTkImage(pil_ava, size=(40, 40))
        except:
            return None

    def exibir_comentarios():
        for widget in list_frame.winfo_children():
            widget.destroy()

        d = load_all_userdata()
        if not d:
            ctk.CTkLabel(list_frame, text="Ainda sem comentários. Seja o primeiro!").pack(padx=5, pady=5)
            return

        for user_, vals in d.items():
            coment_ = vals["comentario"]
            if not coment_.strip():
                continue

            comment_container = ctk.CTkFrame(list_frame)
            comment_container.pack(fill="x", anchor="w", pady=5, padx=5)

            ava_img = get_user_avatar(user_)
            if ava_img:
                lbl_ava = ctk.CTkLabel(comment_container, image=ava_img, text="")
            else:
                lbl_ava = ctk.CTkLabel(comment_container, text="(no avatar)")
            lbl_ava.pack(side="left", padx=5)

            text_label = ctk.CTkLabel(
                comment_container,
                text=f"{user_} - {coment_}",
                wraplength=500,
                justify="left"
            )
            text_label.pack(side="left", padx=5)

    exibir_comentarios()

# ------------------------------------------------------------------------
#         CRIAR OU VER LISTAS PESSOAIS
# ------------------------------------------------------------------------

def create_list_treeview(lists_container):
    """
    Cria uma Treeview dentro do frame 'lists_container' para exibir
    os ficheiros (listas) que o utilizador possui em ./files/users/<user>/listas/.
    """
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

    user_folder = os.path.join(root_dir, "files", "users", username)
    lists_folder = os.path.join(user_folder, "listas")

    if not os.path.exists(lists_folder):
        os.makedirs(lists_folder)

    for ficheiro in os.listdir(lists_folder):
        if ficheiro.endswith(".txt"):
            lista_nome = ficheiro[:-4]
            tree.insert("", "end", values=(lista_nome,))

    def on_double_click(event):
        selected = tree.selection()
        if not selected:
            return
        item = selected[0]
        lista_nome = tree.item(item, "values")[0]
        ver_conteudo_lista(lista_nome)

    tree.bind("<Double-1>", on_double_click)

def criar_lista_modal():
    """
    Abre um Toplevel para criar uma nova lista do utilizador,
    guardando-a como um ficheiro .txt em ./files/users/<username>/listas/.
    """
    modal = ctk.CTkToplevel(app)
    modal.title("Criar Nova Lista")
    modal.iconbitmap(".//images//hoot.ico")

    width_modal = 400
    height_modal = 200
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

        with open(list_path, "w", encoding="utf-8"):
            pass

        CTkMessagebox.CTkMessagebox(
            title="Sucesso",
            message=f"Lista '{list_name}' criada com sucesso!",
            icon="check"
        )
        modal.destroy()

        # Atualiza a vista de perfil
        for widget in frames["perfil"].winfo_children():
            widget.destroy()
        ecra_perfil(frames["perfil"])

    btn_criar = ctk.CTkButton(modal, text="Criar", command=criar, fg_color="#4F8377")
    btn_criar.pack(pady=(0, 5))

    btn_cancel = ctk.CTkButton(modal, text="Cancelar", command=modal.destroy, fg_color="#D9534F")
    btn_cancel.pack(pady=(0, 10))

def ver_conteudo_lista(list_name):
    """
    Abre um Toplevel com o conteúdo (itens) guardado no ficheiro da lista.
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

    label_titulo = ctk.CTkLabel(
        modal_lista,
        text=f"Itens da lista '{list_name}'",
        font=("Helvetica", 16, "bold")
    )
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

# ------------------------------------------------------------------------
#                           EXECUÇÃO INICIAL
# ------------------------------------------------------------------------
if __name__ == "__main__":
    # Carrega dados (caso o splashscreen não o faça logo)
    dados_geral = carregar_dados()
    splashscreen()
    app.mainloop()