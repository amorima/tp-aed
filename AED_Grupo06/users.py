import os
import datetime
import CTkMessagebox

user_db = ".\\files\\users.txt"
user_ativo = None

# ------------------------------------------
# Ler Ficheiro
# ------------------------------------------
def lerFicheiro(ficheiro):
    lista = []
    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as file:
            lista = file.readlines()
    return lista

# ------------------------------------------
# Checker para Password
# ------------------------------------------
def passwordChecker(password):
    """
    Password deve ter:
    - Pelo menos 8 caracteres
    - 1 letra maiúscula
    - 1 número
    - 1 caracter especial
    - NÃO pode ter ponto e vírgula (;)
    """
    if len(password) < 8:
        return "-Deve conter pelo menos 8 caracteres\n"

    capitalUsed = any(c.isupper() for c in password)
    if not capitalUsed:
        return "-Deve conter pelo menos uma maiúscula\n"

    numberUsed = any(c.isdigit() for c in password)
    if not numberUsed:
        return "-Deve conter pelo menos um número\n"

    specialUsed = any(not c.isalnum() for c in password)
    if not specialUsed:
        return "-Deve conter pelo menos um caracter especial\n"

    if ";" in password:
        return "-Caracter ';' não é válido\n"

    return "True"

# ------------------------------------------
# Checker para Email
# ------------------------------------------
def emailChecker(email):
    """
    - Email deve conter '@'
    - Não pode ter ';'
    Retorna "True" se válido, caso contrário, devolve a mensagem de erro.
    """
    if ";" in email:
        return "-Email não pode conter ponto e vírgula (;)\n"
    if "@" not in email:
        return "-Email deve conter '@'\n"
    return "True"

# ------------------------------------------
# Obter dados de um utilizador (by Email)
# ------------------------------------------
def get_user_data_by_email(email):
    """
    Retorna uma tupla (username, password, email, role, data)
    ou None se não existir um utilizador com esse email.
    """
    userList = lerFicheiro(user_db)
    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 5:
            # Linha inválida ou com formatação antiga
            continue
        # campos = [username, password, email, role, data]
        if campos[2] == email:
            return campos[0], campos[1], campos[2], campos[3], campos[4]
    return None

# ------------------------------------------
# Verificar se user é Admin
# ------------------------------------------
def is_admin(username):
    """
    Verifica se um determinado 'username' tem papel Admin.
    """
    userList = lerFicheiro(user_db)
    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 4:
            continue
        if campos[0] == username:
            return campos[3].strip().lower() == "admin"
    return False

# ------------------------------------------
# Update Login Date
# ------------------------------------------

def update_login_date(email):
    """
    Atualiza a data de registo (5º campo) para a data/hora atual,
    localizando o user pelo email.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    userList = lerFicheiro(user_db)
    updated_user_db = []

    for line in userList:
        campos = line.strip().split(";")
        if len(campos) < 5:
            # Mantém linhas mal-formadas (ou antigas), ou podes ignorar/descartar
            updated_user_db.append(line)
            continue

        # Se for o user que queremos (mesmo email), altera o 5º campo
        if campos[2] == email:
            campos[4] = current_date
            updated_line = ";".join(campos) + "\n"
            updated_user_db.append(updated_line)
        else:
            # Caso não seja o user que procuramos, mantém a linha original
            if not line.endswith("\n"):
                line += "\n"
            updated_user_db.append(line)

    # Reescreve o ficheiro
    with open(user_db, "w", encoding="utf-8") as f:
        for line in updated_user_db:
            f.write(line)

# ------------------------------------------
# Log In
# ------------------------------------------
def logIn(password, mail, fn_after_login, fn_close_login):
    global user_ativo, username
    user_ativo = None

    user_data = get_user_data_by_email(mail)
    if user_data is not None:
        # user_data -> (username, db_password, db_email, role, db_date)
        username, db_password, db_email, role, db_date = user_data
        if password == db_password:
            # Credenciais corretas
            user_ativo = username

            # Atualiza a data para a data/hora atual
            update_login_date(mail)

            # Chamamos as funções callback
            fn_close_login()
            fn_after_login(username)
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

# ------------------------------------------
# Sign / Criar Conta
# ------------------------------------------
def sign(user, password, mail, fn_after_sign):
    """
    Cria um novo utilizador no ficheiro user_db.
    Formato (agora com 5 campos):
        Username;Password;Email;Role;Data
    """
    # 1) Valida password
    validPassword = passwordChecker(password)
    if validPassword != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="A password não é válida:\n" + validPassword,
            icon="warning",
            option_1="Ok"
        )
        return

    # 2) Valida mail
    validMail = emailChecker(mail)
    if validMail != "True":
        CTkMessagebox.CTkMessagebox(
            title="Sign in",
            message="Email inválido:\n" + validMail,
            icon="warning",
            option_1="Ok"
        )
        return

    # 3) Valida username
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

    # 4) Verifica se user ou email já existem
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

    # 5) Adiciona linha no ficheiro com 5º campo (data do registo)
    data_registo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(user_db, "a", encoding="utf-8") as f:
        f.write(f"{user};{password};{mail};User;{data_registo}\n")

    # 6) Callback pós-criação
    fn_after_sign()

# ------------------------------------------
# Mudar Username
# ------------------------------------------
def changeUser(user, password, newUser):
    """
    Altera o 'username' para 'newUser' (se a password for correta).
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
        if campos[0] == user and campos[1] == password:
            # Encontrou o user e password corretos
            newUser_db.append(newUser + ";" + campos[1] + ";" + campos[2] + ";" + campos[3] + "\n")
            changed = True
        else:
            # Copia a linha sem alterações
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for line in newUser_db:
            file.write(line if line.endswith("\n") else (line + "\n"))

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Username Change",
            message="Não foi possível alterar (username ou password incorretos).",
            icon="warning",
            option_1="Ok"
        )

