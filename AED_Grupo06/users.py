#Gestão de users
#Bibliotecas
#-------------------
import os
import CTkMessagebox
#Files
#-----------------------------------
#user_db=".\\AED_Grupo06\\files\\users.txt"
#user_data=.\\files\\user_data\\...
user_db=".\\files\\users.txt"
#Funções de Gestão de Users
#--------------
def lerFicheiro(ficheiro):
    lista = []
    if os.path.exists(ficheiro):   # Ficheiro existe
        file = open(ficheiro, "r", encoding="utf-8")
        lista = file.readlines()
        file.close()    
    return lista

def passwordChecker(password):
    """
    Password must have at least:
    -Eight characthers long
    -One capital letter
    -Use at least one number
    -Use at least one special caracther
    Return if the password matches every requirement(True or ErrorMsm)
    """
    minLenght = capitalUsed = numberUsed = specialUsed = splitterUsed = False
    #Lenght Checker
    #----------------------
    if len(password) >= 8:
        minLenght = True
    for letter in password:
        #Capital Checker
        #--------------------
        if letter.isupper():
            capitalUsed = True
        #Number Checker
        #-----------------------
        if letter.isdigit():
            numberUsed = True
        # Check for special characters
        if not letter.isalnum():
            specialUsed = True
        if letter==";":
            splitterUsed=True 
    shortMsm=capitalMsm=numberMsm=specialMsm=splitterMsm=""
    if minLenght and capitalUsed and numberUsed and specialUsed and splitterUsed==False: 
        return "True"
    if not minLenght:
        shortMsm="-Deve conter pelo menos 8 caracteres\n"
    if not capitalUsed:
        capitalMsm="-Deve conter pelo menos uma maisuscula\n"
    if not numberUsed:
        numberMsm="-Deve conter pelo menos um numero\n"
    if not specialUsed:
        specialMsm="-Deve conter pelo menus um caracter especial\n"
    if splitterUsed:
        splitterMsm="-Caracter ; não é valido\n"
    Msm=shortMsm+capitalMsm+numberMsm+specialMsm+splitterMsm
    return Msm

def logIn(password,mail,next,next2):
    """
    next-proxima ação a fazer
    A função recebe a procura o username na lista
    Email&Pass Corret-Entra na aplicação
    Email Corret-Aviso de password errado

    Formato do ficheiro user_db
        Username;Password;Email;Admin/User
    O ultimo campo é preenchido como User como default 
    """
    userList=lerFicheiro(user_db)
    userExists=False
    for userLine in userList:
        campos = userLine.split(";")
        if mail == campos[2] and password == campos[1]:
            next2()
            next()
            return
        elif mail==campos[2]:
            CTkMessagebox.CTkMessagebox(title="LogIn", message="Password Incorreta",icon="warning", option_1="Ok") #Pop up Password
            return
    if userExists==False:
        CTkMessagebox.CTkMessagebox(title="LogIn", message="User não existe \nPor favor faça criar conta",icon="warning", option_1="Ok") #Pop up Sign In

