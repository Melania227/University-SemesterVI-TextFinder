import os
import pickle

class FileManager:

    #def __init__(self):

    
    #Funcion que abre y lee y retorna el texto de un archivo
    def readFile(path):
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
        file = open(path, "w")
        file.write(text)
        file.close()

    #Funcion que guarda un diccionario en un archivo
    def writeDictionary(path, name, dict):
        outfile = open(path+'/'+name, 'wb')
        pickle.dump(dict, outfile)
        outfile.close()

    #Funcion que lee un diccionario de un archivo
    def readDictionary(path):
        infile = open(path,'rb')
        new_dict = pickle.load(infile)
        infile.close()
        return new_dict




    