import re

#Funcion que elimina los signos de puntuacion del texto y los cambia por un espacio en blanco
def deletePunctuation(text):
    return re.sub(r'\<(.*?)\>',' ',text)

text="<MEMBER>Seth Alves: <EMAIL>alves@helixcode.com</EMAIL></MEMBER>"
print(deletePunctuation(text))