def sign(user,password,mail,next):
    """
    A função recebe e procura o user na lista
    UserNotFound & PasswordValida - Aceita logIn
    UserNotFound - Pede Password
    UserFound - Pede Log in

    Formato do ficheiro user_db
        Username;Password;Admin/User
    O ultimo campo é preenchido como User como default 
    """
    validPassword = passwordChecker(password)
    validMail = emailChecker(mail)
    validUser = True
    for letter in user:
        if letter ==";":
            validUser=False
    if len(user) >= 4:
        if validPassword == "True":
            if validMail == "True":
                if validUser == True:
                    userExist = False
                    userList = lerFicheiro(user_db)
                    for userLine in userList:
                        campo = userLine.split(";")
                        if campo[0] == user:
                            userExist = True
                            CTkMessagebox.CTkMessagebox(
                                title="Sign in", 
                                message="Usuario já Existe", 
                                icon="warning", 
                                option_1="Ok"
                            )
                            return  # Não continua com a criação do usuário
                    for userLine in userList:
                        campo = userLine.split(";")
                        if campo[2] == mail:
                            userExist = True    
                            CTkMessagebox.CTkMessagebox(
                                title="Sign in", 
                                message="Email já Registado", 
                                icon="warning", 
                                option_1="Ok"
                            )
                    if not userExist:
                        with open(user_db, "a", encoding="utf-8") as f:
                            f.write(f"{user};{password};{mail};User\n")
                        next()  # Chama a próxima função apenas quando o cadastro for bem-sucedido
                else:
                    CTkMessagebox.CTkMessagebox(
                    title="Sign in", 
                    message="User Invalido", 
                    icon="warning", 
                    option_1="Ok"
                )
            else:
                CTkMessagebox.CTkMessagebox(
                    title="Sign in", 
                    message="Email invalid\n"+validMail, 
                    icon="warning", 
                    option_1="Ok"
                )
        else:
            CTkMessagebox.CTkMessagebox(
                title="Sign in", 
                message="The password is:\n" + validPassword, 
                icon="warning", 
                option_1="Ok"
            )
    else:
        CTkMessagebox.CTkMessagebox(
            title="Sign in", 
            message="Username deve ter no minimo 4 caratheres", 
            icon="warning", 
            option_1="Ok"
        )

def emailChecker(email):
    """
    @ checker
    """
    valid = "-Email deve conter um @\n"
    for letter in email:
        if letter == "@" :
            valid = "True"
    for letter in email:
        if letter ==";" :
            valid = ""
    return valid

def changeUser(user,password,newUser):
    """
    Arg-user|str,newUser|str
    Returns-changes the user to the newUser on the utilizadores.txt (if the login is valid)
    """
    newUser_db=[]
    if len(newUser)>=4:
        userList=lerFicheiro(user_db)
        for line in userList:
            username = line.split(";")
            if username[0] == user and username[1] == password:
                newUser_db.append(newUser+";"+username[1]+";"+username[2]+";"+username[3])
            elif username[0] == user:
                CTkMessagebox.CTkMessagebox(title="Username Change", message="Password Incorreta",icon="warning", option_1="Ok")
                newUser_db.append(line)
            else:
                newUser_db.append(line)
        file= open(user_db,"w",encoding="utf-8")
        for line in newUser_db:
            file.write(line)
        file.close()

def changePass(user,password,newPassword):
    """
    Arg-user|str,password|str
    Returns-changes the user's password to the newPassword on the utilizadores.txt (if the login is valid)
    """
    newUser_db=[]
    validPassword=passwordChecker(newPassword)
    if validPassword=="True":
        userList=lerFicheiro(user_db)
        for line in userList:
            campos = line.split(";")
            if campos[0] == user and campos[1] == password:
                newUser_db.append(campos[0]+";"+newPassword+";"+campos[2]+";"+campos[3])
            elif campos[0] == user:
                CTkMessagebox.CTkMessagebox(title="Username Change", message="Password Incorreta",icon="warning", option_1="Ok")
                newUser_db.append(line)
            else:
                newUser_db.append(line)
        file= open(user_db,"w",encoding="utf-8")
        for line in newUser_db:
            file.write(line)
        file.close()
    else:
        CTkMessagebox.CTkMessagebox(
                title="Sign in", 
                message="The password is:\n" + validPassword, 
                icon="warning", 
                option_1="Ok"
            )

