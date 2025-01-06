#Gestão de users
#Bibliotecas
#-------------------
import os
import CTkMessagebox
#Files
#-----------------------------------
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
    minLenght = capitalUsed = numberUsed = specialUsed = False
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
    shortMsm=capitalMsm=numberMsm=specialMsm=""
    if minLenght and capitalUsed and numberUsed and specialUsed: 
        return "True"
    if not minLenght:
        shortMsm="-Too short(8 caracther minimun)\n"
    if not capitalUsed:
        capitalMsm="-Should use at least one Capital Letter\n"
    if not numberUsed:
        numberMsm="-Should use at least one number\n"
    if not specialUsed:
        specialMsm="-Should use at least one Speacial Caracther\n"
    Msm=shortMsm+capitalMsm+numberMsm+specialMsm
    return Msm

def logIn(username,password,mail,tab):
    """
    A função recebe a procura o username na lista
    User&Pass Corret-Entra na aplicação
    User Corret-Aviso de password errado

    Formato do ficheiro user_db
        Username;Password;Email;Admin/User
    O ultimo campo é preenchido como User como default 
    """
    userExists=False
    userList=lerFicheiro(user_db)
    for userLine in userList:
        campos = userLine.split(";")
        if username == campos[0] and password == campos[1]:
            userExists=True
            tab.add("Home")
            tab.delete("Login/Sign In")
        elif username==campos[0]:
            userExists=True
            CTkMessagebox.CTkMessagebox(title="LogIn", message="Password Incorreta",icon="warning", option_1="Ok") #Pop up Password
    if userExists==False:
        CTkMessagebox.CTkMessagebox(title="LogIn", message="User não existe \nPor favor faça Sign In",icon="warning", option_1="Ok") #Pop up Sign In

def sign(user,password,mail):
    """
    A função recebe e procura o user na lista
    UserNotFound & PasswordValida - Aceita logIn
    UserNotFound - Pede Password
    UserFound - Pede Log in

    Formato do ficheiro user_db
        Username;Password;Admin/User
    O ultimo campo é preenchido como User como default 
    """
    validPassword=passwordChecker(password)
    if len(user)>=4:
        if validPassword=="True":
            userExist=False
            userList=lerFicheiro(user_db)
            for userLine in userList:
                campo= userLine.split(";")
                if campo[0]==user:
                    userExist=True
                    CTkMessagebox.CTkMessagebox(title="Sign in", message="Usuario já Existe",icon="warning", option_1="Ok")
            if userExist==False:
                f = open(user_db, "a", encoding="utf-8")
                f.write(user+";"+password+";"+mail+";User\n")
                f.close()
        else:
            CTkMessagebox.CTkMessagebox(title="Sign in", message="The password is:\n"+validPassword,icon="warning", option_1="Ok")
    else:
        CTkMessagebox.CTkMessagebox(title="Sign in", message="Username deve ter no minimo 4 caratheres",icon="warning", option_1="Ok")