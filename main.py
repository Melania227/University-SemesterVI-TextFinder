from collections import Counter
from collections import OrderedDict
from math import log, sqrt
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

documents={
}

collectionDictionary={
}

#Toma todos los paths de los documentos en una coleccion
def documentsInDirectory(ruta):
    return [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]


#Procesa archivo por archivo para crear el archivo invertido y el track de documentos
def processCollection(path):
    path="C:/Users/Laptop/OneDrive/Documentos/Sexto Semestre/RECUPERACION DE INFORMACION TEXTUAL/Pruebas"
    paths = documentsInDirectory(path)
    
    for p in paths:
        dictionary = dictionaryOfDocument(path+"/"+p)
        keysOfDictionary = sorted(dictionary.keys())
        frequencies = sumFrequencies(dictionary.values())
        

        #Update collection
        collectionAux = {
            'N':collection.get('N')+1,
            'avgLen':collection.get('avgLen')+frequencies,
            'ruta':path
        }
        collection.update(collectionAux)

        #Update documents
        documentData={
            'ruta':p,
            'longuitud':frequencies,
            'norma':"",
        }
        documents[collection.get('N')] = documentData

        #Update collection dictionary
        updateCollectionDictionary(dictionary, keysOfDictionary)
    
    collectionAux = {
        'N':collection.get('N'),
        'avgLen':collection.get('avgLen')/collection.get('N'),
        'ruta':path
    }

    collection.update(collectionAux)
    
    calculateWeight()
    
    #IDF    
    getIdf()

    #Norma
    updateDocuments()

    print (collection)
    print("///////////////////////////////////////////////////////////")
    print (documents)
    print("///////////////////////////////////////////////////////////")
    print(collectionDictionary)

def updateCollectionDictionary(dictionary, keys):
    for term in keys:
        if term in collectionDictionary:
            collectionDictionary[term]['ni'] += 1
            posting = createPosting(dictionary[term])
            collectionDictionary[term]['postings'].update({collection['N']:posting})
        else:
            termInCollectionDictionary={
                'ni':1,
                'idfs':0,
                'postings':{},
            }
            posting = createPosting(dictionary[term])
            termInCollectionDictionary['postings'][collection['N']] =  posting
            collectionDictionary[term]=termInCollectionDictionary
    

def createPosting(term):
    postingAux={
        'd':collection['N'],
        'freq':term,
        'peso':0
    }
    return postingAux

def getIdf():
    N = collection['N']
    for term in collectionDictionary:
        ni = collectionDictionary[term]['ni']
        tempIdf = log((N-ni+0.5)/(ni+0.5),10)
        if tempIdf < 0:
          collectionDictionary[term]['idfs'] = 0
        else:
           collectionDictionary[term]['idfs'] = tempIdf

def updateDocuments():
    for i in range (1,collection.get('N')+1):
        pesosTemp = []
        for term in collectionDictionary.copy():
            if i in collectionDictionary[term]['postings']: 
                pesosTemp += [collectionDictionary[term]['postings'][i]['peso']]
        documents[i]['norma'] = calculateNorma(pesosTemp)
    
    
def calculateNorma(pesosTemp):
    sum = 0
    for peso in pesosTemp:
        sum += pow(peso,2)
    return sqrt(sum)

def calculateWeight():
    for term in collectionDictionary:
        ni = collectionDictionary[term]['ni']
        for post in collectionDictionary[term]['postings']:
            frequency = collectionDictionary[term]['postings'][post]['freq']
            collectionDictionary[term]['postings'][post]['peso'] = log((1+frequency),2)* log((collection['N']/ni),2)


#PROCESAMIENTO DEL DOCUMENTO

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
    return re.sub('\<(.*?)\>',' ',text)

#Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
def deletePunctuation(text):
    return re.sub('[\W]+',' ',text)

#Funcion que elimina los caracteres especiales, por ejemplo, las tildes
def deleteAccent(text):
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

#Funcion que toma todas las frecuencias y las suma
def sumFrequencies(list):
    result = 0
    for i in list: 
        result+=i
    return result

#Funcion principal
def dictionaryOfDocument(path):
    #Text Input
    #text = readFile(path)
    text = readFile(path)

    #Text format
    text = deleteTags(text)
    text = deletePunctuation(text)
    text = deleteAccent(text)

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

