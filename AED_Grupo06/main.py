import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import webbrowser
import tkinter as tk
import datetime
import users

root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class HootApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.app_width = 1200
        self.app_height = 675
        self.title("Hoot - Gestor de Filmes e Séries")
        self.iconbitmap("./images/hoot.ico")
        self.geometry(f"{self.app_width}x{self.app_height}")
        self.resizable(False, False)
        ecran_largura = self.winfo_screenwidth()
        ecran_altura = self.winfo_screenheight()
        x = int((ecran_largura / 2) - (self.app_width / 2))
        y = int((ecran_altura / 2) - (self.app_height / 2))
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

        self.selected_button = None
        self.username = None
        self.is_admin = False
        self.frames = {}

        self.dados_geral = self._carregar_dados()
        self.dados_series = []
        self.dados_filmes = []

        self.splashscreen()

    def splashscreen(self):
        self._clear_window()
        logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
        label_logo = ctk.CTkLabel(self, text="", image=logo)
        label_logo.place(relx=0.5, rely=0.4, anchor="center")
        progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
        progress_bar.start()
        self.after(2000, self.ecra_login)

    def ecra_login(self):
        self._clear_window()
        ctk.set_appearance_mode("light")
        promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
        label_promo = ctk.CTkLabel(self, text="", image=promo)
        label_promo.place(relx=0.0, rely=0.5, anchor="w")
        rotulo = ctk.CTkLabel(self, text="Iniciar Sessão",
                              font=("Helvetica", 24, "bold"),
                              text_color="#4F8377")
        rotulo.place(x=513, y=36)
        rotulo_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_email.place(x=513, y=92)
        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira o seu e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.place(x=513, y=115)
        rotulo_senha = ctk.CTkLabel(self, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_senha.place(x=513, y=169)
        entry_password = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira a sua palavra-passe",
                                      show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_password.place(x=513, y=191)
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
        clickable_text = ctk.CTkLabel(self,
                                      text="Esqueceste-te da tua palavra passe?",
                                      text_color="#4F8377",
                                      font=("Helvetica", 16, "underline"))
        clickable_text.place(x=513, y=246)
        clickable_text.bind("<Button-1>", lambda e: self.ecra_recuperar_password())
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
        rotulo_criar = ctk.CTkLabel(self, text="Ainda não tens conta?",
                                    font=("Helvetica", 24, "bold"),
                                    text_color="#4F8377")
        rotulo_criar.place(x=513, y=494)
        rotulo_desc = ctk.CTkLabel(self,
                                   text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores vantagens na Hoot.",
                                   font=("Helvetica", 16, "bold"),
                                   text_color="#000",
                                   justify="left",
                                   anchor="w",
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

    def ecra_recuperar_password(self):
        self._clear_window()
        ctk.set_appearance_mode("light")
        promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
        label_promo = ctk.CTkLabel(self, text="", image=promo)
        label_promo.place(relx=0.0, rely=0.5, anchor="w")
        rotulo = ctk.CTkLabel(self, text="Recuperar Palavra-Passe",
                              font=("Helvetica", 24, "bold"),
                              text_color="#4F8377")
        rotulo.place(x=513, y=36)
        rotulo_user = ctk.CTkLabel(self, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_user.place(x=513, y=112)
        entry_username = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira um username",
                                      fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_username.place(x=513, y=134)
        rotulo_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_email.place(x=513, y=208)
        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira um e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.place(x=513, y=231)
        button_criar_conta = ctk.CTkButton(self,
                                           text='ENVIAR INSTRUÇÕES',
                                           font=("Helvetica", 14.3, "bold"),
                                           text_color="#fff",
                                           hover_color="#3F685F",
                                           fg_color="#4F8377",
                                           width=173,
                                           height=36,
                                           command=lambda: self._simular_envio_instrucoes(entry_email.get()))
        button_criar_conta.place(x=513, y=314)
        button_cancelar = ctk.CTkButton(self,
                                        text='CANCELAR',
                                        font=("Helvetica", 14.3, "bold"),
                                        text_color="#fff",
                                        hover_color="#3F685F",
                                        fg_color="#4F8377",
                                        command=self.ecra_login,
                                        width=173,
                                        height=36)
        button_cancelar.place(x=713, y=314)

    def _simular_envio_instrucoes(self, email):
        print(f"A enviar e-mail de recuperação para {email}...")
        self.ecra_login()

    def criar_conta(self):
        self._clear_window()
        ctk.set_appearance_mode("light")
        promo = ctk.CTkImage(Image.open('./images/promo.png'), size=(468, 675))
        label_promo = ctk.CTkLabel(self, text="", image=promo)
        label_promo.place(relx=0.0, rely=0.5, anchor="w")
        rotulo = ctk.CTkLabel(self, text="Criar Conta", font=("Helvetica", 24, "bold"), text_color="#4F8377")
        rotulo.place(x=513, y=36)
        rotulo_user = ctk.CTkLabel(self, text="USERNAME", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_user.place(x=513, y=112)
        entry_username = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira um username",
                                      fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_username.place(x=513, y=134)
        rotulo_email = ctk.CTkLabel(self, text="E-MAIL", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_email.place(x=513, y=208)
        entry_email = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                   placeholder_text="Insira um e-mail",
                                   fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_email.place(x=513, y=231)
        rotulo_senha = ctk.CTkLabel(self, text="PALAVRA-PASSE", font=("Helvetica", 10, "bold"), text_color="#000")
        rotulo_senha.place(x=513, y=305)
        entry_password = ctk.CTkEntry(self, width=451, height=43, border_width=0,
                                      placeholder_text="Insira uma palavra-passe",
                                      show="*", fg_color="#D9D9D9", font=("Helvetica", 16))
        entry_password.place(x=513, y=328)
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

    def _carregar_dados(self):
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
                if len(partes) < 7:
                    continue
                titulo, genero, ano, rating, img_path, trailer, descricao = partes
                try:
                    ano = int(ano)
                except:
                    ano = 0
                try:
                    rating = float(rating)
                except:
                    rating = 0.0
                item = {
                    "titulo": titulo,
                    "genero": genero,
                    "ano": ano,
                    "rating": rating,
                    "img_path": img_path,
                    "trailer": trailer,
                    "descricao": descricao
                }
                lista.append(item)
        return lista

    def _carregar_dados_series(self):
        return self.dados_geral

    def _login_success(self, username):
        self.username = username
        self.is_admin = users.is_admin(username) if hasattr(users, 'is_admin') else False
        self.iniciar_frames()

    def _login_fail(self):
        print("Falha de login.")
        self.ecra_login()

    def iniciar_frames(self):
        self._clear_window()
        ctk.set_appearance_mode("dark")
        frame_series = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_filmes = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_explorar = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
        frame_perfil = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")

        frame_series.place(relx=1.0, rely=1.0, anchor="se")
        frame_filmes.place(relx=1.0, rely=1.0, anchor="se")
        frame_explorar.place(relx=1.0, rely=1.0, anchor="se")
        frame_perfil.place(relx=1.0, rely=1.0, anchor="se")

        self.frames["series"] = frame_series
        self.frames["filmes"] = frame_filmes
        self.frames["explorar"] = frame_explorar
        self.frames["perfil"] = frame_perfil

        if self.is_admin:
            frame_admin = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
            frame_admin.place(x=150, y=100)
            self.frames["admin"] = frame_admin

        top_cover_frame = ctk.CTkFrame(self, width=1050, height=100, fg_color="#242424")
        top_cover_frame.place(x=150, y=0)

        self._criar_menu_lateral()
        self._atualizar_informacoes_topo()
        self._ecra_series(frame_series)
        self._ecra_filmes(frame_filmes)
        self._ecra_explorar(frame_explorar)

        if self.is_admin:
            self._ecra_admin(self.frames["admin"])
        else:
            self._ecra_perfil(frame_perfil)

        frame_series.tkraise()

    def _criar_menu_lateral(self):
        logo_p = ctk.CTkImage(Image.open('./images/logo_ui.png'), size=(83, 48))
        label_logo_p = ctk.CTkLabel(self, text="", image=logo_p)
        label_logo_p.place(x=29, y=26)
        linha = ctk.CTkImage(Image.open('./images/Line_ecra.png'), size=(1, 472))
        label_linha = ctk.CTkLabel(self, text="", image=linha)
        label_linha.place(x=130, y=151)

        botao_series_image = ctk.CTkImage(Image.open("./images/button_series.png"), size=(68, 89))
        botao_series = ctk.CTkButton(
            self,
            width=68, height=89,
            text="",
            image=botao_series_image,
            fg_color="transparent",
            hover_color="#181818",
            command=lambda: self._update_active_screen("series")
        )
        botao_series.place(x=28, y=151)

        botao_filmes_image = ctk.CTkImage(Image.open("./images/button_filmes.png"), size=(68, 89))
        botao_filmes = ctk.CTkButton(
            self,
            width=68, height=89,
            text="",
            image=botao_filmes_image,
            fg_color="transparent",
            hover_color="#181818",
            command=lambda: self._update_active_screen("filmes")
        )
        botao_filmes.place(x=28, y=278)

        botao_explorar_image = ctk.CTkImage(Image.open("./images/button_explorar.png"), size=(68, 89))
        botao_explorar = ctk.CTkButton(
            self,
            width=68, height=89,
            text="",
            image=botao_explorar_image,
            fg_color="transparent",
            hover_color="#181818",
            command=lambda: self._update_active_screen("explorar")
        )
        botao_explorar.place(x=28, y=408)

        botao_perfil_image = ctk.CTkImage(Image.open("./images/button_perfil.png"), size=(68, 89))
        botao_perfil = ctk.CTkButton(
            self,
            width=68, height=89,
            text="",
            image=botao_perfil_image,
            fg_color="transparent",
            hover_color="#181818",
            command=lambda: self._update_active_screen("admin" if self.is_admin else "perfil")
        )
        botao_perfil.place(x=28, y=534)

    def _atualizar_informacoes_topo(self):
        user_folder = os.path.join(root_dir, "files", "users", self.username)
        if not os.path.exists(user_folder):
            image_path = './images/default_avatar.png'
        else:
            image_path = os.path.join(user_folder, "profile_picture.png")
        image = Image.open(image_path)
        avatar = ctk.CTkImage(image, size=(55, 55))
        self.avatar_label = ctk.CTkLabel(self, text="", image=avatar)
        self.avatar_label.place(x=1100, y=23)
        self.label_username_top = ctk.CTkLabel(
            self,
            text=self.username,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#a3d9c8"
        )
        self.label_username_top.place(x=1000, y=38)

    def _ecra_series(self, parent_frame):
        # Labels "Para ver" e "Brevemente" com fonte maior
        label_series_ver = ctk.CTkLabel(
            parent_frame,
            text='Para ver',
            font=("Helvetica", 18, "bold"),  # Maior fonte
            fg_color='transparent'
        )
        label_series_ver.place(x=10, y=0)

        label_series_brev = ctk.CTkLabel(
            parent_frame,
            text='Brevemente',
            font=("Helvetica", 18, "bold"),  # Maior fonte
            fg_color='transparent'
        )
        label_series_brev.place(x=520, y=0)

        self.scroll_left_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_left_series.place(x=10, y=30)

        self.scroll_right_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_right_series.place(x=520, y=30)

        if not hasattr(self, "todas_series"):
            self.todas_series = self._carregar_dados_series()

        # Pequeno frame só para alinhar horizontalmente os filtros
        filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        # Coloca-o no canto superior direito, com pequena margem
        filtro_frame.place(relx=1.0, y=10, x=-10, anchor="ne")

        generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance"]
        self.filtro_genero = ctk.CTkOptionMenu(
            filtro_frame, values=generos_possiveis, width=80
        )
        self.filtro_genero.set("Todos")
        self.filtro_genero.grid(row=0, column=0, padx=5)

        self.filtro_ano = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
        self.filtro_ano.grid(row=0, column=1, padx=5)

        self.botao_filtrar = ctk.CTkButton(
            filtro_frame,
            text="Filtrar",
            width=60,
            command=self._aplicar_filtro_series
        )
        self.botao_filtrar.grid(row=0, column=2, padx=5)

        self._mostrar_series_filtradas()

    def _aplicar_filtro_series(self):
        import datetime
        genero_selecionado = self.filtro_genero.get()
        ano_texto = self.filtro_ano.get()
        lista_filtrada = []

        for item in self.todas_series:
            if genero_selecionado != "Todos" and item["genero"] != genero_selecionado:
                continue
            if ano_texto.strip():
                try:
                    ano_int = int(ano_texto.strip())
                    if item["ano"] != ano_int:
                        continue
                except ValueError:
                    pass
            lista_filtrada.append(item)

        for child in self.scroll_left_series.winfo_children():
            child.destroy()
        for child in self.scroll_right_series.winfo_children():
            child.destroy()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in lista_filtrada:
            if item["ano"] <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)

        self._criar_cards_series(lista_passado, self.scroll_left_series)
        self._criar_cards_series(lista_futuro, self.scroll_right_series)

    def _mostrar_series_filtradas(self):
        import datetime
        for child in self.scroll_left_series.winfo_children():
            child.destroy()
        for child in self.scroll_right_series.winfo_children():
            child.destroy()

        if not hasattr(self, "todas_series"):
            self.todas_series = self._carregar_dados_series()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in self.todas_series:
            if item["ano"] <= ano_hoje:
                lista_passado.append(item)
            else:
                lista_futuro.append(item)

        self._criar_cards_series(lista_passado, self.scroll_left_series)
        self._criar_cards_series(lista_futuro, self.scroll_right_series)

    def _criar_cards_series(self, lista, parent):
        for item in lista:
            self._criar_card(
                parent_frame=parent,
                cat_img_path=item["img_path"],
                movie_name=item["titulo"],
                description=item["descricao"],
                trailer=item["trailer"],
                rating=str(item["rating"]),
                year=str(item["ano"])
            )

    def _ecra_filmes(self, parent_frame):
        mock = ctk.CTkImage(Image.open('./images/filmes_mock.png'), size=(894, 521))
        label_mock = ctk.CTkLabel(parent_frame, text="", image=mock)
        label_mock.place(x=0, y=0)

    def _ecra_explorar(self, parent_frame):
        scroll_left = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_left.place(x=10, y=0)
        scroll_right = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_right.place(x=520, y=0)

    def _ecra_perfil(self, parent_frame):
        placeholder_frame = ctk.CTkFrame(parent_frame, width=100, height=100, corner_radius=110)
        placeholder_frame.place(x=0, y=0)
        image_label = ctk.CTkLabel(placeholder_frame, text="", width=100, height=100, bg_color="#242424")
        image_label.place(relx=0.5, rely=0.5, anchor="center")
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
        user_folder = os.path.join(root_dir, "files", "users", self.username)
        if os.path.exists(user_folder):
            image_path = os.path.join(user_folder, "profile_picture.png")
        else:
            image_path = './images/default_avatar.png'
        avatar_image = ctk.CTkImage(Image.open(image_path), size=(100, 100))
        image_label.configure(image=avatar_image, text="")
        image_label.image = avatar_image
        info_user = ctk.CTkLabel(parent_frame,
                                 text="Métricas do Utilizador:\n- Gosto: 0\n- Horas: 0\n- Comentários: 0\n- Notificações: 0",
                                 font=("Helvetica", 14),
                                 text_color="white",
                                 justify="left")
        info_user.place(x=20, y=150)

    def _ecra_admin(self, parent_frame):
        label = ctk.CTkLabel(parent_frame, text="Área de Admin",
                             font=("Helvetica", 24, "bold"),
                             text_color="#4F8377")
        label.pack(pady=10)
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

    def _gerir_utilizadores(self):
        print("Gerir Utilizadores: criar ecrã/modal para listar, bloquear ou remover utilizadores.")

    def _gerir_categorias(self):
        print("Gerir Categorias: criar ecrã para adicionar/editar/remover categorias.")

    def _ecra_dashboard_admin(self):
        print("Dashboard Admin: criar gráficos e estatísticas para administradores.")

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _update_active_screen(self, frame_name):
        if frame_name in self.frames:
            if frame_name == "perfil" or frame_name == "admin":
                print("A ocultar avatar e username no topo...")
                self.avatar_label.place_forget()
                self.label_username_top.place_forget()
            else:
                self.avatar_label.place(x=1100, y=23)
                self.label_username_top.place(x=1000, y=38)
            self.frames[frame_name].tkraise()
        else:
            print(f"AVISO: O frame '{frame_name}' não foi encontrado em self.frames.")

    def _toggle_password_visibility(self, entry: ctk.CTkEntry):
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    def _upload_avatar(self, image_label: ctk.CTkLabel):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_path:
            return
        user_folder = os.path.join(root_dir, "files", "users", self.username)
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
        if hasattr(self, "avatar_label"):
            topo_img = ctk.CTkImage(circular, size=(55, 55))
            self.avatar_label.configure(image=topo_img, text="")
            self.avatar_label.image = topo_img

    def _criar_card(self, parent_frame, cat_img_path, movie_name, description, trailer, rating, year):
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
            colunas = 4
            num_cards = len(parent_frame.winfo_children()) - 1
            linha = num_cards // colunas
            coluna = num_cards % colunas
            card_frame.grid(row=linha, column=coluna, padx=5, pady=5)

            def on_click(event):
                self._mostrar_detalhes_filme(movie_name, description, trailer, rating, year)

            card_frame.bind("<Button-1>", on_click)
            card_label.bind("<Button-1>", on_click)

        except (FileNotFoundError, IOError):
            print(f"Erro ao carregar a imagem: {cat_img_path}")

    def _mostrar_detalhes_filme(self, movie_name, description, trailer, rating, year):
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

if __name__ == "__main__":
    app = HootApp()
    app.mainloop()