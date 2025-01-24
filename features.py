#Biblioteca
#-----------
import os
import datetime
import CTkMessagebox
import tkinter as tk
#Files
#-----------------------------------
user_db=".\\files\\user.txt"
category_db=".\\files\\categories.txt"
catalog_db=".\\files\\catalog.txt"
ban_list=".\\files\\ban_list.txt"
global_notification=".\\files\\notifications.txt"

def lerFicheiro(ficheiro):
    """
    Arg:
        file path|str
    Return:
        file content|list
    """
    lista = []
    if os.path.exists(ficheiro):   # Ficheiro existe
        file = open(ficheiro, "r", encoding="utf-8")
        lista = file.readlines()
        file.close()    
    return lista

def isAdmin(user):
    """
    Arg:
        username|str

    Return:
        True|bol if the username given is an admin

    Used File Structure:
        user_db:
            Username;Password;Email;User/Admin;Last Login(optional)\n
    """
    userList=lerFicheiro(user_db)
    for username in userList:
        campos=username.split(";")
        if campos[0]==user and campos[3]=="Admin\n":return True
    return False

def seeUsers():
    """
    Arg:
        N/a

    Return:
        Users List|list

    List Line Structure:
        Username;Role(admin or not);Status(blocked or not)

    Used Files Structure:
        user_db:
            Username;Password;Email;User/Admin;Last Login(optional)\n
        ban_list:
            Username;Date\n <--if the user is banned
    """
    userList=lerFicheiro(user_db)
    banList=lerFicheiro(ban_list)
    user_list=[]
    for user in userList:
        campos=user.split(";")
        if campos[0] in banList:
            user_list.append(campos[0]+";"+campos[3]+";Blocked")
        else:
            user_list.append(campos[0]+";"+campos[3]+";Not Blocked")
    return user_list

def sortUsers(tree):
    """
    Ordena a tree criada pela função userTree() por ordem alfabética do campo User

    Args:
        tree|tk.Treeview
    
    Returns:
        None
    """
    data = [(tree.set(child, "User"), tree.item(child)["values"]) for child in tree.get_children("")]#leitura dos valores da tree

    data.sort(key=lambda x: x[0].lower())#ordenação dos valores (case INSENSITIVE)

    for child in tree.get_children():#limpar tree
        tree.delete(child)

    for user, values in data:#atualização da tree
        tree.insert("", "end", values=(user, *values[1:]))

def reverseSortUsers(tree):
    """
    Ordena a tree criada pela função userTree() por ordem alfabética inversa do campo User

    Args:
        tree|tk.Treeview
    
    Returns:
        None
    """
    data = [(tree.set(child, "User"), tree.item(child)["values"]) for child in tree.get_children("")]#leitura dos valores da tree

    data.sort(key=lambda x: x[0].lower(), reverse=True)#ordenação dos valores (case INSENSITIVE)

    for child in tree.get_children():#limpar tree
        tree.delete(child)

    for user, values in data:#atualização da tree
        tree.insert("", "end", values=(user, *values[1:]))

def searchUsers(user,tree):
    """
    Mostra na treeview o user procurado e os seus dados

    Args:
        user|str
        tree|tk.Treeview

    Returns:
        None
    """
    tree.delete(*tree.get_children())
    userList=lerFicheiro(user_db)
    for user in userList:
        campos=user.split(";")
        if campos[0]==user:
            tree.insert("", "end", text=campos[0], values=(campos[1], campos[2]))

def userTree(user_list):
    """
    Mostra os users returnados pela seeUsers() numa treeview

    Args:
        user_list|list

    return:
        None

    Format:
        Username;Role(admin or not);Status(blocked or not)
    """
    tree = tk.Treeview(frame,
                    columns=("User", "Role", "Status"),
                    show="headings")
    
    tree.column("User", width=160, anchor="center")
    tree.column("Role", width=160, anchor="center")
    tree.column("Status", width=160, anchor="center")

    tree.heading("User", text="Username")
    tree.heading("Role", text="Role")
    tree.heading("Status", text="Status")

    for user in user_list:
        campos = user.split(";")
        tree.insert("", "end", text=campos[0], values=(campos[1], campos[2]))

    tree.place()

def removeUsers(user):
    """
    Rewrites the file user_db without the username given

    Arg:
        Username(str)-username to remove

    Returns:
        None

    Used Files Structure:
        user_db:
            Username;Password;Email;User/Admin;Last Login(optional)\n
    """
    userList=lerFicheiro(user_db)
    newUserList=[]
    for username in userList:
        campos=username.split(";")
        if campos[0]!=user:
            newUserList.append(username)
    file= open(user_db,"w",encoding="utf-8")
    for line in newUserList:
        file.write(line)
    file.close()

