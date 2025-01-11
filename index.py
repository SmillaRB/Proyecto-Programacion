import os
import re
import math
from collections import defaultdict

class DocumentIndexer:
    def __init__(self):
        self.Larousse = defaultdict(dict)
        self.TF_IDF = defaultdict(dict)
        self.documentos = {}
        self.threshold = None
        self.stop_words = set() 

    def cargar_stop_words(self, ruta_archivo):
        """Carga las palabras no deseadas desde un archivo."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                self.stop_words = set(file.read().splitlines())
        except Exception as e:
            print(f"Error cargando las stop words: {e}")

    def limpiar_texto(self, texto):
        """Elimina puntuaciones, pasa a minúsculas y excluye palabras no deseadas."""
        texto = re.sub(r'[\W_]+', ' ', texto.lower()) 
        palabras = texto.split()
        return [palabra for palabra in palabras if palabra not in self.stop_words]

    def cargar_documentos(self, ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".txt"):  
                ruta_txt = os.path.join(ruta_carpeta, archivo)
                with open(ruta_txt, 'r', encoding='utf-8') as file:  
                    texto = file.read()
                    self.documentos[archivo] = texto