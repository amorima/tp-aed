#Ficheiro .py de gestão e funções admin
#Biblioteca
#-----------
import os
#Files
#-----------------------------------
user_db=".\\files\\users.txt"

#Funções
#-----------------------------------------------------
def lerFicheiro(ficheiro):
    lista = []
    if os.path.exists(ficheiro):   # Ficheiro existe
        file = open(ficheiro, "r", encoding="utf-8")
        lista = file.readlines()
        file.close()    
    return lista

def isAdmin(user):
    """
    Arg-username|str
    Return-True(bol) if username given is an admin 
    """
    userList=lerFicheiro(user_db)
    for username in userList:
        campos=username.split(";")
        if campos[0]==user and campos[3]=="Admin\n":return True
    return False

def seeUsers():
    """
    Arg-N/a
    Return-Username List
    """
    userList=lerFicheiro(user_db)
    displayList=[]
    for username in userList:
        if username=="Username;Password;Email;User/Admin\n":continue
        campos=username.split(";")
        displayList.append(campos[0])
    return displayList

def removeUsers(user):
    """
    Arg-username|str
    Returns-rewrites the file utilizadores.txt without the username given
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
    Arg-username|str
    Returns-Changes the tag "User" to "Admin" of the given username in the file utilizadores.txt
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