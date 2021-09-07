from index import Index
from FileManager import FileManager

index = Index()
index.processCollection("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/pruebas", "C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/resultados", "C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/pruebas/stopwords.txt")
print(FileManager.readDictionary("C:/Users/melan/OneDrive/6. TEC-SEXTO SEMESTRE/RECUPERACION DE INFORMACION TEXTUAL/PROYECTO 1/resultados/Dictionary Terms.txt"))