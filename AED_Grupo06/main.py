import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import webbrowser
import tkinter as tk

# Se precisares de HTMLLabel para ver vídeos do YouTube embutidos, import do tkhtmlview (ou equivalente):
# from tkhtmlview import HTMLLabel

# Se precisares do TkinterVideo:
# from tkVideoPlayer import TkinterVideo

# Módulo de utilizadores que criaste
import users

# =========================
# Configurações Iniciais
# =========================

root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)  # Garante que estamos no diretório do ficheiro

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# =========================
# Classe Principal da App
# =========================
class HootApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Dimensões
        self.app_width = 1200
        self.app_height = 675
        self.title("Hoot - Gestor de Filmes e Séries")
        self.iconbitmap("./images/hoot.ico")
        self.geometry(f"{self.app_width}x{self.app_height}")
        self.resizable(False, False)

        # Centra no ecrã
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (self.app_width / 2))
        y = int((screen_height / 2) - (self.app_height / 2))
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

        # Variáveis de estado
        self.selected_button = None
        self.username = None
        self.is_admin = False

        # Frames principais armazenados num dicionário
        self.frames = {}

        # Inicia no SplashScreen
        self.splashscreen()

    # =========================================
    # 1) Splash Screen
    # =========================================
    def splashscreen(self):
        """Cria a splashscreen da app."""
        # Limpa o ecrã
        self._clear_window()

        # Logo
        logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
        label_logo = ctk.CTkLabel(self, text="", image=logo)
        label_logo.place(relx=0.5, rely=0.4, anchor="center")

        # Barra de loading
        progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
        progress_bar.start()

        # Após 2s, vai para tela de login
        self.after(2000, self.ecra_login)

    # =========================================
    # 2) Tela de Login
    # =========================================
    def ecra_login(self):
        self._clear_window()
        ctk.set_appearance_mode("light")

        # Imagem Lateral
        promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
        label_promo = ctk.CTkLabel(self, text="", image=promo)
        label_promo.place(relx=0.0, rely=0.5, anchor="w")

        # Título
        rotulo = ctk.CTkLabel(self, text="Iniciar Sessão",
                              font=("Helvetica", 24, "bold"),
                              text_color="#4F8377")
        rotulo.place(x=513, y=36)

        # E-mail
        rotulo_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_email.place(x=513, y=92)

        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira o seu e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.place(x=513, y=115)

        # Palavra-passe
        rotulo_senha = ctk.CTkLabel(self, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_senha.place(x=513, y=169)

        entry_password = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira a sua palavra-passe",
                                      show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_password.place(x=513, y=191)

        # Botão de mostrar/ocultar password
        toggle_button = ctk.CTkButton(self,
                                      text="👁",
                                      font=("Helvetica", 14),
                                      width=35,
                                      height=35,
                                      fg_color="#D9D9D9",
                                      bg_color="#D9D9D9",
                                      hover_color="#B0B0B0",
                                      text_color="#000",
                                      command=lambda: self._toggle_password_visibility(entry_password))
        toggle_button.place(x=923, y=195)

        # Link de recuperação de password (AGORA VAI PARA ecra_recuperar_password)
        clickable_text = ctk.CTkLabel(self,
                                      text="Esqueceste-te da tua palavra passe?",
                                      text_color="#4F8377",
                                      font=("Helvetica", 16, "underline"))
        clickable_text.place(x=513, y=246)
        clickable_text.bind("<Button-1>", lambda e: self.ecra_recuperar_password())

        # Botão de iniciar sessão
        button_iniciar_sessao = ctk.CTkButton(self,
                                              text='INICIAR SESSÃO',
                                              font=("Helvetica", 14.3, "bold"),
                                              text_color="#000",
                                              hover_color="#D59C2A",
                                              fg_color="#F2C94C",
                                              width=173,
                                              height=36,
                                              command=lambda:
                                                 users.logIn(entry_password.get(),
                                                             entry_email.get(),
                                                             self._login_success,
                                                             self._login_fail))
        button_iniciar_sessao.place(x=513, y=297)

        # Secção de criar conta
        rotulo_criar = ctk.CTkLabel(self, text="Ainda não tens conta?",
                                    font=("Helvetica", 24, "bold"),
                                    text_color="#4F8377")
        rotulo_criar.place(x=513, y=494)
        rotulo_desc = ctk.CTkLabel(self,
                                   text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores vantagens na Hoot.",
                                   font=("Helvetica", 16, "bold"),
                                   text_color="#000",
                                   wraplength=450)
        rotulo_desc.place(x=513, y=540)

        button_criar_conta = ctk.CTkButton(self,
                                           text='CRIAR CONTA',
                                           font=("Helvetica", 14.3, "bold"),
                                           text_color="#fff",
                                           hover_color="#3F685F",
                                           fg_color="#4F8377",
                                           width=173,
                                           height=36,
                                           command=self.criar_conta)
        button_criar_conta.place(x=513, y=601)

    # =========================================
    # 2.1) Tela de Recuperação de Password
    # =========================================
    def ecra_recuperar_password(self):
        """Tela para recuperar a palavra-passe."""
        self._clear_window()
        ctk.set_appearance_mode("light")

        # Apenas um exemplo simples
        label_info = ctk.CTkLabel(self,
                                  text="Recuperar Password",
                                  font=("Helvetica", 24, "bold"),
                                  text_color="#4F8377")
        label_info.pack(pady=40)

        label_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        label_email.pack()
        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira o seu e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.pack(pady=10)

        # Botão que simulava envio de e-mail
        button_recuperar = ctk.CTkButton(self,
                                         text="Enviar Instruções",
                                         font=("Helvetica", 14, "bold"),
                                         fg_color="#F2C94C",
                                         text_color="#000",
                                         command=lambda: self._simular_envio_instrucoes(entry_email.get()))
        button_recuperar.pack(pady=20)

        button_cancelar = ctk.CTkButton(self,
                                        text="Cancelar",
                                        font=("Helvetica", 14, "bold"),
                                        fg_color="#4F8377",
                                        text_color="#fff",
                                        command=self.ecra_login)
        button_cancelar.pack(pady=10)

    def _simular_envio_instrucoes(self, email):
        # Aqui inseres a lógica real de recuperação
        print(f"A enviar e-mail de recuperação para {email}...")
        self.ecra_login()

    # =========================================
    # 3) Tela de Criar Conta
    # =========================================
    def criar_conta(self):
        self._clear_window()
        ctk.set_appearance_mode("light")

        # Imagem Lateral
        promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
        label_promo = ctk.CTkLabel(self, text="", image=promo)
        label_promo.place(relx=0.0, rely=0.5, anchor="w")

        rotulo = ctk.CTkLabel(self, text="Criar Conta", font=("Helvetica", 24, "bold"), text_color="#4F8377")
        rotulo.place(x=513, y=36)

        # Username
        rotulo_user = ctk.CTkLabel(self, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_user.place(x=513, y=112)
        entry_username = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira um username",
                                      fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_username.place(x=513, y=134)

        # E-mail
        rotulo_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_email.place(x=513, y=208)
        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira um e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.place(x=513, y=231)

        # Password
        rotulo_senha = ctk.CTkLabel(self, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_senha.place(x=513, y=305)
        entry_password = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira uma palavra-passe",
                                      show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_password.place(x=513, y=328)

        # Botão de toggle password
        toggle_button = ctk.CTkButton(self,
                                      text="👁",
                                      font=("Helvetica", 14),
                                      width=35,
                                      height=35,
                                      fg_color="#D9D9D9",
                                      bg_color="#D9D9D9",
                                      hover_color="#B0B0B0",
                                      text_color="#000",
                                      command=lambda: self._toggle_password_visibility(entry_password))
        toggle_button.place(x=923, y=332)

        # Botão CRIAR CONTA
        button_criar_conta = ctk.CTkButton(self,
                                           text='CRIAR CONTA',
                                           font=("Helvetica", 14.3, "bold"),
                                           text_color="#fff",
                                           hover_color="#3F685F",
                                           fg_color="#4F8377",
                                           width=173,
                                           height=36,
                                           command=lambda: users.sign(entry_username.get(),
                                                                     entry_password.get(),
                                                                     entry_email.get(),
                                                                     self.ecra_login))
        button_criar_conta.place(x=513, y=414)

        # Botão CANCELAR
        button_cancelar = ctk.CTkButton(self,
                                        text='CANCELAR',
                                        font=("Helvetica", 14.3, "bold"),
                                        text_color="#fff",
                                        hover_color="#3F685F",
                                        fg_color="#4F8377",
                                        command=self.ecra_login,
                                        width=173,
                                        height=36)
        button_cancelar.place(x=713, y=414)

    # =========================================
    # 4) Caso o login seja bem-sucedido
    # =========================================
    def _login_success(self, username):
        # O módulo users.logIn, em princípio, indicará se o user é admin ou não
        self.username = username
        # Exemplo: se no teu users.py existir algo do género:
        # self.is_admin = users.is_admin(username)
        self.is_admin = users.is_admin(username) if hasattr(users, 'is_admin') else False

        # Constrói as telas principais
        self.iniciar_frames()
        print(f"[DEBUG] Login com sucesso. Utilizador: {username} | Admin? {self.is_admin}")

    def _login_fail(self):
        # Lida com o caso de falha
        print("[DEBUG] Falha de login.")
        # Poderias exibir um pop-up ou Label com erro
        # Vamos apenas voltar ao ecra_login
        self.ecra_login()

    # =========================================
    # 5) Construção da Janela Principal
    # =========================================
    def iniciar_frames(self):
        """Inicializa frames principais da app pós-login."""
        self._clear_window()
        ctk.set_appearance_mode("dark")

        # Cria frames que serão sobrepostos
        frame_series = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_filmes = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_explorar = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_perfil = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")

        frame_series.place(x=150, y=100)   # Reserva espaço para menu lateral e top
        frame_filmes.place(x=150, y=100)
        frame_explorar.place(x=150, y=100)
        frame_perfil.place(x=150, y=100)

        # Armazenar para gerir a exibição
        self.frames["series"] = frame_series
        self.frames["filmes"] = frame_filmes
        self.frames["explorar"] = frame_explorar
        self.frames["perfil"] = frame_perfil

        # Frame Admin (só se for admin)
        if self.is_admin:
            frame_admin = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
            frame_admin.place(x=150, y=100)
            self.frames["admin"] = frame_admin

        # Frame para o topo (avatar e username)
        top_cover_frame = ctk.CTkFrame(self, width=1050, height=100, fg_color="#242424")
        top_cover_frame.place(x=150, y=0)

        # Menu lateral (botões) + Avatar e user
        self._criar_menu_lateral()
        self._atualizar_informacoes_topo()

        # Preenche cada frame com a sua lógica
        self._ecra_series(frame_series)
        self._ecra_filmes(frame_filmes)
        self._ecra_explorar(frame_explorar)
        if self.is_admin:
            self._ecra_admin(self.frames["admin"])
        else:
            self._ecra_perfil(frame_perfil)

        # Abre séries por default
        frame_series.tkraise()

    # 5.1) Menu Lateral
    def _criar_menu_lateral(self):
        # Logo
        logo_p = ctk.CTkImage(Image.open('./images/logo_ui.png'), size=(83, 48))
        label_logo_p = ctk.CTkLabel(self, text="", image=logo_p)
        label_logo_p.place(x=29, y=26)

        # Linha vertical
        linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
        label_linha = ctk.CTkLabel(self, text="", image=linha)
        label_linha.place(x=130, y=151)

        # Botão - SÉRIES
        botao_series_image = ctk.CTkImage(Image.open("./images/button_series.png"), size=(68, 89))
        botao_series = ctk.CTkButton(self,
                                     width=68, height=89,
                                     text="",
                                     image=botao_series_image,
                                     fg_color="transparent",
                                     hover_color="#181818",
                                     command=lambda: self._update_active_screen("series"))
        botao_series.place(x=28, y=151)

        # Botão - FILMES
        botao_filmes_image = ctk.CTkImage(Image.open("./images/button_filmes.png"), size=(68, 89))
        botao_filmes = ctk.CTkButton(self,
                                     width=68, height=89,
                                     text="",
                                     image=botao_filmes_image,
                                     fg_color="transparent",
                                     hover_color="#181818",
                                     command=lambda: self._update_active_screen("filmes"))
        botao_filmes.place(x=28, y=278)

        # Botão - EXPLORAR
        botao_explorar_image = ctk.CTkImage(Image.open("./images/button_explorar.png"), size=(68, 89))
        botao_explorar = ctk.CTkButton(self,
                                       width=68, height=89,
                                       text="",
                                       image=botao_explorar_image,
                                       fg_color="transparent",
                                       hover_color="#181818",
                                       command=lambda: self._update_active_screen("explorar"))
        botao_explorar.place(x=28, y=408)

        # Botão - PERFIL (ou ADMIN)
        botao_perfil_image = ctk.CTkImage(Image.open("./images/button_perfil.png"), size=(68, 89))
        botao_perfil = ctk.CTkButton(self,
                                     width=68, height=89,
                                     text="",
                                     image=botao_perfil_image,
                                     fg_color="transparent",
                                     hover_color="#181818",
                                     command=lambda: (
                                         self._update_active_screen("admin") if self.is_admin
                                         else self._update_active_screen("perfil")
                                     ))
        botao_perfil.place(x=28, y=534)

    # 5.2) Informação de topo (avatar e username)
    def _atualizar_informacoes_topo(self):
        # Avatar
        user_folder = os.path.join(root_dir, "files", "users", self.username)
        if not os.path.exists(user_folder):
            image_path = './images/default_avatar.png'
        else:
            image_path = os.path.join(user_folder, "profile_picture.png")

        image = Image.open(image_path)
        avatar = ctk.CTkImage(image, size=(55, 55))

        # Torna o label do avatar no topo um atributo de instância
        self.avatar_label = ctk.CTkLabel(self, text="", image=avatar)
        self.avatar_label.place(x=1100, y=23)

        # Username
        self.label_username_top = ctk.CTkLabel(
            self,
            text=self.username,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#a3d9c8"
        )
        self.label_username_top.place(x=1000, y=38)


    # =========================================
    # Frames de Conteúdo
    # =========================================

    def _ecra_series(self, parent_frame):
        """Frame das séries."""
        # Exemplo do que já tinhas
        scroll_left = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_left.place(x=10, y=0)
        scroll_right = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_right.place(x=520, y=0)

        # Poderias preencher com cards (mock):
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
        self._criar_card(scroll_left, "./images/catalog/hp1.jpg",
                         "Harry Potter e a Pedra Filosofal",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "4.8", "2025")
        self._criar_card(scroll_left, "./images/catalog/hp2.jpg",
                         "Harry Potter e a Pedra Filosofal LOL",
                         "Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...Um órfão descobre que é um bruxo e começa uma jornada mágica...",
                         "https://www.youtube.com/watch?v=2yJgwwDcgV8",
                         "5", "2035")
    

    def _ecra_filmes(self, parent_frame):
        """Frame dos filmes."""
        # Exemplo simples do que tinhas
        mock = ctk.CTkImage(Image.open('./images/filmes_mock.png'), size=(894, 521))
        label_mock = ctk.CTkLabel(parent_frame, text="", image=mock)
        label_mock.place(x=0, y=0)

    def _ecra_explorar(self, parent_frame):
        """Frame de explorar."""
        scroll_left = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_left.place(x=10, y=0)
        scroll_right = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_right.place(x=520, y=0)
        # Aqui poderias colocar busca por nome/categoria/etc.

    def _ecra_perfil(self, parent_frame):
        """Frame de perfil (user normal)."""
        placeholder_frame = ctk.CTkFrame(parent_frame, width=100, height=100, corner_radius=110)
        placeholder_frame.place(x=0, y=0)

        image_label = ctk.CTkLabel(placeholder_frame, text="", width=100, height=100, bg_color="#242424")
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Username
        label_username = ctk.CTkLabel(
            parent_frame,
            text=self.username,
            font=ctk.CTkFont(family="Helvetica", size=27, weight="bold"),
            text_color="#a3d9c8",
            anchor="e",
            justify="left",
            wraplength=300
        )
        label_username.place(x=125, y=30)

        # Botão de mudar avatar
        upload_button = ctk.CTkButton(
            placeholder_frame,
            text="Mudar",
            command=lambda: self._upload_avatar(image_label),
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="transparent",
            bg_color="transparent",
            hover_color="#242424",
            text_color="#FFFFFF",
            border_width=1,
            border_color="white",
            width=10,
            height=30
        )
        upload_button.place(relx=0.5, rely=0.5, anchor="center")

        # Carrega imagem do avatar
        user_folder = os.path.join(root_dir, "files", "users", self.username)
        if os.path.exists(user_folder):
            image_path = os.path.join(user_folder, "profile_picture.png")
        else:
            image_path = './images/default_avatar.png'
        avatar_image = ctk.CTkImage(Image.open(image_path), size=(100, 100))
        image_label.configure(image=avatar_image, text="")
        image_label.image = avatar_image

        # Aqui poderás criar as estatísticas do user, gosto, horas investidas, etc.
        # placeholders
        info_user = ctk.CTkLabel(parent_frame,
                                 text="Métricas do Utilizador:\n- Gosto: 0\n- Horas: 0\n- Comentários: 0\n- Notificações: 0",
                                 font=("Helvetica", 14),
                                 text_color="white",
                                 justify="left")
        info_user.place(x=20, y=150)

    def _ecra_admin(self, parent_frame):
        """Frame de admin. Mostra botões para gerir utilizadores, categorias, ver dashboard, etc."""
        label = ctk.CTkLabel(parent_frame, text="Área de Admin",
                             font=("Helvetica", 24, "bold"),
                             text_color="#4F8377")
        label.pack(pady=10)

        # Botões de gestão
        btn_users = ctk.CTkButton(parent_frame,
                                  text="Gerir Utilizadores",
                                  fg_color="#4F8377",
                                  command=self._gerir_utilizadores)
        btn_users.pack(pady=5)

        btn_categorias = ctk.CTkButton(parent_frame,
                                       text="Gerir Categorias",
                                       fg_color="#4F8377",
                                       command=self._gerir_categorias)
        btn_categorias.pack(pady=5)

        btn_dashboard = ctk.CTkButton(parent_frame,
                                      text="Dashboard Admin",
                                      fg_color="#4F8377",
                                      command=self._ecra_dashboard_admin)
        btn_dashboard.pack(pady=5)

        # Poderias criar mais botões (ex.: ver logs, aprovar reviews, etc.)

    def _gerir_utilizadores(self):
        """Placeholder para lógica de gerir utilizadores (admin)."""
        print("Gerir Utilizadores: Aqui criarias o ecrã ou modal para listar users, bloquear, remover...")

    def _gerir_categorias(self):
        """Placeholder para lógica de gerir categorias (admin)."""
        print("Gerir Categorias: Aqui criarias o ecrã para adicionar/editar/remover categorias...")

    def _ecra_dashboard_admin(self):
        """Placeholder para um dashboard real com gráficos. (Admin)"""
        print("Dashboard Admin: Aqui criarias e exibirias gráficos (Matplotlib, etc.)")

    # =========================================
    # Funções Internas / Auxiliares
    # =========================================

    def _clear_window(self):
        """Remove todos widgets da janela."""
        for widget in self.winfo_children():
            widget.destroy()

    def _update_active_screen(self, frame_name):
        """Altera o frame ativo."""
        if frame_name in self.frames:
            self.frames[frame_name].tkraise()

    def _toggle_password_visibility(self, entry: ctk.CTkEntry):
        """Mostra ou oculta o texto de um ctk.CTkEntry (password)."""
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    def _upload_avatar(self, image_label: ctk.CTkLabel):
        """Faz upload, recorta e salva o avatar do utilizador."""
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_path:
            return

        user_folder = os.path.join(root_dir, "files", "users", self.username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Carrega e recorta para quadrado
        with Image.open(file_path) as img:
            width, height = img.size
            side_length = min(width, height)
            left = (width - side_length) // 2
            top = (height - side_length) // 2
            right = left + side_length
            bottom = top + side_length
            cropped_image = img.crop((left, top, right, bottom))

        # Aplica máscara circular e redimensiona
        size = (500, 500)
        cropped_image = cropped_image.resize(size, Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        circular_image = Image.new("RGBA", size)
        circular_image.paste(cropped_image, (0, 0), mask)

        # Guarda
        save_path = os.path.join(user_folder, "profile_picture.png")
        circular_image.save(save_path)
        print(f"Imagem guardada em: {save_path}")

        # Atualiza o placeholder (dentro do perfil) 
        ctk_image = ctk.CTkImage(circular_image, size=(100, 100))
        image_label.configure(image=ctk_image, text="")
        image_label.image = ctk_image

        # >>> Agora atualiza o avatar no topo <<<
        if hasattr(self, "avatar_label"):
            top_image = ctk.CTkImage(circular_image, size=(55, 55))
            self.avatar_label.configure(image=top_image, text="")
            self.avatar_label.image = top_image

    def _criar_card(self, parent_frame, cat_img_path, movie_name, description, trailer, rating, year):
        """Exemplo simplificado de criação de cards."""
        try:
            card_image = Image.open(cat_img_path).resize((100, 148), Image.Resampling.LANCZOS)
            # Rounded corners
            mask = Image.new("L", card_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), card_image.size], radius=6, fill=255)
            rounded_card_image = Image.new("RGBA", card_image.size)
            rounded_card_image.paste(card_image, (0, 0), mask)

            card_frame = ctk.CTkFrame(parent_frame, width=110, height=158)
            card_frame.grid_propagate(False)

            card_image_ctk = ctk.CTkImage(rounded_card_image, size=(100, 148))
            card_label = ctk.CTkLabel(card_frame, image=card_image_ctk, text="")
            card_label.pack(expand=True)

            # Disposição em grid (4 colunas, p.ex.)
            columns = 4
            num_cards = len(parent_frame.winfo_children()) - 1
            row = num_cards // columns
            col = num_cards % columns
            card_frame.grid(row=row, column=col, padx=5, pady=5)

            # Tornar “clicável”
            def on_click(event):
                self._mostrar_detalhes_filme(movie_name, description, trailer, rating, year)

            card_frame.bind("<Button-1>", on_click)
            card_label.bind("<Button-1>", on_click)

        except (FileNotFoundError, IOError) as e:
            print(f"Erro ao carregar imagem: {e}")

    def _mostrar_detalhes_filme(self, movie_name, description, trailer, rating, year):
        """Cria uma janela/ frame sobreposto com detalhes do filme."""
        detalhes_frame = ctk.CTkFrame(self, width=800, height=500, corner_radius=6, fg_color="#4f8377")
        detalhes_frame.place(relx=0.5, rely=0.5, anchor="center")

        botao_fechar = ctk.CTkButton(detalhes_frame,
                                     text="X",
                                     width=30,
                                     command=detalhes_frame.destroy,
                                     fg_color="#a3d9c8",
                                     text_color="#121212")
        botao_fechar.place(x=760, y=10)

        titulo = ctk.CTkLabel(detalhes_frame,
                              text=movie_name,
                              font=("Helvetica", 24, "bold"),
                              text_color="#ffffff")
        titulo.place(x=20, y=20)

        desc = ctk.CTkLabel(detalhes_frame,
                            text=description,
                            font=("Helvetica", 12),
                            text_color="#ffffff",
                            wraplength=700)
        desc.place(x=20, y=60)

        info = ctk.CTkLabel(detalhes_frame,
                            text=f"Rating: {rating} | Ano: {year}",
                            font=("Helvetica", 12, "bold"),
                            text_color="#ffffff")
        info.place(x=20, y=460)

        # Se quiseres exibir um iframe YouTube, precisarias do HTMLLabel (tkhtmlview)
        # from tkhtmlview import HTMLLabel
        #
        # video_label = HTMLLabel(detalhes_frame,
        #                        html=f'<iframe width="700" height="400" src="{trailer}" frameborder="0" allowfullscreen></iframe>')
        # video_label.place(x=50, y=100)

        # Ou simplesmente abrir no browser:
        # webbrowser.open(trailer, new=2)

# =============================
# Inicialização da Aplicação
# =============================
if __name__ == "__main__":
    app = HootApp()
    app.mainloop()
    