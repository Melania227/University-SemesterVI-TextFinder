import re
import os

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


text = readFile("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/xml-es/apx-authors.xml")
text = deleteTags(text)
text = deletePunctuation(text)
text = deleteSpecialCharacters(text)
text = deleteSpecialCharacters(text)
wordList = splitText(text)
print(wordList)

stopwordsList = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "e", "el", "en", "entre", "hacia", "hasta", "ni", "la", "le", "lo", "los", "las", "o", "para", "pero", "por", "que", "se", "segun", "sin", "so", "sobre", "tras", "u", "un", "una", "unas", "uno", "unos", "y"]

wordList = stopwords(stopwordsList,wordList)
print(wordList)
