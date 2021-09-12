import os
import pickle

class FileManager:

    #def __init__(self):
    
    
    #Funcion que abre y lee y retorna el texto de un archivo
    def readFile(path):
        path = path.replace("\\", "/")
        try:
            with open(path, encoding='utf-8') as file:
                content=file.read()
                file.close()
        except:
            with open(path,"r") as file:
                content=file.read()
                file.close()
        return content

    
    #Funcion que coloca en un archivo toda la informacion que se le indique
    def writeFile(path, text):
        path = path.replace("\\", "/")
        file = open(path, "w")
        file.write(text)
        file.close()

    #Funcion que guarda un diccionario en un archivo
    def writeDictionary(path, name, dict):
        path = path.replace("\\", "/")
        outfile = open(path+'/'+name, 'wb')
        pickle.dump(dict, outfile)
        outfile.close()


    #Funcion que lee un diccionario de un archivo
    def readDictionary(path):
        path = path.replace("\\", "/")
        infile = open(path,'rb')
        new_dict = pickle.load(infile)
        infile.close()
        return new_dict


    def getDocumentsInDirectory(self,path,list_,path_):
        path = path.replace("\\", "/")
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                if path_=="":
                    list_+=[f]
                else:
                    list_+=[path_+"/"+f]
            elif os.path.isdir(os.path.join(path, f)):
                if path_=="":
                    self.getDocumentsInDirectory(os.path.join(path, f),list_, f)
                else:
                    self.getDocumentsInDirectory(os.path.join(path, f),list_, path_+"/"+f)
        return list_  

    