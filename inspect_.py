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
        FileManager().getDocumentsInDirectory(self.baseData.get("path"),self.indexPaths,"")
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
        doc = self.baseData.get("data")
        for item in self.data[2]:
            if item == doc:
                return self.data[2][item]
        return 0

    def showResultTerm(self, result):
        if result == 0:
            print("")
            print("////////////////////////////////////")
            print("No se encontraron datos con respecto al término "+self.baseData.get("data"))
        else:
            print("")
            print("////////////////////////////////////")
            print("Resultados inspección del término "+self.baseData.get("data"))
            print("Número de documentos en los que aparece el término: "+ str(result['ni']))
            print("Frecuencia inversa del documento: "+ str(result['idfs']))
            for item in result['postings']:
                print("Documento #"+self.data[2][item]['ruta']+":")
                print("Frecuencia: "+ str(result[item]['postings']['freq']))
                print("Peso: "+ str(result[item]['postings']['peso']))
    
    def showResultDoc(self, result):
        if result == 0:
            print("")
            print("////////////////////////////////////")
            print("No se encontraron datos con respecto al documento "+result['ruta'])
        else:
            print("")
            print("////////////////////////////////////")
            print("Resultados inspección del documento "+self.baseData.get("data"))
            print("Id: "+ str(result.keys()))
            print("Longitud: "+ str(result['longuitud']))
            print("Norma: "+ str(result['norma']))