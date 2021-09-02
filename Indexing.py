import re

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

#Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
def deletePunctuation(text):
    return re.sub(r'\<(.*?)\>',' ',text)

text="<MEMBER>Seth Alves: <EMAIL>alves@helixcode.com</EMAIL></MEMBER>"
text2 = readFile("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/xml-es/apx-authors.xml")
print(deletePunctuation(text2))