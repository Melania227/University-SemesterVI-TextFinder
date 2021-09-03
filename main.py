from collections import Counter
from collections import OrderedDict
import re
import os


def takePath():
    path = input("Indique el path donde se encuentra su archivo y el nombre del mismo: ")
    return path

#PROCESAMIENTO DE LA COLECCION
collection = {
    'N':0,
    'avgLen':0,
    'ruta':""
}

#Toma todos los paths de los documentos en una coleccion
def documentsInDirectory(ruta):
    return [ruta+"/"+f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]


#Procesa archivo por archivo para crear el archivo invertido y el track de documentos
def processCollection(ruta):
    rutas = documentsInDirectory("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/pruebas")
    for r in rutas:
        dictionary = dictionaryOfDocumet(path)
        keysOfDictionary = sorted(dictionary.keys())
        print (dictionary)
        print(dictionary.get(keysOfDictionary[0]))

#PROCESAMIENTO DEL DOCUMENTO
documents={
    'd1':{
        'ruta':"",
        'longuitud':"",
        'largo':"",
    }
}


#Funcion que abre y lee y retorna el texto de un archivo
def readFile(path):
    route, extension = os.path.splitext(path)
    if(extension==".xml" or extension==".XML"):    
        try:
            with open(path, encoding='utf-8') as file:
                content=file.read()
                file.close()
        except:
            with open(path,"r") as file:
                content=file.read()
                file.close()
        return content
    return ""

#Funcion que elimina los tags XML del texto y los cambia por un espacio en blanco
def deleteTags(text):
    return re.sub(r'\<(.*?)\>',' ',text)

#Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
def deletePunctuation(text):
    return re.sub(r'[\W]+',' ',text)

#Funcion que elimina los caracteres especiales, por ejemplo, las tildes
def deleteSpecialCharacters(text):
    text=text.lower()
    mapTable = text.maketrans("áéíóúü", "aeiouu")
    text = text.translate(mapTable)
    return str(text)

#Funcion que toma un texto y lo separa en palabras
def splitText(text):
    return text.split()

#Eliminar stopwords
def stopwords(stopwordsList, wordList):
    for stopWord in stopwordsList:
        while stopWord in wordList: wordList.remove(stopWord)
    return wordList   

#Funcion la lista de palabras y quita duplicados
def wordsInTextList(wordList):
	return list(set(wordList))

#Funcion que toma una lista de palabras y nos devuelve un diccionario que contiene cada palabra y la cantidad de veces que aparece
def wordAppearances(list):
    return Counter(list)


#Funcion principal
def dictionaryOfDocumet(path):
    #Text Input
    #text = readFile(path)
    text = readFile("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/xml-es/apx-authors.xml")

    #Text format
    text = deleteTags(text)
    text = deletePunctuation(text)
    text = deleteSpecialCharacters(text)
    text = deleteSpecialCharacters(text)

    #Final format list
    wordList = splitText(text)

    stopwordsList = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "e", "el", "en", "entre", "hacia", "hasta", "ni", "la", "le", "lo", "los", "las", "o", "para", "pero", "por", "que", "se", "segun", "sin", "so", "sobre", "tras", "u", "un", "una", "unas", "uno", "unos", "y"]
    wordList = stopwords(stopwordsList,wordList)

    #wordList = wordsInTextList(wordList)
    wordList.sort()

    wordIndex = wordAppearances(wordList)
    return wordIndex

path = takePath()
processCollection(path)