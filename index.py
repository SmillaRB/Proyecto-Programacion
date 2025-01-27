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

    def load_stop_words(self, path_doc):
        """Carga las palabras no deseadas desde un archivo."""
        try:
            with open(path_doc, 'r', encoding='utf-8') as file:
                self.stop_words = set(file.read().splitlines())
        except Exception as e:
            print(f"Error cargando las stop words: {e}")

    def clean_text(self, text):
        """Elimina puntuaciones, pasa a minúsculas y excluye palabras no deseadas."""
        text = re.sub(r'[\W_]+', ' ', text.lower()) 
        palabras = text.split()
        return [palabra for palabra in palabras if palabra not in self.stop_words]
   
    def calcular_umbral(self):
        """Calcula el umbral dinámico basado en la frecuencia de las palabras en todo el corpus."""
        palabra_frecuencia = defaultdict(int)
        for palabras in self.Larousse.values():
            for doc, freq in palabras.items():
                palabra_frecuencia[doc] += freq

        total_frecuencias = sum(palabra_frecuencia.values())
        if len(palabra_frecuencia) > 0: 
            self.threshold = total_frecuencias / len(palabra_frecuencia)
        else:
            self.threshold = float('inf') 

    def load_doc(self, ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".txt"):  
                ruta_txt = os.path.join(ruta_carpeta, archivo)
                with open(ruta_txt, 'r', encoding='utf-8') as file:  
                    texto = file.read()
                    self.documentos[archivo] = texto

    def build_index(self):
        total_documentos = len(self.documentos)
        for doc, texto in self.documentos.items():
            palabras = self.clean_text(texto)
            total_palabras = len(palabras)
            frecuencias = defaultdict(int)

            for palabra in palabras:
                frecuencias[palabra] += 1

            for palabra, frecuencia in frecuencias.items():
                self.Larousse[palabra][doc] = frecuencia

            for palabra, frecuencia in frecuencias.items():
                if frecuencia <= self.threshold:  # Excluir palabras muy comunes
                    self.TF_IDF[palabra][doc] = (frecuencia / total_palabras) * math.log10(total_documentos / len(self.Larousse[palabra]))
