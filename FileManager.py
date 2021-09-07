import os

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




    