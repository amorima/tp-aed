#Ficheiro .py de gestão e funções admin
#Biblioteca
#-----------
import os
import datetime
#Files
#-----------------------------------
user_db=".\\files\\user.txt"
category_db=".\\files\\categories.txt"
catalog_db=".\\files\\catalog.txt"
ban_list=".\\files\\ban_list.txt"

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

def addCat(categoryName):
    """
    Arg-Category Name|str
    Returns-Add the Category name to the categorias.txt file
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=[]
    for category in categoryList:
        campos=category.split(";")
        main=campos[0][0:2]
    try:
        int(main)
    except:
        main="00"
        newCategoryList.append(main+";"+categoryName+"\n")
    else:
        if len(str(int(main)))==2 and main!="09":
            newCategoryList.append(str(int(main)+1)+";"+categoryName+"\n")
        elif main=="09":
            newCategoryList.append(str(int(main)+1)+";"+categoryName+"\n")
        else:
            newCategoryList.append("0"+str(int(main)+1)+";"+categoryName+"\n")
    file= open(category_db,"a",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()

def removeCat(categoryName):
    """
    Arg-Category Name|str
    Returns-Removes the Category (as well as all the sub-categories associated) from the categorias.txt
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=["Main(XX).Sub(.XX);Name\n"]
    categoryToDelete="N/a"
    for line in categoryList:
        campos=line.split(";")
        if campos[1]==categoryName+"\n":
            categoryToDelete=campos[0]
        try:
            if campos[0][0:2]!=categoryToDelete and int(campos[0][0:2])<int(categoryToDelete):
                newCategoryList.append(line)
            elif campos[0][0:2]!=categoryToDelete:
                if len(str(int(campos[0][0:2])))==1 or campos[0][0:2]=="10":
                    try:
                        sub=campos[0][2:5]
                    except:
                        sub=""
                    newCategoryList.append("0"+str(int(campos[0][0:2])-1)+sub+";"+campos[1])
                else:
                    try:
                        sub=campos[0][2:5]
                    except:
                        sub=""
                    newCategoryList.append(str(int(campos[0][0:2])-1)+sub+";"+campos[1])
        except:continue
    file= open(category_db,"w",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()
    
def addSubCat(mainCategory,subCategory):
    """
    Arg-mainCategory|str, subCategory|str
    Returns-Adds the sub-category to the main category given in the categorias.txt file
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=[]
    sub=".00"
    main="N/a"
    for categoryLine in categoryList:
        campos=categoryLine.split(";")
        if campos[1]==mainCategory+"\n":
            main=campos[0]
            mainAdd=categoryLine
        if campos[0][0:3]==main+".":
            lastSub=campos[0][3:5]
            fullLine=categoryLine
            if len(str(int(lastSub)))==2:
                sub="."+str(int(lastSub)+1)
            elif lastSub=="09":
                sub=".10"
            else:
                sub=".0"+str(int(lastSub)+1)
        newCategoryList.append(categoryLine)#index
    try:
        indexAdd=newCategoryList.index(fullLine)+1
    except:
        indexAdd=newCategoryList.index(mainAdd)+1
    newCategoryList.insert(indexAdd,main+sub+";"+subCategory+"\n")
    file= open(category_db,"w",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()

def removeSubCat(mainCategory,subCategory):
    """
    Arg-mainCategory|str, subCategory|str
    Returns-Removes the sub-category to the main category given in the categorias.txt file
    """
    categoryList=lerFicheiro(category_db)
    newCategoryList=[]
    mainCode=subCode="100"
    for line in categoryList:
        campos=line.split(";")
        codes=campos[0].split(".")
        if campos[1]==mainCategory+"\n":
            mainCode=codes[0]
        if campos[1]==subCategory+"\n":
            subCode=codes[1]
        if codes[0]!=mainCode:
            newCategoryList.append(line)
        elif campos[0][0:3]==codes[0]+".":
            if int(codes[1])<int(subCode):
                newCategoryList.append(line)
            elif int(codes[1])>int(subCode):
                if len(str(int(codes[1])))==2  and codes[1]!="10":
                    newCategoryList.append(codes[0]+"."+str(int(codes[1])-1)+";"+campos[1])
                else:
                    newCategoryList.append(codes[0]+".0"+str(int(codes[1])-1)+";"+campos[1])
        else:
            newCategoryList.append(line)
    file= open(category_db,"w",encoding="utf-8")
    for line in newCategoryList:
        file.write(line)
    file.close()

def blockUsers(user):
    """
    Blocks a user for a specified number of days.
    
    Args:
        user (str): The username to block.
        time (int): The duration of the block in days.
    
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
    Arg-mensage|str
    Notification Format = id;mensage
    Returns-
    """
    id="0"
    notificationList=lerFicheiro(".\\files\\notifications.txt")
    for line in notificationList:
        try:
            campos = line.split(";")
            id=str(int(campos[0])+1)
        except:continue
    file= open(".\\files\\notifications.txt","a",encoding="utf-8")
    file.write(id+";"+mensage)
    file.close()
    
