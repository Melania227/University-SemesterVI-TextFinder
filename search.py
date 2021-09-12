import re
from FileManager import FileManager

class Search:

    def __init__(self, indexPath, type, data, numDocs, query):
        self.baseData={
            'indexPath': indexPath,
            'type': type,
            'data': data,
            'numDocs': numDocs,
            'query': query
        }
        self.indexPaths= []
        print(self.processQuery())
    
    #Funcion principal para la busqueda vectorial
    def searchByVectorial(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("path"),self.indexPaths,"")
        self.baseData['query'] = self.processQuery()
        

    #Funcion principal para la busqueda con BM25
    def searchByBM25(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("path"),self.indexPaths,"")
        self.readData()

    def readData(self):
        for item in self.indexPaths:
            print(FileManager.readDictionary(self.baseData.get("path")+"/"+item))
        

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
        return wordList