# ------------------------------------------
# Mudar Password
# ------------------------------------------
def changePass(user, oldPassword, newPassword):
    """
    Altera a password do 'user' (se oldPassword for correta).
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
            newUser_db.append(campos[0] + ";" + newPassword + ";" + campos[2] + ";" + campos[3] + "\n")
            changed = True
        else:
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for line in newUser_db:
            file.write(line if line.endswith("\n") else (line + "\n"))

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Password Change",
            message="Password antiga incorreta ou user não encontrado.",
            icon="warning",
            option_1="Ok"
        )

# ------------------------------------------
# Mudar Email
# ------------------------------------------
def changeMail(user, oldPassword, newMail):
    """
    Altera o email do 'user' (se a password for correta e o newMail for válido).
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
            newUser_db.append(campos[0] + ";" + campos[1] + ";" + newMail + ";" + campos[3] + "\n")
            changed = True
        else:
            newUser_db.append(line)

    with open(user_db, "w", encoding="utf-8") as file:
        for line in newUser_db:
            file.write(line if line.endswith("\n") else (line + "\n"))

    if not changed:
        CTkMessagebox.CTkMessagebox(
            title="Mail Change",
            message="Password antiga incorreta ou user não encontrado.",
            icon="warning",
            option_1="Ok"
        )


import os

