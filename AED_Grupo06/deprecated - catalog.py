#Ficheiro .py de gestão de entidade de aplicação
#Bibliotecas
#-----------
import os
#Files
#-----------------------------------
user_db=".\\files\\user.txt"
category_db=".\\files\\categories.txt"
catalog_db=".\\files\\catalog.txt"

def lerFicheiro(ficheiro):
    lista = []
    if os.path.exists(ficheiro):
        file = open(ficheiro, "r", encoding="utf-8")
        lista = file.readlines()
        file.close()    
    return lista

def codeToName(code):
    """
    Procura o codigo inserido e devolve o nome da categoria inserida
    Code|str :
        XX.XX   ,se for completo
        XX      ,se for apenas categoria principal
    """
    category=lerFicheiro(category_db)
    for line in category:
        if len(code)==5:#full
            campos=line.split(";")
            if campos[0]==code:
                return campos[1]
        if len(code)==2:#main
            campos=line.split(";")
            if campos[0][0:2]==code:
                return campos[1]

def nameToCodeFull(name):
    """
    Procura o nome inserido e devolve o codigo da categoria especifico inserido
    """
    category=lerFicheiro(category_db)
    for line in category:
        campo=line.split(";")
        if campo[1]==name+"\n":
            return campo[0]

def nameToCodeMain(name):
    """
    Procura o nome inserido e devolve o codigo da categoria principal inserido
    """
    category=lerFicheiro(category_db)
    for line in category:
        campo=line.split(";")
        if campo[1]==name+"\n":
            return campo[0][0:2]

def addToCatalog(name,categoriesList):
    """
    Arg-Series/Movie name|str ,categories codes|list
    returns-add series to catalog.txt
    """
    categoryCode=[]
    for category in categoriesList:
        categoryCode.append(nameToCodeFull(category))
    file=open(catalog_db,"a",encoding="UTF-8")
    file.write(name+";")
    for i in range(len(categoryCode)):
        if i<len(categoryCode)-1:
            file.write(categoryCode[i]+"|")
        else:
            file.write(categoryCode[i])
    file.write("\n")

def removeFromCatalog(name):
    """
    Arg-Series/Movie name|str
    return-removes series from catalgo.txt
    """
    catalogList=lerFicheiro(catalog_db)
    newCatalog=[]
    for line in catalogList:
        campos=line.split(";")
        if campos[0]!=name:
            newCatalog.append(line)
    file= open(catalog_db,"w",encoding="utf-8")
    for line in newCatalog:
        file.write(line)
    file.close()
