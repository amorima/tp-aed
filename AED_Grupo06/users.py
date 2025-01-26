import os
import datetime
import shutil
import CTkMessagebox
from PIL import Image

# ------------------------------------------------------------------------
#                VARIÁVEIS GLOBAIS (BASE DE DADOS / FICHEIROS)
# ------------------------------------------------------------------------
user_db = ".\\files\\users.txt"    # Caminho para o ficheiro onde estão guardados os utilizadores
user_ativo = None                  # Para armazenar o user atualmente autenticado (se aplicável)

# ------------------------------------------------------------------------
#                   FUNÇÕES DE SUPORTE / UTILITÁRIAS
# ------------------------------------------------------------------------
def lerFicheiro(ficheiro):
    """
    Lê um ficheiro e retorna a lista de linhas (strings).
    Se o ficheiro não existir, retorna uma lista vazia.
    """
    lista = []
    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as file:
            lista = file.readlines()
    return lista

def passwordChecker(password):
    """
    Verifica se a 'password' cumpre os seguintes requisitos:
      - Pelo menos 8 caracteres
      - Pelo menos 1 letra maiúscula
      - Pelo menos 1 dígito
      - Pelo menos 1 caracter especial
      - NÃO pode conter ponto e vírgula (';')
    Se todos os requisitos forem cumpridos, retorna "True".
    Caso contrário, retorna uma string com a descrição do erro.
    """
    if len(password) < 8:
        return "-Deve conter pelo menos 8 caracteres\n"

    if not any(c.isupper() for c in password):
        return "-Deve conter pelo menos uma maiúscula\n"

    if not any(c.isdigit() for c in password):
        return "-Deve conter pelo menos um número\n"

    if not any(not c.isalnum() for c in password):
        return "-Deve conter pelo menos um caracter especial\n"

    if ";" in password:
        return "-Caracter ';' não é válido\n"

    return "True"

def emailChecker(email):
    """
    Verifica se o 'email':
      - Contém '@'
      - Não contém ponto e vírgula (';')
    Retorna "True" se for válido, caso contrário, retorna a descrição do erro.
    """
    if ";" in email:
        return "-Email não pode conter ponto e vírgula (;)\n"
    if "@" not in email:
        return "-Email deve conter '@'\n"
    return "True"

# ------------------------------------------------------------------------
#               OBTENÇÃO DE DADOS DE UTILIZADORES
# ------------------------------------------------------------------------
def get_user_data_by_email(email):
    """
    Tenta localizar o utilizador pelo campo 'email' no ficheiro user_db.
    O ficheiro tem 5 campos: Username;Password;Email;Role;Data
    Retorna uma tupla (username, password, email, role, data) se encontrar,
    ou None se não encontrar.
    """
    userList = lerFicheiro(user_db)
    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 5:
            continue
        # campos = [username, password, email, role, data_registo]
        if campos[2] == email:
            return campos[0], campos[1], campos[2], campos[3], campos[4]
    return None

def is_admin(username):
    """
    Verifica se um determinado 'username' tem papel (role) "admin" no ficheiro user_db.
    """
    userList = lerFicheiro(user_db)
    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue
        if campos[0] == username:
            return campos[3].strip().lower() == "admin"
    return False

def get_all_users():
    """
    Lê o ficheiro user_db e retorna uma lista de dicionários contendo:
      [{"username":..., "email":..., "estado":...}, ...]
    Aqui, "estado" é o campo role (User ou Admin). Se existirem mais campos, ajusta conforme.
    """
    user_list = lerFicheiro(user_db)
    new_user_list = []

    for line in user_list:
        # Ignora possivelmente a linha de cabeçalho, se existir
        if line != "Username;Password;Email;User/Admin\n":
            campos = line.split(";")
            if len(campos) >= 4:
                new_user_list.append({
                    "username": campos[0],
                    "email": campos[2],
                    "estado": campos[3]
                })
    return new_user_list