def addAdmin(user):
    """
    Writes the file user_db with the username given as an admin

    Arg:
        Username(str)-username to promote

    Returns:
        None

    Used Files Structure:
        user_db:
            Username;Password;Email;User/Admin;Last Login(optional)\n
    """
    userList=lerFicheiro(user_db)
    newUserList=[]
    for username in userList:
        campos=username.split(";")
        if campos[0]!=user:
            newUserList.append(username)
        else:
            newAdmin=campos[0]+";"+campos[1]+";"+campos[2]+";Admin\n"
            newUserList.append(newAdmin)
    file= open(user_db,"w",encoding="utf-8")
    for line in newUserList:
        file.write(line)
    file.close()

def addCat(categoryName):
    """
    Writes the file category_db with the new category

    Arg:
        Category Name(str)-category to add

    Returns:
        None

    Used Files Structure:
        category_db:
            Name\n
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=[]
    for category in categoryList:
        newCategoryList.append(category)
    newCategoryList.append(categoryName+"\n")
    file= open(category_db,"w",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()

def removeCat(categoryName):
    """
    Rewrites the file category_db without the category given

    Arg:
        Category Name (str) - category to remove

    Returns:
        None

    Used Files Structure:
        category_db:
            Name\n
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=[]
    for category in categoryList:
        if category.strip()!=categoryName:
            newCategoryList.append(category)
    file= open(category_db,"w",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()

def blockUsers(user):
    """
    Blocks a user for a specified number of days.
    
    Args:
        user (str): The username to block.
    
    Returns:
        None: Updates the ban list file with the block information.
    """
    time=15
    instant = datetime.now().date()

    end_time = instant + datetime.timedelta(days=time)
    end_time_str = end_time.strftime("%d/%m/%y")

    new_list = lerFicheiro(ban_list)

    new_list.append(f"{user};{end_time_str}\n")

    with open(ban_list, "w", encoding="utf-8") as file:
        file.writelines(new_list)

def isBlocked(user):
    """
    Checks if the user is blocked and for how long.
    
    Reads a ban list from a file and checks if the given user is currently blocked.
    The ban list should have entries in the format: "username;dd/mm/yy".
    
    Args:
        user (str): The username to check.

    Returns:
        - False: If the user is not blocked or the block has expired.
        - str: A message with the remaining block duration if the user is still blocked.

    Used Files Structure:
        ban_list:
            username;dd/mm/yy
    """
    blocked_list = lerFicheiro(ban_list)
    for line in blocked_list:
        campos = line.split(";")
        if campos[0] == user:
            instant = datetime.now().date()
            expiry_date = datetime.strptime(campos[1], "%d/%m/%y").date()
            if instant <= expiry_date:
                remaining_days = (expiry_date - instant).days
                return f"Blocked for {remaining_days} more days."
            else:
                return False
    return False

def sendNotification(mensage):
    """
    Sends a notification to all users, to be displayed to all users, pushed by the admin.
    The notification writen with an id and the mensage given.
    The id propose is to be used as an method for each user to mark the notification as read without conflicting with others.
    Arg:
        mensage(str)-mensage to push
    Returns:
        None
    Notification Format = id;mensage

    """
    id="0"
    notificationList=lerFicheiro(global_notification)
    for line in notificationList:
        try:
            campos = line.split(";")
            id=str(int(campos[0])+1)
        except:continue
    file= open(global_notification,"a",encoding="utf-8")
    file.write(id+";"+mensage)
    file.close()

def auto_notification(user):
    """
    Sends an automatic mensage to all users, based on the date.
    It functions compares the last login date with the release dates of the catalog and pushes an notifications if there are new releases
    Args:
        User(str)-user currently log on
    Returns:

    Used Files Structure:
        user_db:
            Username;Password;Email;User/Admin;Last Login(optional)\n
        catalog_db:
            ID;Name;Category;Release Date;Author;Description\n
        user_data/{user}/notifications.txt
            id;mensage\n
    """
    userList=lerFicheiro(user_db)
    catalogList=lerFicheiro(catalog_db)
    userNotifications=f".\\files\\user_data\\{user}\\notifications.txt"
    if not os.path.exists(userNotifications):
        open(userNotifications,"w").close()
    userNotifications=lerFicheiro(userNotifications)
    for user in userList:
        campos=user.split(";")
        if campos[0]==user:
            lastLogin=campos[4]
            break
    for catalog in catalogList:
        campos=catalog.split(";")
        if campos[3]>lastLogin:
            newNotificationList=[]
            for notification in userNotifications:
                campos=notification.split(";")
                newNotificationList.append(campos[0])
            if campos[0] not in newNotificationList:
                file= open(userNotifications,"a",encoding="utf-8")
                file.write(campos[0]+";"+"New Release: "+campos[1])
                file.close()

def notificationRead(user,id):
    """
    Remove a notificação do para ler do utilizador

    Args:
        user (str): Username.
        id (str): ID da notificação.

    Returns:
        None

    Used Files Structure:
        .\\files\\user_data\\{user}\\notifications.txt
            id\n
    """
    notification_file = f".\\files\\user_data\\{user}\\notifications.txt"
    notificationList = lerFicheiro(notification_file)
    newNotificationList = []

    for line in notificationList:
        if line.strip() != id:
            newNotificationList.append(line)

    with open(notification_file, "w", encoding="utf-8") as file:
        for line in newNotificationList:
            file.write(line if line.endswith("\n") else (line + "\n"))

def passwordChecker(password):
    """
    Args:
        password (str): The password to check.

    Returns:
        str: A message with the requirements that the password does not meet.
        True(str): If the password meets all requirements.

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

def emailChecker(email):
    """
    Arg:
        email (str): The email to check.

    Returns:
        str: A message with the requirements that the email does not meet.
        True(str): If the email meets all requirements.

    Requisitos:
    - Email deve conter '@'
    - Não pode ter ';' (ponto e vírgula)
    """
    if ";" in email:
        return "-Email não pode conter ponto e vírgula (;)\n"
    if "@" not in email:
        return "-Email deve conter '@'\n"
    return "True"

def changeUser(user, password, newUser):
    """
    Altera o 'username' para 'newUser' (se a password for correta).
    Args:
        user (str): Username atual.
        password (str): Password atual.
        newUser (str): Novo username.
    Return:
        Mensage Box com a informação do sucesso ou insucesso da operação.
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

def changePass(user, oldPassword, newPassword):
    """
    Altera a password do 'user' (se oldPassword for correta).

    Args:
        user (str): Username.
        oldPassword (str): Password atual.
        newPassword (str): Nova password.

    Return:
        Mensage Box com a informação do sucesso ou insucesso da operação.
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

def changeMail(user, oldPassword, newMail):
    """
    Altera o email do 'user' (se a password for correta e o newMail for válido).

    Args:
        user (str): Username.
        oldPassword (str): Password atual.
        newMail (str): Novo email.

    Returns:
        Mensage Box com a informação do sucesso ou insucesso da operação.
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

def addFavorite(user, item):
    """
    Adiciona 'item' à lista de favoritos do 'user'.

    Args:
        user (str): Username.
        item (str): Item a adicionar.

    Returns:
        None

    Used Files Structure:
        user_data/{user}/favorites.txt:
            item\n
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

    Args:
        user (str): Username.
        item (str): Item a remover.

    Retruns:
        None

    Used Files Structure:
        user_data/{user}/favorites.txt:
            item\n
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

def addRating(user, item, rating):
    """
    Adiciona rating a 'item'.

    Args:
        user (str): Username.
        item (str): Item a adicionar rating.
        rating (str): Rating a adicionar(valor de 1 a 5).

    Returns:    
        None

    Used Files Structure:
        .\\files\\catalog_data\\{item}\\reviews.txt
            user;rating\n
    """            

    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.makedirs(f".\\files\\catalog_data\\{item}")

    reviews_file = f".\\files\\catalog_data\\{item}\\reviews.txt"
    if not os.path.isfile(reviews_file):
        open(reviews_file, 'w').close()

    with open(reviews_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{rating}\n")

def removeRating(user, item):
    """
    Remove rating a um 'item'.

    Args:
        user (str): Username.
        item (str): Item a remover rating.

    Returns:
        None

    Used Files Structure:
        .\\files\\catalog_data\\{item}\\reviews.txt
            user;rating\n    
    """
    reviews_file = f".\\files\\catalog_data\\{item}\\reviews.txt"

    reviewsList = lerFicheiro(reviews_file)
    newReviewsList = []

    for line in reviewsList:
        campos = line.split(";")
        if campos[0] != user:
            newReviewsList.append(line)

    # Reescreve o ficheiro de reviews
    with open(reviews_file, "w", encoding="utf-8") as file:
        for line in newReviewsList:
            file.write(line if line.endswith("\n") else (line + "\n"))

def addComment(user, item, comment):
    """
    Adiciona comentário a 'item'.

    Args:
        user (str): Username.
        item (str): Item a adicionar comentário.
        comment (str): Comentário a adicionar.

    Returns:
        None

    Used Files Structure:
        .\\files\\catalog_data\\{item}\\comments.txt
            user;comment\n
        .\\files\\user_data\\{user}\\comments.txt
            item;comment\n
    """
    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.makedirs(f".\\files\\catalog_data\\{item}")

    comments_file = f".\\files\\catalog_data\\{item}\\comments.txt"
    if not os.path.isfile(comments_file):
        open(comments_file, 'w').close()

    with open(comments_file, 'a', encoding="utf-8") as file:
        file.write(f"{user};{comment}\n")

    user_comments_file = f".\\files\\user_data\\{user}\\comments.txt"
    if not os.path.isfile(user_comments_file):
        open(user_comments_file, 'w').close()

    with open(user_comments_file, 'a', encoding="utf-8") as file:
        file.write(f"{item};{comment}\n")

def removeComment(user, item):
    """
    Remove comentário a um 'item'.

    Args:
        user (str): Username.
        item (str): Item a remover comentário.

    Returns:
        None

    Used Files Structure:
        .\\files\\catalog_data\\{item}\\comments.txt
            user;comment\n
        .\\files\\user_data\\{user}\\comments.txt
            item;comment\n
    """
    comments_file = f".\\files\\catalog_data\\{item}\\comments.txt"
    commentsList = lerFicheiro(comments_file)
    newCommentsList = []

    for line in commentsList:
        campos = line.split(";")
        if campos[0] != user:
            newCommentsList.append(line)

    with open(comments_file, "w", encoding="utf-8") as file:
        for line in newCommentsList:
            file.write(line if line.endswith("\n") else (line + "\n"))

    user_comments_file = f".\\files\\user_data\\{user}\\comments.txt"
    user_commentsList = lerFicheiro(user_comments_file)
    newUserCommentsList = []

    for line in user_commentsList:
        campos = line.split(";")
        if campos[0] != item:
            newUserCommentsList.append(line)

    with open(user_comments_file, "w", encoding="utf-8") as file:
        for line in newUserCommentsList:
            file.write(line if line.endswith("\n") else (line + "\n"))

def addLike(user, item, like):
    """
    Adiciona like a um 'item'.

    Args:
        user (str): Username.
        item (str): Item a adicionar like.
        like (str): Like a adicionar(1 ou -1).

    Returns:
        None

    Used Files Structure:
        .\\files\\user_data\\{user}\\likes.txt
            item;like\n
    """
    if not os.path.isdir(f".\\files\\user_data\\{user}"):
        os.makedirs(f".\\files\\user_data\\{user}")

    likes_file = f".\\files\\user_data\\{user}\\likes.txt"
    if not os.path.isfile(likes_file):
        open(likes_file, 'w').close()

    with open(likes_file, 'a', encoding="utf-8") as file:
        file.write(f"{item};{like}\n")

def removeLike(user, item):
    """
    Remove like a um 'item'.

    Arg:
        user (str): Username.
        item (str): Item a remover like.

    Returns:
        None

    Used Files Structure:
        .\\files\\user_data\\{user}\\likes.txt
            item;like\n
    """
    likes_file = f".\\files\\user_data\\{user}\\likes.txt"
    likesList = lerFicheiro(likes_file)
    newLikesList = []

    for line in likesList:
        campos = line.split(";")
        if campos[0] != item:
            newLikesList.append(line)

    # Reescreve o ficheiro de likes
    with open(likes_file, "w", encoding="utf-8") as file:
        for line in newLikesList:
            file.write(line if line.endswith("\n") else (line + "\n"))

def add_to_list(user, item, list_name):
    """
    Adiciona um item a uma lista do utilizador.

    Arg:
        user (str): Username.
        item (str): Item a adicionar à lista.
        list_name (str): Nome da lista.

    Retruns:
        None

    Used Files Structure:
        .\\files\\user_data\\{user}\\{list_name}.txt
            item\n
    """
    if not os.path.isdir(f".\\files\\user_data\\{user}"):
        os.makedirs(f".\\files\\user_data\\{user}")

    list_file = f".\\files\\user_data\\{user}\\{list_name}.txt"
    if not os.path.isfile(list_file):
        open(list_file, 'w').close()

    with open(list_file, 'a', encoding="utf-8") as file:
        file.write(item + "\n")

def remove_from_list(user, item, list_name):
    """
    Remove um item de uma lista do utilizador.

    Arg:
        user (str): Username.
        item (str): Item a remover da lista.
        list_name (str): Nome da lista.

    Returns:
        None    

    Used Files Structure:
        .\\files\\user_data\\{user}\\{list_name}.txt
            item\n
    """
    list_file = f".\\files\\user_data\\{user}\\{list_name}.txt"
    listList = lerFicheiro(list_file)
    newListList = []

    for line in listList:
        if line.strip() != item:
            newListList.append(line)

    with open(list_file, "w", encoding="utf-8") as file:
        for line in newListList:
            file.write(line if line.endswith("\n") else (line + "\n"))