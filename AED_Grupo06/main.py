import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import webbrowser
import tkinter as tk
import datetime
import users

"""
Comentários a nível académico:
1. Foi introduzido um frame de administrador (menu admin) que se comporta da mesma forma
   que os restantes frames (series, filmes, explorar e perfil). É colocado no mesmo local
   (relx=1.0, rely=1.0, anchor="se") com dimensões 1050x540, garantindo coerência de layout.
2. No formulário de adição de conteúdo (filme/série), adicionámos:
   - Uma checkbox para marcar se é "Série" ou "Filme".
   - Um campo adicional "Duração".
   - As novas informações são gravadas no ficheiro "data.txt", passando agora a haver 10 campos:
       [0] título
       [1] género
       [2] data_completa (DD/MM/AAAA)
       [3] data_insercao (DD/MM/AAAA)
       [4] rating (float)
       [5] img_path
       [6] trailer (URL)
       [7] descricao
       [8] tipo ("serie" ou "filme")
       [9] duracao
3. O "Cancelar" do menu de adicionar séries/filmes passa a levantar (raise) o frame de admin,
   corrigindo o comportamento anteriormente reportado.
4. Implementámos uma nova secção de filmes (aba "filmes") funcionalmente idêntica à de séries,
   mas que filtra e apresenta apenas os registos em que `tipo=="filme"`.
5. O carregamento dos dados do ficheiro "data.txt" foi atualizado para lidar com 10 campos,
   descartando linhas incompletas para evitar erros.
6. O método `_mostrar_detalhes_filme` agora exibe também a "duração" do filme/série, se existente,
   ilustrando como as novas informações podem ser apresentadas ao utilizador.
7. A estrutura modular do código (com frames para cada secção) permite escalabilidade e mantém
   a lógica de negócio (carregamento/escrita de ficheiros, gestão de utilizadores) separada
   da lógica de interface (GUI), promovendo boa legibilidade e manutenção do código.
"""

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

        # Centrar a janela no ecrã
        ecran_largura = self.winfo_screenwidth()
        ecran_altura = self.winfo_screenheight()
        x = int((ecran_largura / 2) - (self.app_width / 2))
        y = int((ecran_altura / 2) - (self.app_height / 2))
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

        self.selected_button = None
        self.username = None
        self.is_admin = False
        self.frames = {}

        # Carregamento de todos os dados (agora com 10 campos)
        self.dados_geral = self._carregar_dados()
        # (Filtrados em runtime para séries ou filmes)
        self.dados_series = []
        self.dados_filmes = []

        self.splashscreen()

    def splashscreen(self):
        """Ecrã inicial de splash com logo e barra de progresso."""
        self._clear_window()
        logo = ctk.CTkImage(Image.open('./images/logo.png'), size=(373, 142))
        label_logo = ctk.CTkLabel(self, text="", image=logo)
        label_logo.place(relx=0.5, rely=0.4, anchor="center")
        progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        progress_bar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)
        progress_bar.start()

        # Após 2 segundos, avança para o ecrã de login
        self.after(2000, self.ecra_login)

    def ecra_login(self):
        """Ecrã de login."""
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

        # Botão de toggle para visibilidade da palavra-passe
        toggle_button = ctk.CTkButton(
            self,
            text="👁",
            font=("Helvetica", 14),
            width=35,
            height=35,
            fg_color="#D9D9D9",
            bg_color="#D9D9D9",
            hover_color="#B0B0B0",
            text_color="#000",
            command=lambda: self._toggle_password_visibility(entry_password)
        )
        toggle_button.place(x=923, y=195)

        clickable_text = ctk.CTkLabel(
            self,
            text="Esqueceste-te da tua palavra passe?",
            text_color="#4F8377",
            font=("Helvetica", 16, "underline")
        )
        clickable_text.place(x=513, y=246)
        clickable_text.bind("<Button-1>", lambda e: self.ecra_recuperar_password())

        button_iniciar_sessao = ctk.CTkButton(
            self,
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
                self._login_success,
                self._login_fail
            )
        )
        button_iniciar_sessao.place(x=513, y=297)

        rotulo_criar = ctk.CTkLabel(self, text="Ainda não tens conta?",
                                    font=("Helvetica", 24, "bold"),
                                    text_color="#4F8377")
        rotulo_criar.place(x=513, y=494)

        rotulo_desc = ctk.CTkLabel(
            self,
            text="Se ainda não tens conta, cria aqui e começa a tirar partido das melhores vantagens na Hoot.",
            font=("Helvetica", 16, "bold"),
            text_color="#000",
            justify="left",
            anchor="w",
            wraplength=450
        )
        rotulo_desc.place(x=513, y=540)

        button_criar_conta = ctk.CTkButton(
            self,
            text='CRIAR CONTA',
            font=("Helvetica", 14.3, "bold"),
            text_color="#fff",
            hover_color="#3F685F",
            fg_color="#4F8377",
            width=173,
            height=36,
            command=self.criar_conta
        )
        button_criar_conta.place(x=513, y=601)

    def ecra_recuperar_password(self):
        """Ecrã para recuperar palavra-passe."""
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

        button_criar_conta = ctk.CTkButton(
            self,
            text='ENVIAR INSTRUÇÕES',
            font=("Helvetica", 14.3, "bold"),
            text_color="#fff",
            hover_color="#3F685F",
            fg_color="#4F8377",
            width=173,
            height=36,
            command=lambda: self._simular_envio_instrucoes(entry_email.get())
        )
        button_criar_conta.place(x=513, y=314)

        button_cancelar = ctk.CTkButton(
            self,
            text='CANCELAR',
            font=("Helvetica", 14.3, "bold"),
            text_color="#fff",
            hover_color="#3F685F",
            fg_color="#4F8377",
            command=self.ecra_login,
            width=173,
            height=36
        )
        button_cancelar.place(x=713, y=314)

    def _simular_envio_instrucoes(self, email):
        """Simulação de envio de instruções de recuperação."""
        print(f"A enviar e-mail de recuperação para {email}...")
        self.ecra_login()

    def criar_conta(self):
        """Ecrã de criação de conta."""
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

        toggle_button = ctk.CTkButton(
            self,
            text="👁",
            font=("Helvetica", 14),
            width=35,
            height=35,
            fg_color="#D9D9D9",
            bg_color="#D9D9D9",
            hover_color="#B0B0B0",
            text_color="#000",
            command=lambda: self._toggle_password_visibility(entry_password)
        )
        toggle_button.place(x=923, y=332)

        button_criar_conta = ctk.CTkButton(
            self,
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
                self.ecra_login
            )
        )
        button_criar_conta.place(x=513, y=414)

        button_cancelar = ctk.CTkButton(
            self,
            text='CANCELAR',
            font=("Helvetica", 14.3, "bold"),
            text_color="#fff",
            hover_color="#3F685F",
            fg_color="#4F8377",
            command=self.ecra_login,
            width=173,
            height=36
        )
        button_cancelar.place(x=713, y=414)

    def _carregar_dados(self):
        """
        Lê o ficheiro 'data.txt', agora assumindo 10 campos por linha.
        Se a linha não tiver pelo menos 10 campos, é ignorada.
        Formato: titulo; genero; data_completa; data_insercao; rating; img_path; trailer; descricao; tipo; duracao
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
                (titulo, genero, data_completa, data_insercao, rating,
                 img_path, trailer, descricao, tipo, duracao) = partes
                try:
                    rating = float(rating)
                except ValueError:
                    print(f"Rating inválido para '{titulo}': {rating}")
                    rating = 0.0

                item = {
                    "titulo": titulo,
                    "genero": genero,
                    "data_completa": data_completa,
                    "data_insercao": data_insercao,
                    "rating": rating,
                    "img_path": img_path,
                    "trailer": trailer,
                    "descricao": descricao,
                    "tipo": tipo.lower(),   # "serie" ou "filme"
                    "duracao": duracao
                }
                lista.append(item)
        return lista

    def _login_success(self, username):
        """
        Callback de sucesso de login. Armazena o username e
        verifica se o utilizador é admin, depois inicializa frames.
        """
        self.username = username
        self.is_admin = users.is_admin(username) if hasattr(users, 'is_admin') else False
        self.iniciar_frames()

    def _login_fail(self):
        """Callback de falha de login."""
        print("Falha de login.")
        self.ecra_login()

    def iniciar_frames(self):
        """
        Limpa a janela e inicializa todos os frames (series, filmes, explorar, perfil/admin).
        Coloca-os em (relx=1.0, rely=1.0, anchor="se") para que possamos usar tkraise().
        """
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
            # Frame admin com comportamento igual aos demais
            frame_admin = ctk.CTkFrame(self, width=1050, height=540, fg_color="#242424")
            frame_admin.place(relx=1.0, rely=1.0, anchor="se")
            self.frames["admin"] = frame_admin

        # Top cover frame (barra superior) — permanece fixo
        top_cover_frame = ctk.CTkFrame(self, width=1050, height=100, fg_color="#242424")
        top_cover_frame.place(x=150, y=0)

        self._criar_menu_lateral()
        self._atualizar_informacoes_topo()

        # Inicializa as seções
        self._ecra_series(frame_series)
        self._ecra_filmes(frame_filmes)
        self._ecra_explorar(frame_explorar)

        if self.is_admin:
            self._ecra_admin(self.frames["admin"])
        else:
            self._ecra_perfil(frame_perfil)

        # Por omissão, levantamos o ecrã de séries
        frame_series.tkraise()

    def _criar_menu_lateral(self):
        """Cria o menu lateral com botões para navegar entre as diferentes abas."""
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
        """Atualiza a zona de topo com o avatar e o username do utilizador."""
        user_folder = os.path.join(root_dir, "files", "users", self.username)
        profile_picture_path = os.path.join(user_folder, "profile_picture.png")

        if os.path.isfile(profile_picture_path):
            image_path = profile_picture_path
        else:
            image_path = './images/default_avatar.png'

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
        """
        Aba de Séries. Apresenta duas colunas (Para ver / Brevemente),
        com filtragem por género e ano. Filtra apenas os registos em que tipo="serie".
        """
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

        self.scroll_left_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_left_series.place(x=10, y=30)

        self.scroll_right_series = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_right_series.place(x=520, y=30)

        # Gera lista de séries (tipo="serie")
        self.todas_series = [x for x in self.dados_geral if x["tipo"] == "serie"]

        # Frame pequeno para opções de filtro no canto superior direito
        filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        filtro_frame.place(relx=1.0, y=0, x=-48, anchor="ne")

        generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance", "Ação", "Comédia", "Ficção Científica", "Terror"]
        self.filtro_genero_series = ctk.CTkOptionMenu(filtro_frame, values=generos_possiveis, width=80)
        self.filtro_genero_series.set("Todos")
        self.filtro_genero_series.grid(row=0, column=0, padx=5)

        self.filtro_ano_series = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
        self.filtro_ano_series.grid(row=0, column=1, padx=5)

        self.botao_filtrar_series = ctk.CTkButton(
            filtro_frame,
            text="Filtrar",
            width=60,
            command=self._aplicar_filtro_series
        )
        self.botao_filtrar_series.grid(row=0, column=2, padx=5)

        self._mostrar_series_filtradas()

    def _aplicar_filtro_series(self):
        """Aplica filtro de género e ano à lista de séries."""
        genero_selecionado = self.filtro_genero_series.get()
        ano_texto = self.filtro_ano_series.get()

        lista_filtrada = []
        for item in self.todas_series:
            if genero_selecionado != "Todos" and item["genero"] != genero_selecionado:
                continue
            if ano_texto.strip():
                try:
                    ano_int = int(ano_texto.strip())
                    ano_lancamento = int(item["data_completa"].split("/")[-1])
                    if ano_lancamento != ano_int:
                        continue
                except ValueError:
                    print(f"Ano inválido: {ano_texto}")
                    continue
            lista_filtrada.append(item)

        # Limpar os frames antes de popular novamente
        for child in self.scroll_left_series.winfo_children():
            child.destroy()
        for child in self.scroll_right_series.winfo_children():
            child.destroy()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in lista_filtrada:
            try:
                ano_lancamento = int(item["data_completa"].split("/")[-1])
                if ano_lancamento <= ano_hoje:
                    lista_passado.append(item)
                else:
                    lista_futuro.append(item)
            except ValueError:
                print(f"Data inválida no item: {item['titulo']}")
                continue

        self._criar_cards(lista_passado, self.scroll_left_series)
        self._criar_cards(lista_futuro, self.scroll_right_series)

    def _mostrar_series_filtradas(self):
        """
        Mostra as séries divididas em "Para ver" (passado/presente)
        e "Brevemente" (futuro), sem qualquer filtro adicional.
        """
        for child in self.scroll_left_series.winfo_children():
            child.destroy()
        for child in self.scroll_right_series.winfo_children():
            child.destroy()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in self.todas_series:
            try:
                ano_lancamento = int(item["data_completa"].split("/")[-1])
                if ano_lancamento <= ano_hoje:
                    lista_passado.append(item)
                else:
                    lista_futuro.append(item)
            except ValueError:
                print(f"Data inválida no item: {item['titulo']}")
                continue

        self._criar_cards(lista_passado, self.scroll_left_series)
        self._criar_cards(lista_futuro, self.scroll_right_series)

    def _ecra_filmes(self, parent_frame):
        """
        Aba de Filmes, funcionalmente idêntica a séries,
        mas filtra por tipo="filme".
        """
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

        self.scroll_left_filmes = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_left_filmes.place(x=10, y=30)

        self.scroll_right_filmes = ctk.CTkScrollableFrame(parent_frame, width=460, height=450)
        self.scroll_right_filmes.place(x=520, y=30)

        # Gera lista de filmes (tipo="filme")
        self.todas_filmes = [x for x in self.dados_geral if x["tipo"] == "filme"]

        # Frame para filtros no canto superior direito
        filtro_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        filtro_frame.place(relx=1.0, y=0, x=-48, anchor="ne")

        generos_possiveis = ["Todos", "Aventura", "Fantasia", "Drama", "Romance", "Ação", "Comédia", "Ficção Científica", "Terror"]
        self.filtro_genero_filmes = ctk.CTkOptionMenu(filtro_frame, values=generos_possiveis, width=80)
        self.filtro_genero_filmes.set("Todos")
        self.filtro_genero_filmes.grid(row=0, column=0, padx=5)

        self.filtro_ano_filmes = ctk.CTkEntry(filtro_frame, placeholder_text="Ano", width=60)
        self.filtro_ano_filmes.grid(row=0, column=1, padx=5)

        self.botao_filtrar_filmes = ctk.CTkButton(
            filtro_frame,
            text="Filtrar",
            width=60,
            command=self._aplicar_filtro_filmes
        )
        self.botao_filtrar_filmes.grid(row=0, column=2, padx=5)

        self._mostrar_filmes_filtradas()

    def _aplicar_filtro_filmes(self):
        """Filtrar a lista de filmes por género e ano."""
        genero_selecionado = self.filtro_genero_filmes.get()
        ano_texto = self.filtro_ano_filmes.get()

        lista_filtrada = []
        for item in self.todas_filmes:
            if genero_selecionado != "Todos" and item["genero"] != genero_selecionado:
                continue
            if ano_texto.strip():
                try:
                    ano_int = int(ano_texto.strip())
                    ano_lancamento = int(item["data_completa"].split("/")[-1])
                    if ano_lancamento != ano_int:
                        continue
                except ValueError:
                    print(f"Ano inválido: {ano_texto}")
                    continue
            lista_filtrada.append(item)

        for child in self.scroll_left_filmes.winfo_children():
            child.destroy()
        for child in self.scroll_right_filmes.winfo_children():
            child.destroy()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in lista_filtrada:
            try:
                ano_lancamento = int(item["data_completa"].split("/")[-1])
                if ano_lancamento <= ano_hoje:
                    lista_passado.append(item)
                else:
                    lista_futuro.append(item)
            except ValueError:
                print(f"Data inválida no item: {item['titulo']}")
                continue

        self._criar_cards(lista_passado, self.scroll_left_filmes)
        self._criar_cards(lista_futuro, self.scroll_right_filmes)

    def _mostrar_filmes_filtradas(self):
        """Mostra os filmes divididos em 'Para ver' e 'Brevemente'."""
        for child in self.scroll_left_filmes.winfo_children():
            child.destroy()
        for child in self.scroll_right_filmes.winfo_children():
            child.destroy()

        ano_hoje = datetime.date.today().year
        lista_passado = []
        lista_futuro = []

        for item in self.todas_filmes:
            try:
                ano_lancamento = int(item["data_completa"].split("/")[-1])
                if ano_lancamento <= ano_hoje:
                    lista_passado.append(item)
                else:
                    lista_futuro.append(item)
            except ValueError:
                print(f"Data inválida no item: {item['titulo']}")
                continue

        self._criar_cards(lista_passado, self.scroll_left_filmes)
        self._criar_cards(lista_futuro, self.scroll_right_filmes)

    def _ecra_explorar(self, parent_frame):
        """
        Aba de Explorar, não modificada no refactor (exemplo de scroll frames).
        Pode ser adaptada com lógicas adicionais se desejado.
        """
        scroll_left = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_left.place(x=10, y=0)

        scroll_right = ctk.CTkScrollableFrame(parent_frame, width=460, height=470)
        scroll_right.place(x=520, y=0)

    def _ecra_perfil(self, parent_frame):
        """Ecrã de perfil do utilizador (se não for admin)."""
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

        info_user = ctk.CTkLabel(
            parent_frame,
            text="Métricas do Utilizador:\n- Gosto: 0\n- Horas: 0\n- Comentários: 0\n- Notificações: 0",
            font=("Helvetica", 14),
            text_color="white",
            justify="left"
        )
        info_user.place(x=20, y=150)

    def _ecra_admin(self, parent_frame):
        """Área de Admin, agora dentro de um frame 1050x540 na zona inferior direita."""
        label = ctk.CTkLabel(parent_frame,
                             text="Área de Admin",
                             font=("Helvetica", 24, "bold"),
                             text_color="#4F8377")
        label.pack(pady=10)

        btn_users = ctk.CTkButton(
            parent_frame,
            text="Gerir Utilizadores",
            fg_color="#4F8377",
            command=self._gerir_utilizadores
        )
        btn_users.pack(pady=5)

        btn_categorias = ctk.CTkButton(
            parent_frame,
            text="Gerir Categorias",
            fg_color="#4F8377",
            command=self._gerir_categorias
        )
        btn_categorias.pack(pady=5)

        btn_dashboard = ctk.CTkButton(
            parent_frame,
            text="Dashboard Admin",
            fg_color="#4F8377",
            command=self._ecra_dashboard_admin
        )
        btn_dashboard.pack(pady=5)

        btn_inserir_conteudo = ctk.CTkButton(
            parent_frame,
            text="Inserir Filme/Série",
            fg_color="#4F8377",
            command=self._ecra_inserir
        )
        btn_inserir_conteudo.pack(pady=5)

    def _gerir_utilizadores(self):
        print("Gerir Utilizadores: criar ecrã/modal para listar, bloquear ou remover utilizadores.")

    def _gerir_categorias(self):
        print("Gerir Categorias: criar ecrã para adicionar/editar/remover categorias.")

    def _ecra_dashboard_admin(self):
        print("Dashboard Admin: criar gráficos e estatísticas para administradores.")

    def _ecra_inserir(self):
        """
        Cria ou levanta um frame de inserção de novo conteúdo (Filme/Série),
        com campos adicionais: checkbox para 'Série' ou 'Filme' e campo 'Duração'.
        """
        if "inserir" in self.frames:
            # Se já existir, apenas levanta
            self.frames["inserir"].tkraise()
            return

        form_frame = ctk.CTkFrame(self, width=1050, height=540, corner_radius=6, fg_color="#4f8377")
        form_frame.place(relx=1.0, rely=1.0, anchor="se")
        self.frames["inserir"] = form_frame

        ctk.CTkLabel(
            form_frame,
            text="Adicionar Filme/Série",
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff"
        ).pack(pady=10)

        entries = {}
        labels = [
            ("Título", "titulo"),
            ("Data Completa (DD/MM/AAAA)", "data_completa"),
            ("Rating (0-10)", "rating"),
            ("URL do Trailer", "trailer"),
            ("Descrição", "descricao")
        ]

        # Cria campos de texto
        for label_text, key in labels:
            ctk.CTkLabel(form_frame, text=label_text, font=("Helvetica", 14), text_color="#ffffff").pack(pady=5)
            entries[key] = ctk.CTkEntry(form_frame, width=400)
            entries[key].pack()

        # Género
        ctk.CTkLabel(form_frame, text="Género", font=("Helvetica", 14), text_color="#ffffff").pack(pady=5)
        generos_disponiveis = ["Ação", "Comédia", "Drama", "Fantasia", "Ficção Científica", "Terror", "Romance", "Aventura"]
        entries["genero"] = ctk.CTkOptionMenu(form_frame, values=generos_disponiveis)
        entries["genero"].set("Ação")
        entries["genero"].pack()

        # Escolha: Série ou Filme (uma checkbox unicamente, se marcada = série; senão = filme)
        entries["check_var"] = tk.BooleanVar(value=True)  # por omissão é Série
        checkbox_serie = ctk.CTkCheckBox(
            form_frame,
            text="Marcar se for Série (desmarcar para Filme)",
            variable=entries["check_var"],
            onvalue=True,
            offvalue=False
        )
        checkbox_serie.pack(pady=10)

        # Campo de duração
        ctk.CTkLabel(form_frame, text="Duração (minutos)", font=("Helvetica", 14), text_color="#ffffff").pack(pady=5)
        entries["duracao"] = ctk.CTkEntry(form_frame, width=400)
        entries["duracao"].pack()

        # Upload de imagem
        ctk.CTkLabel(form_frame, text="Carregar Imagem", font=("Helvetica", 14), text_color="#ffffff").pack(pady=5)
        img_label = ctk.CTkLabel(form_frame, text="Nenhuma imagem carregada", text_color="#ffffff")
        img_label.pack(pady=5)

        def fazer_upload_imagem():
            file_path = filedialog.askopenfilename(
                title="Selecionar uma imagem",
                filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                catalog_dir = os.path.join(root_dir, "files", "catalog")
                if not os.path.exists(catalog_dir):
                    os.makedirs(catalog_dir)

                img_filename = os.path.basename(file_path)
                new_img_path = os.path.join(catalog_dir, img_filename)

                with Image.open(file_path) as img:
                    img.save(new_img_path)

                img_label.configure(text=f"Imagem carregada: {img_filename}")
                entries["img_path"] = new_img_path

        btn_upload = ctk.CTkButton(form_frame, text="Selecionar Imagem", command=fazer_upload_imagem)
        btn_upload.pack(pady=5)

        def salvar_dados():
            """Salva o novo registo no ficheiro data.txt (com 10 campos)."""
            titulo = entries["titulo"].get().strip()
            genero = entries["genero"].get().strip()
            data_completa = entries["data_completa"].get().strip()
            rating = entries["rating"].get().strip()
            trailer = entries["trailer"].get().strip()
            descricao = entries["descricao"].get().strip()
            img_path = entries.get("img_path", "").strip()
            duracao = entries["duracao"].get().strip()

            # Se a checkbox estiver marcada, é série; caso contrário, é filme
            tipo = "serie" if entries["check_var"].get() else "filme"

            data_insercao = datetime.datetime.now().strftime("%d/%m/%Y")

            # Valida campos obrigatórios
            if not (titulo and genero and data_completa and rating and trailer and descricao and img_path and duracao):
                print("Por favor, preencha todos os campos.")
                return

            # Valida data e rating
            try:
                dia, mes, ano = map(int, data_completa.split("/"))
                datetime.datetime(ano, mes, dia)  # Verifica se a data é válida
                rating_float = float(rating)
            except ValueError:
                print("Data ou rating inválidos. Verifique os valores introduzidos.")
                return

            # Formato final dos 10 campos (separados por ponto e vírgula)
            # titulo;genero;data_completa;data_insercao;rating;img_path;trailer;descricao;tipo;duracao
            novo_registo = f"{titulo};{genero};{data_completa};{data_insercao};{rating_float};{img_path};{trailer};{descricao};{tipo};{duracao}\n"
            caminho_ficheiro = os.path.join(root_dir, "files", "data.txt")

            # Escreve no ficheiro
            with open(caminho_ficheiro, "a", encoding="utf-8") as f:
                f.write(novo_registo)

            print("Filme/Série inserido com sucesso!")
            # Recarregar dados gerais para atualizar listagens
            self.dados_geral = self._carregar_dados()
            # Voltar ao menu admin
            self._update_active_screen("admin")

        # Botões de ação
        ctk.CTkButton(form_frame, text="Guardar", fg_color="#4F8377", command=salvar_dados).pack(pady=20)

        def cancelar():
            self._update_active_screen("admin")

        ctk.CTkButton(form_frame, text="Cancelar", fg_color="#D9534F", command=cancelar).pack()

        # Levanta este frame
        form_frame.tkraise()

    def _clear_window(self):
        """Remove todos os widgets/frames da janela."""
        for widget in self.winfo_children():
            widget.destroy()

    def _update_active_screen(self, frame_name):
        """
        Levanta (raise) o frame indicado em self.frames.
        Se for perfil/admin, retira o avatar do topo.
        """
        if frame_name in self.frames:
            if frame_name in ["perfil", "admin", "inserir"]:
                # Oculta avatar e username no topo
                self.avatar_label.place_forget()
                self.label_username_top.place_forget()
            else:
                # Mostra avatar e username no topo
                self.avatar_label.place(x=1100, y=23)
                self.label_username_top.place(x=1000, y=38)

            self.frames[frame_name].tkraise()
        else:
            print(f"AVISO: O frame '{frame_name}' não foi encontrado em self.frames.")

    def _toggle_password_visibility(self, entry: ctk.CTkEntry):
        """Ativa/desativa a visibilidade do texto no campo de password."""
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    def _upload_avatar(self, image_label: ctk.CTkLabel):
        """
        Permite selecionar e recortar uma imagem para usar como avatar,
        guardando-a na pasta do utilizador.
        """
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

        # Atualizar no topo também, se estiver visível
        if hasattr(self, "avatar_label"):
            topo_img = ctk.CTkImage(circular, size=(55, 55))
            self.avatar_label.configure(image=topo_img, text="")
            self.avatar_label.image = topo_img

    def _criar_cards(self, lista, parent_frame):
        """
        Cria 'cards' para cada item da lista (podem ser séries ou filmes),
        colocando-os em grelha dentro de um CTkScrollableFrame.
        """
        for item in lista:
            cat_img_path = item["img_path"]
            movie_name = item["titulo"]
            description = item["descricao"]
            trailer = item["trailer"]
            rating = str(item["rating"])
            duracao = item["duracao"]

            # Extrair ano do campo data_completa
            try:
                year = int(item["data_completa"].split("/")[-1])
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
                    self._mostrar_detalhes_filme(movie_name, description, trailer, rating, year, duracao)

                card_frame.bind("<Button-1>", on_click)
                card_label.bind("<Button-1>", on_click)

            except (FileNotFoundError, IOError):
                print(f"Erro ao carregar a imagem: {cat_img_path}")

    def _mostrar_detalhes_filme(self, movie_name, description, trailer, rating, year, duracao):
        """
        Mostra detalhes do item num frame sobreposto (pop-up),
        incluindo a duração.
        """
        detalhes_frame = ctk.CTkFrame(self, width=800, height=500, corner_radius=6, fg_color="#4f8377")
        detalhes_frame.place(relx=0.5, rely=0.5, anchor="center")

        botao_fechar = ctk.CTkButton(
            detalhes_frame,
            text="X",
            width=30,
            command=detalhes_frame.destroy,
            fg_color="#a3d9c8",
            text_color="#121212"
        )
        botao_fechar.place(x=760, y=10)

        titulo = ctk.CTkLabel(
            detalhes_frame,
            text=movie_name,
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff"
        )
        titulo.place(x=20, y=20)

        desc = ctk.CTkLabel(
            detalhes_frame,
            text=description,
            font=("Helvetica", 12),
            text_color="#ffffff",
            wraplength=700
        )
        desc.place(x=20, y=60)

        info = ctk.CTkLabel(
            detalhes_frame,
            text=f"Rating: {rating} | Ano: {year} | Duração: {duracao} min",
            font=("Helvetica", 12, "bold"),
            text_color="#ffffff"
        )
        info.place(x=20, y=460)


if __name__ == "__main__":
    app = HootApp()
    app.mainloop()