def changeMail(user,password,newMail):
    """
    Arg-user|str,newMail|str
    Returns-changes the user's email to the newMail on the utilizadores.txt (if the login is valid)
    """
    newUser_db=[]
    validMail=emailChecker(newMail)
    if validMail=="True":
        userList=lerFicheiro(user_db)
        for line in userList:
            campos = line.split(";")
            if campos[0] == user and campos[1] == password:
                newUser_db.append(campos[0]+";"+campos[1]+";"+newMail+";"+campos[3])
            elif campos[0] == user:
                CTkMessagebox.CTkMessagebox(title="Username Change", message="Password Incorreta",icon="warning", option_1="Ok")
                newUser_db.append(line)
            else:
                newUser_db.append(line)
        file= open(user_db,"w",encoding="utf-8")
        for line in newUser_db:
            file.write(line)
        file.close()
    else:
        CTkMessagebox.CTkMessagebox(
                title="Sign in", 
                message="The password is:\n" + validMail, 
                icon="warning", 
                option_1="Ok"
            )

def addFavorite(user,item):
    """
    Arg-user|str , Serie/Movie name|str
    Returms-Adds item to the Favorite list of the user
    """
    userList=lerFicheiro(user_db)
    for line in userList:
        campos = line.split(";")
        if campos[0]==user:
            if not os.path.isdir(f".\\files\\user_data\\{user}"):
                os.mkdir(f".\\files\\user_data\\{user}")
            if not os.path.isfile(f".\\files\\user_data\\{user}\\favorites.txt"):
                open(f".\\files\\user_data\\{user}\\favorites.txt", 'w').close()
            with open(f".\\files\\user_data\\{user}\\favorites.txt", 'a',encoding="utf-8") as file:
                file.write(item+"\n")

def removeFavorite(user,item):
    """
    Arg-user|str , Serie/Movie name|str
    Returms-Removes item from the Favorite list of the user (favorites.txt)
    """
    favoritesList=lerFicheiro(f".\\files\\user_data\\{user}\\favorites.txt")
    newFavoritesList=[]
    for line in favoritesList:
        if line != item+"\n":
            newFavoritesList.append(line)
    file= open(user_db,"w",encoding="utf-8")
    for line in newFavoritesList:
        file.write(line)
    file.close()

def addRating(user,item,rating):
    """
    Arg-user|str , Serie/Movie name|str ,rating|int(0-5)
    Returns-Adds ratting to. . .
    """
    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.mkdir(f".\\files\\catalog_data\\{item}")
    if not os.path.isfile(f".\\files\\catalog_data\\{item}\\reviews.txt"):
        open(f".\\files\\catalog_data\\{user}\\reviews.txt", 'w').close()
    with open(f".\\files\\catalog_data\\{item}\\reviews.txt", 'a',encoding="utf-8") as file:
        file.write(user+";"+rating+"\n")

def addComment(user,item,comment):
    """
    Arg-user|str , Series/Movie name|str ,comment|str
    Returns-Adds comment to . . .
    """
    #checks (and creates) for series folder
    if not os.path.isdir(f".\\files\\catalog_data\\{item}"):
        os.mkdir(f".\\files\\catalog_data\\{item}")
    #checks (and creates) for series coments file
    if not os.path.isfile(f".\\files\\catalog_data\\{item}\\comments.txt"):
        open(f".\\files\\catalog_data\\{user}\\comments.txt", 'w').close()
    with open(f".\\files\\catalog_data\\{item}\\comments.txt", 'a',encoding="utf-8") as file:
        file.write(user+";"+comment+"\n")

def addLike(user,item,like):
    """
    Arg-user|str , Series/Movie name|str , like|int(-2 to 2 with 0 as the default)
    Returns-Adds likes to . . .
    """
    if not os.path.exists(f".\\files\\user_data\\{user}"):
        os.makedirs(f".\\files\\user_data\\{user}")
    if not os.path.exists(f".\\files\\user_data\\{user}\\likes.txt"):
        open(f".\\files\\user_data\\{user}\\likes.txt", 'w').close()
    with open(f".\\files\\user_data\\{user}\\likes.txt", 'a',encoding="utf-8") as file:
        file.write(item+";"+like+"\n")

def notificationRead(id):
    """
    Marks the notification as read
    """
    #help

#tester
user=input("user:")
item=input("series:")
like="5"
addLike(user,item,like)