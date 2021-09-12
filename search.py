from collections import Counter
import re
from FileManager import FileManager
import bisect
from math import log, sqrt
from datetime import datetime

class Search:

    def __init__(self, indexPath, type, prefix, numDocs, query):
        self.baseData={
            'indexPath': indexPath,
            'type': type,
            'prefix': prefix,
            'numDocs': numDocs,
            'query': query,
            'literalTextOfQuery': query
        }

        self.dateTime = datetime.now()

        self.dictionary = {}
        self.collectionInfo = {}
        self.documentsInfo = {}

        self.indexPaths = []
        self.docScale = [] #Lista de tuples (sim,docID)
        
        '''print(self.processQuery())'''
    
    #Funcion principal
    def searching(self):
        try:
            FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        except:
            print("")
            print("Error con el directorio índice. Intente nuevamente.")
            print("")
            return
        self.baseData['query'] = self.processQuery()
        self.dictionary = FileManager.readDictionary(self.baseData['indexPath']+'/Dictionary Terms.txt')
        self.collectionInfo = FileManager.readDictionary(self.baseData['indexPath']+'/Collection Information.txt')
        self.documentsInfo = FileManager.readDictionary(self.baseData['indexPath']+'/Documents Information.txt')
        
        if (self.baseData['type']=="vec"):
            self.searchByVectorial()
            self.generateFile()
            self.generateHTML()
        else:
            self.searchByBM25()
            self.generateFile()
            self.generateHTML()
        print("")
        print("Busqueda completada.") 
        print("")

    #Funcion principal para la busqueda vectorial
    def searchByVectorial(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        #Vamos a ir documento por documento: del 1 al número que nos dieron como entrada
        keys = list(self.documentsInfo.keys())
        queryNorm = self.getQueryNorm()
        for key in keys:
            sumProdWeights = 0 
            isInDictionary=False
            for word in self.baseData['query']:
                if word in self.dictionary:
                    if key in self.dictionary[word]['postings']:
                        isInDictionary=True
                        frequencyInCons = self.baseData['query'][word]
                        ni = self.dictionary[word]['ni']
                        weightQueryWord = log((1+frequencyInCons),2) * log((self.collectionInfo['N']/ni),2)
                        weightQueryInDoc = self.dictionary[word]['postings'][key]['peso']
                        sumProdWeights += weightQueryWord*weightQueryInDoc

            if(isInDictionary):
                '''print("PARA EL DOC " + str(key))
                print("SUMA PRODUCTO " + str(sumProdWeights))
                print("NORMA DEL DOC " + str(self.documentsInfo[key]['norma']))
                print("NORMA DE LA CONSULTA " + str(queryNorm))'''
                simTempDoc = (sumProdWeights/(queryNorm*self.documentsInfo[key]['norma']))
                bisect.insort(self.docScale,(simTempDoc, key))
            else:
                bisect.insort(self.docScale,(0, key))
        '''print(self.docScale)'''
        self.docScale = list(reversed(self.docScale))





    #Funcion principal para la busqueda con BM25
    def searchByBM25(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("indexPath"),self.indexPaths,"")
        #Vamos a ir documento por documento: del 1 al número que nos dieron como entrada
        keys = list(self.documentsInfo.keys())
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

            bisect.insort(self.docScale,(simTempDoc, key))
        '''print(self.docScale)'''
        self.docScale = list(reversed(self.docScale))
        

    #Funcion que genere el archivo de salida
    def generateFile(self):
        textForFile=""
        textForFile+="ESCALAFÓN:\n\tPosición\t|\tDocID\t|\tValor de Similitud\n"
        pos=1
        for sim in self.docScale:
            if(sim[0]>0):
                textForFile+="\t"+str(pos)+"\t\t\t\t"+str(sim[1])+"\t\t\t"+str(sim[0])+"\n"
                pos+=1
        '''print(textForFile)'''
        path=self.baseData.get("indexPath")+"/"+self.baseData['prefix']+".esca"
        FileManager.writeFile(path,textForFile)

    #Funcion que genere el HTML
    def generateHTML(self):
        textForFile=""
        dt_string = self.dateTime.strftime("%d/%m/%Y %H:%M:%S")
        prefix = self.baseData['prefix']
        textQuery = self.baseData['literalTextOfQuery']
        if len(self.docScale)<int(self.baseData['numDocs']):
            self.baseData['numDocs'] == len(self.docScale)
        docsScale = list(self.docScale)[:int(self.baseData['numDocs'])]

        textForFile+= f"""
<!DOCTYPE html>

    <html>
        <head>
            <title>{prefix}</title>
        </head>

        <body>
            <h1>Consulta: "{textQuery}"</h1>
            <h2>Momento de realización: {dt_string}</h2>

            <br>

            <h2>Documentos: </h2>
        </body>
    </html>
""" 
        cont = 1
        for doc in docsScale:
            simTemp = doc[0]
            docIDTemp = doc[1]

            docText = self.getTextFromDoc(docIDTemp)

            textForFile+= f"""
            <h3>ID: {docIDTemp} </h3>
            <h4>Posición en el escalafón: {cont} </h4>
            <h4>Similitud: {simTemp} </h4>
            <h4>Primeros 200 caracteres del texto del documento: </h4>
            <p>{docText}</p>
    """ 
            cont+=1

        path=self.baseData.get("indexPath")+"/"+prefix+".HTML"
        FileManager.writeFile(path,textForFile)


    #FUNCIONES SECUNDARIAS:

    #Funcion que trae las primeras 200 lineas de un texto
    def getTextFromDoc(self, docIDTemp):
        path = self.collectionInfo['ruta']
        path += "/" + self.documentsInfo[docIDTemp]['ruta']
        
        #Text Input
        text = FileManager.readFile(path)

        #Text format
        text = self.deleteTags(text)

        text = re.sub('\n',' ',text)

        return text[:200]

    #Funcion que saca la norma de la consulta
    def getQueryNorm(self):
        weightQueryForNorm = 0 
        for word in self.baseData['query']:
            if word in self.dictionary:
                frequencyInCons = self.baseData['query'][word]
                ni = self.dictionary[word]['ni']
                weightQueryWord = log((1+frequencyInCons),2) * log((self.collectionInfo['N']/ni),2)
                '''print("Peso de la consulta " + str(weightQueryWord))'''
                weightQueryForNorm += weightQueryWord**2
        weightQueryForNorm = sqrt(weightQueryForNorm)
        return weightQueryForNorm

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

    #Funcion que elimina los tags XML del texto y los cambia por un espacio en blanco
    def deleteTags(self, text):
        return re.sub('\<(.*?)\>',' ',text)

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