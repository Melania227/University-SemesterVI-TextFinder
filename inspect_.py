from FileManager import FileManager

class Inspect:

    def __init__(self, path, type, data):
        self.baseData={
            'path': path,
            'type':type,
            'data': data
        }
        self.indexPaths= []
    
    def startInspection(self):
        FileManager().getDocumentsInDirectory(self.baseData.get("path"),self.indexPaths,"")
        self.readData()
        
        #if self.baseData.get("type")=="doc":
        #else:

    def readData(self):
        for item in self.indexPaths:
            print(FileManager.readDictionary(self.baseData.get("path")+"/"+item))
        