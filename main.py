import shlex
from index import Index
from shlex import split
from inspect_ import Inspect
from search import Search
from FileManager import FileManager

#index = Index()
#index.processCollection("")

def menu():
    print("Tarea programada 1 --- Menú")
    print("1. Indización")
    print("2. Búsqueda")
    print("3. Inspección")
    print("4. Salir")
    option = input("Seleccione una opción: ")
    if option == "1":
        print("")
        print("")
        return indizacionMenu()
    elif option == "2":
        print("")
        print("")
        return busquedaMenu()
    elif option == "3":
        print("")
        print("")
        return inspeccionMenu()
    elif option == "4":
        print("Adiós :P")
        return
    else:
        print("Opción no valida")
        print("")
        print("")
        return menu()

def indizacionMenu():
    print("¡Bienvenido a la herramienta de Indización!")
    print("Para ejecutar esta herramienta es necesario invocar el siguiente comando:")
    print("indizar 'Colección' 'Stopwords' 'Índice'")
    print("Colección -> ruta del directorio raíz")
    print("Stopwords -> ruta del archivo que contiene la lista de palabras que se deben omitir")
    print("Índice  -> ruta del directorio en que se almacenará los archivos generados")
    print("Igualmente puedes ingresar 'Volver' para regresar al menú principal")
    command = input("Ingrese el comando: ")
    if command == "Volver":
        print("")
        return menu()
    parts = shlex.split(command)
    if validate(parts,1):
        Index().processCollection(parts[1], parts[3], parts[2])
        return menu()
    else:
        print("")
        print("Error en comando. Intente nuevamente.")
        print("")
        return indizacionMenu()

def busquedaMenu():
    print("¡Bienvenido a la herramienta de Búsqueda!")
    print("Para ejecutar esta herramienta es necesario invocar el siguiente comando:")
    print("buscar 'Índice' Tipo Prefijo NumDocs 'Consulta'")
    print("Índice -> ruta del directorio en que se contiene los archivos que componen el índice usado")
    print("Tipo -> búsqueda vectorial (vec) o BM25 (bm25)")
    print("Prefijo  -> prefijo usado con todos los archivos de salida producidos por este comando")
    print("NumDocs  -> cantidad de los primeros documentos del escalafón que serán mostrados en un archivo HTML")
    print("Consulta  -> texto de la consulta")
    print("Igualmente puedes ingresar 'Volver' para regresar al menú principal")
    command = input("Ingrese el comando: ")
    if command == "Volver":
        print("")
        return menu()
    parts = shlex.split(command)
    if validate(parts,2):
        Search(parts[1], parts[2], parts[3], parts[4], parts[5]).searching() 
        return menu()
    else:
        print("")
        print("Error en comando. Intente nuevamente.")
        print("")
        return busquedaMenu()
    

def inspeccionMenu():
    print("¡Bienvenido a la herramienta de Inspección!")
    print("Para ejecutar esta herramienta es necesario invocar el siguiente comando:")
    print("mostrar 'Índice' Tipo 'Dato'")
    print("Índice -> ruta del directorio en que se contiene los archivos que componen el índice usado")
    print("Tipo -> término (ter) o documento (doc)")
    print("Dato   -> ruta del archivo o el término que se quiere buscar")
    print("Igualmente puedes ingresar 'Volver' para regresar al menú principal")
    command = input("Ingrese el comando: ")
    if command == "Volver":
        print("")
        return menu()
    parts = shlex.split(command)
    if validate(parts,3):
        Inspect(parts[1],parts[2],parts[3]).startInspection()
        return menu()
    else:
        print("")
        print("Error en comando. Intente nuevamente.")
        print("")
        return inspeccionMenu()

def validate(cmd, type): 
    if type == 1:
        return True if (cmd[0] == "indizar" and len(cmd)==4) else False
    elif type == 2:
        validWords = ["vec","bm25"]
        return True if (cmd[0] == "buscar" and len(cmd)==6 and cmd[2] in validWords) else False 
    else:
        validWords = ["doc","ter"]
        return True if (cmd[0] == "mostrar" and len(cmd)==4 and cmd[2] in validWords) else False      

menu()