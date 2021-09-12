from FileManager import FileManager

class Inspect:

    def __init__(self, path, type, data):
        self.baseData={
            'path': path,
            'type':type,
            'data': data
        }
        self.indexPaths= []
        self.data = []
       
    def startInspection(self):
        try:
            FileManager().getDocumentsInDirectory(self.baseData.get("path"),self.indexPaths,"")
        except:
            print("")
            print("Error con el archivo índice. Intente nuevamente.")
            print("")
            return
        self.readData()
        if self.baseData.get("type")=="ter":
            self.showResultTerm(self.selectData())
        elif self.baseData.get("type")=="doc":
            self.showResultDoc(self.selectDoc())
            
    def readData(self):
        for item in self.indexPaths:
            self.data += [FileManager.readDictionary(self.baseData.get("path")+"/"+item) ]

    def selectData(self):
        term = self.baseData.get("data")
        for item in self.data[1]:
            if item == term:
                return self.data[1][item]
        return 0
    
    def selectDoc(self):
        doc = self.baseData.get("data").replace("\\", "/")
        for item in self.data[2]:
            if self.data[2][item]['ruta'] == doc:
                self.data[2][item]['id']=item
                return self.data[2][item]
        return 0

    def showResultTerm(self, result):
        if result == 0:
            print("")
            print("No se encontraron datos con respecto al término "+self.baseData.get("data"))
            print("")
        else:
            print("")
            print("Resultados inspección del término "+self.baseData.get("data"))
            print("Número de documentos en los que aparece el término: "+ str(result['ni']))
            print("Frecuencia inversa del documento: "+ str(result['idfs']))
            print("Frecuencia inversa del documento 2: "+ str(result['idfs2']))
            for item in result['postings']:
                print("-Documento "+self.data[2][item]['ruta']+":")
                print("Frecuencia: "+ str(result['postings'][item]['freq']))
                print("Peso: "+ str(result['postings'][item]['peso']))
            print("")
    
    def showResultDoc(self, result):
        if result == 0:
            print("")
            print("No se encontraron datos con respecto al documento "+self.baseData.get("data"))
            print("")
        else:
            print("")
            print("Resultados inspección del documento "+self.baseData.get("data"))
            print("Id: "+ str(result['id']))
            print("Longitud: "+ str(result['longuitud']))
            print("Norma: "+ str(result['norma']))
            print("")