def set_admin(username):
    """
    Marca o estado do usuário como 'admin' (ou define um flag).
    Necessário ter algo como userinfo.txt em users/<username>/
    """
    users_dir = os.path.join(".", "files", "users")
    user_folder = os.path.join(users_dir, username)

    if not os.path.exists(user_folder):
        print(f"Usuário {username} não existe.")
        return

    userinfo_path = os.path.join(user_folder, "userinfo.txt")
    # Se não existir, cria. Se existir, reescreve 'estado=admin'.
    lines = []
    found_estado = False

    if os.path.isfile(userinfo_path):
        with open(userinfo_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_content = []
    for ln in lines:
        if ln.strip().startswith("estado="):
            new_content.append("estado=admin\n")
            found_estado = True
        else:
            new_content.append(ln)

    if not found_estado:
        new_content.append("estado=admin\n")

    with open(userinfo_path, "w", encoding="utf-8") as f:
        f.writelines(new_content)

    print(f"Usuário {username} promovido a admin.")


def block_user(username, dias=15):
    """
    Marca o estado do usuário como 'bloqueado' e, opcionalmente,
    armazena a data de bloqueio ou algo assim. Exemplo simples:
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

    print(f"Usuário {username} bloqueado por {dias} dias (exemplo).")


def remove_user(username):
    """
    Remove a pasta do usuário e todo o conteúdo.
    **CUIDADO**: isso apaga os dados desse user permanentemente!
    """
    import shutil
    users_dir = os.path.join(".", "files", "users")
    user_folder = os.path.join(users_dir, username)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)  # apaga tudo
        print(f"Usuário {username} removido completamente!")
    else:
        print(f"Usuário {username} não existe.")


def get_all_users():
    """
    Lê cada subpasta em ./files/users e tenta ler um arquivo userinfo.txt
    para descobrir o 'username', 'email' e 'estado'.
    Retorna lista de dicionários: [{"username":..., "email":..., "estado":...}, ...]
    """
    users_dir = os.path.join(".", "files", "users")
    lista_users = []

    if not os.path.exists(users_dir):
        return lista_users  # Se não existir, lista vazia

    for pasta in os.listdir(users_dir):
        caminho_pasta = os.path.join(users_dir, pasta)
        if os.path.isdir(caminho_pasta):
            # Tenta ler userinfo.txt
            user_info_path = os.path.join(caminho_pasta, "userinfo.txt")
            username_ = pasta  # se não achar nada, ao menos o nome da pasta
            email_ = ""
            estado_ = "ativo"  # default

            if os.path.isfile(user_info_path):
                # Exemplo de formato do userinfo.txt:
                # username=joao
                # email=joao@email.com
                # estado=ativo
                with open(user_info_path, "r", encoding="utf-8") as f:
                    for linha in f:
                        linha = linha.strip()
                        if "=" in linha:
                            chave, valor = linha.split("=", 1)
                            chave = chave.strip()
                            valor = valor.strip()
                            if chave == "username":
                                username_ = valor
                            elif chave == "email":
                                email_ = valor
                            elif chave == "estado":
                                estado_ = valor

            lista_users.append({
                "username": username_,
                "email": email_,
                "estado": estado_
            })

    # Se quiser ordenar, ex: por username e depois email:
    lista_users.sort(key=lambda u: (u["username"].lower(), u["email"].lower(), u["estado"].lower()))
    return lista_users

# ------------------------------------------
# Favoritos
# ------------------------------------------
def addFavorite(user, item):
    """
    Adiciona 'item' à lista de favoritos do 'user'.
    """
    # Cria pasta user_data se não existir
    if not os.path.isdir(f".\\files\\user_data\\{user}"):
        os.makedirs(f".\\files\\user_data\\{user}")

    favorites_file = f".\\files\\user_data\\{user}\\favorites.txt"
    # Cria o ficheiro se não existir
    if not os.path.isfile(favorites_file):
        open(favorites_file, 'w').close()

    with open(favorites_file, 'a', encoding="utf-8") as file:
        file.write(item + "\n")

def removeFavorite(user, item):
    """
    Remove 'item' da lista de favoritos do 'user'.
    """
    favorites_file = f".\\files\\user_data\\{user}\\favorites.txt"
    if not os.path.exists(favorites_file):
        return  # Se não existe, não há nada para remover

    favoritesList = lerFicheiro(favorites_file)
    newFavoritesList = []

    for line in favoritesList:
        if line.strip() != item:
            newFavoritesList.append(line)

    # Reescreve o ficheiro de favoritos
    with open(favorites_file, "w", encoding="utf-8") as file:
        for line in newFavoritesList:
            file.write(line if line.endswith("\n") else (line + "\n"))

# ------------------------------------------
# Ratings
# ------------------------------------------
def addRating(user, item, rating):
    """
    Adiciona rating a 'item'.
    Ex.: rating entre 0 e 5 (string ou int).
    Ficheiro: .\\files\\catalog_data\\{item}\\reviews.txt
    Formato: "user;rating"
    """
    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.makedirs(f".\\files\\catalog_data\\{item}")

    reviews_file = f".\\files\\catalog_data\\{item}\\reviews.txt"
    if not os.path.isfile(reviews_file):
        open(reviews_file, 'w').close()

    with open(reviews_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{rating}\n")

# ------------------------------------------
# Comentários
# ------------------------------------------
def addComment(user, item, comment):
    """
    Adiciona comentário a 'item'.
    Formato: "user;comentário"
    """
    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.makedirs(f".\\files\\catalog_data\\{item}")

    comments_file = f".\\files\\catalog_data\\{item}\\comments.txt"
    if not os.path.isfile(comments_file):
        open(comments_file, 'w').close()

    with open(comments_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{comment}\n")

# ------------------------------------------
# Likes
# ------------------------------------------
def addLike(user, item, like):
    if not os.path.isdir(f".\\files\\user_data\\{user}"):
        os.makedirs(f".\\files\\user_data\\{user}")

    likes_file = f".\\files\\user_data\\{user}\\likes.txt"
    if not os.path.isfile(likes_file):
        open(likes_file, 'w').close()

    with open(likes_file, 'a', encoding="utf-8") as file:
        file.write(f"{item};{like}\n")

# ------------------------------------------
# Notificações (placeholder)
# ------------------------------------------
def notificationRead(id):
    """
    Marca a notificação 'id' como lida.
    Ex.: isto dependerá da forma como guardas as notificações.
    """
    # TODO: Implementar de acordo com a tua lógica de notificações
    pass