# ------------------------------------------------------------------------
#               ATUALIZAÇÃO / MODIFICAÇÃO DE DADOS
# ------------------------------------------------------------------------
def update_login_date(email):
    """
    Atualiza a data/hora do último login (5º campo do ficheiro user_db),
    para o utilizador identificado pelo 'email'.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    userList = lerFicheiro(user_db)
    updated_user_db = []

    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 5:
            # Mantém linhas mal-formadas
            updated_user_db.append(line)
            continue

        if campos[2] == email:
            # Atualiza apenas o 5º campo
            campos[4] = current_date
            updated_line = ";".join(campos) + "\n"
            updated_user_db.append(updated_line)
        else:
            if not line.endswith("\n"):
                line += "\n"
            updated_user_db.append(line)

    with open(user_db, "w", encoding="utf-8") as f:
        for line in updated_user_db:
            f.write(line)

# ------------------------------------------------------------------------
#                       OPERAÇÕES DE LOGIN/REGISTO
# ------------------------------------------------------------------------
def logIn(password, mail, fn_after_login, fn_close_login):
    """
    Tenta fazer login com (password, mail).
    Se as credenciais estiverem corretas, chama:
      - fn_close_login()  (para fechar o ecrã de login)
      - fn_after_login(username)  (passa o username)
    Caso falhe, mostra a mensagem de erro.
    """
    global user_ativo, username
    user_ativo = None

    user_data = get_user_data_by_email(mail)
    if user_data is not None:
        # user_data -> (username, db_password, db_email, role, db_date)
        username, db_password, db_email, role, db_date = user_data
        if password == db_password:
            user_ativo = username
            update_login_date(mail)
            fn_close_login()         # callback para fechar ecrã de login
            fn_after_login(username) # callback pós-login
        else:
            CTkMessagebox.CTkMessagebox(
                title="LogIn",
                message="Password Incorreta",
                icon="warning",
                option_1="Ok"
            )
    else:
        CTkMessagebox.CTkMessagebox(
            title="LogIn",
            message="User não existe.\nPor favor crie conta.",
            icon="warning",
            option_1="Ok"
        )

def sign(user, password, mail, fn_after_sign):
    """
    Cria um novo utilizador no ficheiro user_db.
    Estrutura do registo: Username;Password;Email;Role;Data
    Role por defeito: "User"
    """
    # 1) Validar password
    validPassword = passwordChecker(password)
    if validPassword != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="A password não é válida:\n" + validPassword,
            icon="warning",
            option_1="Ok"
        )
        return

    # 2) Validar email
    validMail = emailChecker(mail)
    if validMail != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="Email inválido:\n" + validMail,
            icon="warning",
            option_1="Ok"
        )
        return

    # 3) Validar username
    if len(user) < 4:
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="Username deve ter no mínimo 4 caracteres.",
            icon="warning",
            option_1="Ok"
        )
        return

    if ";" in user:
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="User não pode conter ponto e vírgula (;)",
            icon="warning",
            option_1="Ok"
        )
        return

    # 4) Verificar se já existe (username ou email)
    userList = lerFicheiro(user_db)
    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue
        if campos[0] == user:
            CTkMessagebox.CTkMessagebox(
                title="Sign in",
                message="Já existe um utilizador com esse username.",
                icon="warning",
                option_1="Ok"
            )
            return
        if campos[2] == mail:
            CTkMessagebox.CTkMessagebox(
                title="Sign in",
                message="Email já registado.",
                icon="warning",
                option_1="Ok"
            )
            return

    # 5) Criar o registo com data de criação
    data_registo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(user_db, "a", encoding="utf-8") as f:
        f.write(f"{user};{password};{mail};User;{data_registo}\n")

    # 5.1) Criar a pasta do user e colocar a imagem de avatar default
    user_folder = f".\\files\\users\\{user}"
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)

    img_default_path = ".\\images\\default_avatar.png"
    if os.path.isfile(img_default_path):
        img = Image.open(img_default_path)
        img.save(os.path.join(user_folder, "profile_picture.png"))

    # 6) Chamar callback pós-criação
    fn_after_sign()

# ------------------------------------------------------------------------
#       FUNÇÕES PARA ALTERAR USERNAME / PASSWORD / EMAIL
# ------------------------------------------------------------------------
def changeUser(user, password, newUser):
    """
    Altera o username para 'newUser', se (user, password) forem corretos.
    """
    if len(newUser) < 4:
        CTkMessagebox.CTkMessagebox(
            title="Username Change",
            message="O novo username deve ter pelo menos 4 caracteres.",
            icon="warning",
            option_1="Ok"
        )
        return

    if ";" in newUser:
        CTkMessagebox.CTkMessagebox(
            title="Username Change",
            message="Username não pode conter ';'.",
            icon="warning",
            option_1="Ok"
        )
        return

    userList = lerFicheiro(user_db)
    newUser_db = []
    changed = False

    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue
        # Se for o registo do user/password corretos, atualiza só o primeiro campo
        if campos[0] == user and campos[1] == password:
            newUser_db.append(newUser + ";" + campos[1] + ";" + campos[2] + ";" + campos[3] + ";" + (campos[4] if len(campos) > 4 else "") + "\n")
            changed = True
        else:
            # Mantém a linha tal como estava
            if not line.endswith("\n"):
                line += "\n"
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for l in newUser_db:
            file.write(l if l.endswith("\n") else (l + "\n"))

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Username Change",
            message="Não foi possível alterar (username ou password incorretos).",
            icon="warning",
            option_1="Ok"
        )

def changePass(user, oldPassword, newPassword):
    """
    Altera a password do 'user' (se a oldPassword for correta e a nova password for válida).
    """
    validPassword = passwordChecker(newPassword)
    if validPassword != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="A nova password não é válida:\n" + validPassword,
            icon="warning",
            option_1="Ok"
        )
        return

    userList = lerFicheiro(user_db)
    newUser_db = []
    changed = False

    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue
        if campos[0] == user and campos[1] == oldPassword:
            newUser_db.append(campos[0] + ";" + newPassword + ";" + campos[2] + ";" + campos[3] + ";" + (campos[4] if len(campos) > 4 else "") + "\n")
            changed = True
        else:
            if not line.endswith("\n"):
                line += "\n"
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for l in newUser_db:
            file.write(l)

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Password Change",
            message="Password antiga incorreta ou user não encontrado.",
            icon="warning",
            option_1="Ok"
        )

def changeMail(user, oldPassword, newMail):
    """
    Altera o email do 'user' (se a oldPassword for correta e newMail for válido).
    """
    validMail = emailChecker(newMail)
    if validMail != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="O novo email não é válido:\n" + validMail,
            icon="warning",
            option_1="Ok"
        )
        return

    userList = lerFicheiro(user_db)
    newUser_db = []
    changed = False

    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue

        if campos[0] == user and campos[1] == oldPassword:
            newUser_db.append(campos[0] + ";" + campos[1] + ";" + newMail + ";" + campos[3] + ";" + (campos[4] if len(campos) > 4 else "") + "\n")
            changed = True
        else:
            if not line.endswith("\n"):
                line += "\n"
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for l in newUser_db:
            file.write(l)

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Mail Change",
            message="Password antiga incorreta ou user não encontrado.",
            icon="warning",
            option_1="Ok"
        )

# ------------------------------------------------------------------------
#     FUNÇÕES PARA ADMINISTRADOR: set_admin / block_user / remove_user
# ------------------------------------------------------------------------
def set_admin(username):
    """
    Marca o utilizador com 'role=Admin' no ficheiro user_db.
    """
    user_list = lerFicheiro(user_db)
    new_user_list = []

    for line in user_list:
        if line != "Username;Password;Email;User/Admin\n":
            campos = line.split(";")
            # Espera-se que existam 5 campos (username, pass, email, role, data)
            if len(campos) >= 4 and campos[0] == username:
                campos[3] = "Admin"
            new_line = ";".join(campos)
            new_user_list.append(new_line)
        else:
            # Linha de cabeçalho, mantemos igual
            new_user_list.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for line in new_user_list:
            if not line.endswith("\n"):
                line += "\n"
            file.write(line)

    print(f"Usuário {username} promovido a admin.")

def block_user(username, dias=15):
    """
    Marca o estado do utilizador como 'bloqueado' no ficheiro ./files/users/<username>/userinfo.txt,
    adicionando/injetando a linha 'estado=bloqueado'.
    """
    users_dir = os.path.join(".", "files", "users")
    user_folder = os.path.join(users_dir, username)
    if not os.path.exists(user_folder):
        print(f"Usuário {username} não existe.")
        return

    userinfo_path = os.path.join(user_folder, "userinfo.txt")
    lines = []
    if os.path.isfile(userinfo_path):
        with open(userinfo_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_content = []
    found_estado = False
    for ln in lines:
        if ln.strip().startswith("estado="):
            new_content.append("estado=bloqueado\n")
            found_estado = True
        else:
            new_content.append(ln)

    if not found_estado:
        new_content.append("estado=bloqueado\n")

    with open(userinfo_path, "w", encoding="utf-8") as f:
        f.writelines(new_content)

    print(f"Utilizador {username} bloqueado por {dias} dias.")

def remove_user(username):
    """
    Remove a pasta do utilizador (./files/users/<username>) e o seu conteúdo.
    Atenção: isto apaga permanentemente os dados desse utilizador.
    """
    users_dir = os.path.join(".", "files", "users")
    user_folder = os.path.join(users_dir, username)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        print(f"Usuário {username} removido completamente!")
    else:
        print(f"Usuário {username} não existe.")

# ------------------------------------------------------------------------
#             FUNÇÕES DE GESTÃO DE FAVORITOS, RATINGS, ETC.
# ------------------------------------------------------------------------
def addFavorite(user, item):
    """
    Adiciona 'item' ao ficheiro favorites.txt do utilizador.
    Se o ficheiro não existir, é criado.
    """
    user_data_dir = f".\\files\\user_data\\{user}"
    if not os.path.isdir(user_data_dir):
        os.makedirs(user_data_dir)

    favorites_file = os.path.join(user_data_dir, "favorites.txt")
    if not os.path.isfile(favorites_file):
        open(favorites_file, 'w').close()  # cria ficheiro vazio

    with open(favorites_file, 'a', encoding="utf-8") as file:
        file.write(item + "\n")

def removeFavorite(user, item):
    """
    Remove 'item' do ficheiro favorites.txt do utilizador, se existir.
    """
    favorites_file = f".\\files\\user_data\\{user}\\favorites.txt"
    if not os.path.exists(favorites_file):
        return

    favoritesList = lerFicheiro(favorites_file)
    newFavoritesList = []

    for line in favoritesList:
        if line.strip() != item:
            newFavoritesList.append(line)

    with open(favorites_file, "w", encoding="utf-8") as file:
        for l in newFavoritesList:
            if not l.endswith("\n"):
                l += "\n"
            file.write(l)

def addRating(user, item, rating):
    """
    Grava um rating para 'item' no ficheiro:
      .\\files\\catalog_data\\{item}\\reviews.txt
    Formato de cada linha: "user;rating"
    """
    item_dir = f".\\files\\catalog_data\\{item}"
    if not os.path.isdir(item_dir):
        os.makedirs(item_dir)

    reviews_file = os.path.join(item_dir, "reviews.txt")
    if not os.path.isfile(reviews_file):
        open(reviews_file, 'w').close()

    with open(reviews_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{rating}\n")

def addComment(user, item, comment):
    """
    Adiciona um comentário a 'item' no ficheiro:
      .\\files\\catalog_data\\{item}\\comments.txt
    Formato de cada linha: "user;comentário"
    """
    item_dir = f".\\files\\catalog_data\\{item}"
    if not os.path.isdir(item_dir):
        os.makedirs(item_dir)

    comments_file = os.path.join(item_dir, "comments.txt")
    if not os.path.isfile(comments_file):
        open(comments_file, 'w').close()

    with open(comments_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{comment}\n")

def addLike(user, item, like):
    """
    Grava um 'like' (ou uma espécie de flag) para 'item' no ficheiro:
      .\\files\\user_data\\{user}\\likes.txt
    Formato de cada linha: "item;like"
    """
    user_data_dir = f".\\files\\user_data\\{user}"
    if not os.path.isdir(user_data_dir):
        os.makedirs(user_data_dir)

    likes_file = os.path.join(user_data_dir, "likes.txt")
    if not os.path.isfile(likes_file):
        open(likes_file, 'w').close()

    with open(likes_file, 'a', encoding="utf-8") as file:
        file.write(f"{item};{like}\n")

def notificationRead(id):
    """
    Marca a notificação 'id' como lida.
    (Placeholder - implementar de acordo com a lógica real de notificações)
    """
    pass