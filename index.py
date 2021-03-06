from collections import Counter
from collections import OrderedDict
from posixpath import splitext
from FileManager import FileManager
from math import log, sqrt
import re
import os


class Index:
    
    def __init__(self):
        self.documents={
        }
        
        self.collection = {
            'N':0,
            'avgLen':0,
            'ruta':""
        }

        self.collectionDictionary={
        }

        self.stopwordsList=[]


    #PROCESAMIENTO DE LA COLECCION

    #Procesa archivo por archivo para crear el archivo invertido y el track de documentos
    def processCollection(self, path, resultsPath, stopWordsPath):
        #path="C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/pruebas"
        try:
            paths = FileManager().getDocumentsInDirectory(path,[],"")
        except:
            print("")
            print("Error con el directorio Coleccíón. Intente nuevamente.")
            print("")
            return
        regex = re.compile(r'.*\.xml')
        paths = [ele for ele in paths if regex.match(ele)]
        for p in paths:
            dictionary = self.dictionaryOfDocument(path+"/"+p, stopWordsPath)
            keysOfDictionary = sorted(dictionary.keys())
            frequencies = self.sumFrequencies(dictionary.values())
            

            #Update collection
            collectionAux = {
                'N':self.collection.get('N')+1,
                'avgLen':self.collection.get('avgLen')+frequencies,
                'ruta':path
            }
            self.collection.update(collectionAux)

            #Update documents
            documentData={
                'ruta':p,
                'longuitud':frequencies,
                'norma':"",
            }
            self.documents[self.collection.get('N')] = documentData

            #Update collection dictionary
            self.updateCollectionDictionary(dictionary, keysOfDictionary)
        
        collectionAux = {
            'N':self.collection.get('N'),
            'avgLen':self.collection.get('avgLen')/self.collection.get('N'),
            'ruta':path
        }

        self.collection.update(collectionAux)
        
        self.calculateWeight()
        
        #IDF    
        self.getIdf()

        #Norma
        self.updateDocuments()

        self.generateIndexDocuments(resultsPath)

        '''print (self.collection)
        print("///////////////////////////////////////////////////////////")
        print (self.documents)
        print("///////////////////////////////////////////////////////////")
        print(self.collectionDictionary)'''
        print("")
        print("Indización completada.") 
        print("")

    def updateCollectionDictionary(self, dictionary, keys):
        for term in keys:
            if term in self.collectionDictionary:
                self.collectionDictionary[term]['ni'] += 1
                posting = self.createPosting(dictionary[term])
                self.collectionDictionary[term]['postings'].update({self.collection['N']:posting})
            else:
                termInCollectionDictionary={
                    'ni':1,
                    'idfs':0,
                    'postings':{},
                }
                posting = self.createPosting(dictionary[term])
                termInCollectionDictionary['postings'][self.collection['N']] =  posting
                self.collectionDictionary[term]=termInCollectionDictionary


    def createPosting(self, term):
        postingAux={
            'd':self.collection['N'],
            'freq':term,
            'peso':0
        }
        return postingAux

    def getIdf(self):
        N = self.collection['N']
        for term in self.collectionDictionary:
            ni = self.collectionDictionary[term]['ni']
            idf2 = log((N-ni+0.5)/(ni+0.5),2)
            tempIdf = log((N/ni),2)
            if tempIdf < 0:
                self.collectionDictionary[term]['idfs'] = 0
                self.collectionDictionary[term]['idfs2'] = 0
            else:
                self.collectionDictionary[term]['idfs'] = tempIdf
                self.collectionDictionary[term]['idfs2'] = idf2

    def updateDocuments(self):
        for i in range (1,self.collection.get('N')+1):
            pesosTemp = []
            for term in self.collectionDictionary.copy():
                if i in self.collectionDictionary[term]['postings']: 
                    pesosTemp += [self.collectionDictionary[term]['postings'][i]['peso']]
            self.documents[i]['norma'] = self.calculateNorma(pesosTemp)
        
        
    def calculateNorma(self,pesosTemp):
        sum = 0
        for peso in pesosTemp:
            sum += pow(peso,2)
        return sqrt(sum)

    def calculateWeight(self):
        for term in self.collectionDictionary:
            ni = self.collectionDictionary[term]['ni']
            for post in self.collectionDictionary[term]['postings']:
                frequency = self.collectionDictionary[term]['postings'][post]['freq']
                self.collectionDictionary[term]['postings'][post]['peso'] = log((1+frequency),2)* log((self.collection['N']/ni),2)

    #Funcion que genera el archivo final con el index
    def generateIndexDocuments(self, path):
        try:
            FileManager.writeDictionary(path, "Collection Information.txt", self.collection)
            FileManager.writeDictionary(path, "Documents Information.txt", self.documents)
            FileManager.writeDictionary(path, "Dictionary Terms.txt", self.collectionDictionary)
            FileManager.writeDictionary(path, "Stopwords.txt", self.stopwordsList)
        except:
            print("")
            print("Error con la ruta para los archivos generados. Intente nuevamente.")
            print("")
            return
            

    #PROCESAMIENTO DEL DOCUMENTO

    #Funcion que elimina los tags XML del texto y los cambia por un espacio en blanco
    def deleteTags(self, text):
        return re.sub('\<(.*?)\>',' ',text)

    #Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
    def deletePunctuation(self, text):
        return re.sub('[\W]+',' ',text)

    #Funcion que elimina los caracteres especiales, por ejemplo, las tildes
    def deleteAccent(self, text):
        text=text.lower()
        mapTable = text.maketrans("áéíóúü", "aeiouu")
        text = text.translate(mapTable)
        return str(text)

    #Funcion que toma un texto y lo separa en palabras
    def splitText(self, text):
        return text.split()

    #Eliminar stopwords
    def stopwords(self, stopwordsList, wordList):
        if stopwordsList is None:
            return wordList
        for stopWord in stopwordsList:
            while stopWord in wordList: wordList.remove(stopWord)
        return wordList   

    #Funcion la lista de palabras y quita duplicados
    def wordsInTextList(self, wordList):
        return list(set(wordList))

    #Funcion que toma una lista de palabras y nos devuelve un diccionario que contiene cada palabra y la cantidad de veces que aparece
    def wordAppearances(self, list):
        return Counter(list)

    #Funcion que toma todas las frecuencias y las suma
    def sumFrequencies(self, list):
        result = 0
        for i in list: 
            result+=i
        return result

    #Funcion que toma los stopwords de un archivo y los procesaa en una lista
    def getStopwords(self, path):
        text = FileManager.readFile(path)
        text = re.sub('\n+|\s+',',',text)
        text = text.split(",")
        return text

    #Funcion que hace el procesamiento de palabras (Termino, frecuencia)
    def dictionaryOfDocument(self, path, stopWordsPath):
        #Text Input
        try:
            text = FileManager.readFile(path)
        except:
            print("")
            print("Error con la lectura de un documento en la colección.")
            print("")
            return
        #Text format
        text = self.deleteTags(text)
        text = self.deletePunctuation(text)
        text = self.deleteAccent(text)

        #Final format list
        wordList = self.splitText(text)

        self.stopwordsList = self.getStopwords(stopWordsPath)

        wordList = self.stopwords(self.stopwordsList,wordList)

        '''wordList = self.wordsInTextList(wordList)'''
        #wordList.sort()

        wordIndex = self.wordAppearances(wordList)
        
        return wordIndex
