from collections import Counter
import re
from FileManager import FileManager
import bisect
from math import log, sqrt

class Search:

    def __init__(self, indexPath, type, data, numDocs, query):
        self.baseData={
            'indexPath': indexPath,
            'type': type,
            'data': data,
            'numDocs': numDocs,
            'query': query
        }

        self.dictionary = {}
        self.collectionInfo = {}
        self.documentsInfo = {}

        self.indexPaths = []
        self.docScale = [] #Lista de tuples (sim,docID)

        self.query={} #Diccionario con pesos ¿se necesita?
        
        print(self.processQuery())
    
    #Funcion principal
    def searching(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        self.baseData['query'] = self.processQuery()
        self.dictionary = FileManager.readDictionary(self.baseData['indexPath']+'/Dictionary Terms.txt')
        self.collectionInfo = FileManager.readDictionary(self.baseData['indexPath']+'/Collection Information.txt')
        self.documentsInfo = FileManager.readDictionary(self.baseData['indexPath']+'/Documents Information.txt')
        
        if (self.baseData['type']=="vec"):
            self.searchByVectorial()
        else:
            self.searchByBM25()

    #Funcion principal para la busqueda vectorial
    def searchByVectorial(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        #Vamos a ir documento por documento: del 1 al número que nos dieron como entrada
        keys = list(self.documentsInfo.keys())[:int(self.baseData['numDocs'])]
        for key in keys:
            weightQueryForNorm=0
            sumProdWeights = 0 
            isInDictionary=False
            for word in self.baseData['query']:
                if word in self.dictionary:
                    if key in self.dictionary[word]['postings']:
                        isInDictionary=True
                        frequencyInCons = self.baseData['query'][word]
                        ni = self.dictionary[word]['ni']
                        weightQueryWord = log((1+frequencyInCons),2) * log((self.collectionInfo['N']/ni),2)
                        weightQueryForNorm += weightQueryWord**2
                        weightQueryInDoc = self.dictionary[word]['postings'][key]['peso']
                        sumProdWeights += weightQueryWord*weightQueryInDoc

            if(isInDictionary):
                queryNorm = sqrt(weightQueryForNorm)
                print("NORMA DE LA CONSULTA " + str(queryNorm))
                print("NORMA DEL DOC " + str(self.documentsInfo[key]['norma']))
                print("LO QUE DA 0 " + str(queryNorm*self.documentsInfo[key]['norma']))
                simTempDoc = (sumProdWeights/(queryNorm*self.documentsInfo[key]['norma']))
                bisect.insort(self.docScale,(simTempDoc, "d"+str(key)))
            else:
                bisect.insort(self.docScale,(0, "d"+str(key)))
        print(self.docScale)






    #Funcion principal para la busqueda con BM25
    def searchByBM25(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        #Vamos a ir documento por documento: del 1 al número que nos dieron como entrada
        keys = list(self.documentsInfo.keys())[:int(self.baseData['numDocs'])]
        k=1.2
        b=0.75
        for key in keys:
            documentSize = self.documentsInfo[key]['longuitud']
            avgCollection = self.collectionInfo['avgLen']
            #isInDictionary=False
            simTempDoc = 0
            for word in self.baseData['query']:
                if word in self.dictionary:
                    if key in self.dictionary[word]['postings']:
                        #isInDictionary=True
                        frequencyInDoc = self.dictionary[word]['postings'][key]['freq']
                        idf = self.dictionary[word]['idfs']
                        ni = self.dictionary[word]['ni']
                        simTempDoc += idf * ((frequencyInDoc*(k+1))/(frequencyInDoc+k*(1-b+b*(documentSize/avgCollection))))

            bisect.insort(self.docScale,(simTempDoc, "d"+str(key)))
        print(self.docScale)
        

    #FUNCIONES SECUNDARIAS:

    #Eliminar stopwords
    def deleteStopwords(self, stopwordsList, wordList):
        for stopWord in stopwordsList:
            while stopWord in wordList: wordList.remove(stopWord)
        return wordList   

     #Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
    def deletePunctuation(self, text):
        return re.sub('[\W]+',' ',text)

    #Funcion que elimina los caracteres especiales, por ejemplo, las tildes
    def deleteAccent(self, text):
        text=text.lower()
        mapTable = text.maketrans("áéíóúü", "aeiouu")
        text = text.translate(mapTable)
        return str(text)

    #Funcion que toma la lista de palabras y quita duplicados
    def wordsInTextList(self, wordList):
        return list(set(wordList))

    #Funcion que toma un texto y lo separa en palabras
    def splitText(self, text):
        return text.split()

    #Funcion que toma una lista de palabras y nos devuelve un diccionario que contiene cada palabra y la cantidad de veces que aparece
    def wordAppearances(self, list):
        return Counter(list)

    #Funcion que procesa la consulta y nos devuelve una lista con las palabras de la consulta
    def processQuery(self):
        #Text format
        text = self.baseData['query']
        text = self.deletePunctuation(text)
        text = self.deleteAccent(text)

        #Final format list
        wordList = self.splitText(text)

        stopwordsList = FileManager.readDictionary(self.baseData['indexPath']+'/Stopwords.txt')

        wordList = self.deleteStopwords(stopwordsList,wordList)

        wordList = self.wordsInTextList(wordList)
        wordList.sort()

        wordIndex = self.wordAppearances(wordList)
        return wordIndex