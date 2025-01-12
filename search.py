from Levenshtein import distance as levenshtein_distance
from collections import defaultdict

class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer
    
    def obtener_snippet(self, documento, palabras_query):
        """Encuentra el fragmento más relevante del documento para las palabras de la consulta."""
        texto = self.indexer.documentos[documento]
        palabras_documento = texto.split()

        max_relevancia = 0
        mejor_inicio = 0
        mejor_fin = 0

        ventana_tamano = 30  
        palabras_posiciones = [i for i, palabra in enumerate(palabras_documento) if palabra in palabras_query]

        if not palabras_posiciones:
            return texto[:200] 

        for i in palabras_posiciones:
            inicio = max(0, i - ventana_tamano // 2)
            fin = min(len(palabras_documento), i + ventana_tamano // 2)
            ventana = palabras_documento[inicio:fin]

            relevancia = sum(1 for palabra in palabras_query if palabra in ventana)

            if relevancia > max_relevancia:
                max_relevancia = relevancia
                mejor_inicio = inicio
                mejor_fin = fin

        snippet = " ".join(palabras_documento[mejor_inicio:mejor_fin])

        punto_inicio = texto.find(snippet)
        if punto_inicio != -1:
            punto_fin = texto.find(".", punto_inicio + len(snippet))  
            if punto_fin != -1:
                snippet = texto[punto_inicio:punto_fin + 1]

        return snippet
    
    def query(self, query):
        palabras_query = self.indexer.limpiar_texto(query)  
        scores = defaultdict(float)
        sugerencias = {}

        for palabra in palabras_query:
            if palabra in self.indexer.Larousse:
                for doc, tfidf in self.indexer.TF_IDF[palabra].items():
                    scores[doc] += tfidf
            else:
                mejor_distancia = float('inf')
                mejor_palabra = None
                for palabra_indexada in self.indexer.Larousse.keys():
                    distancia = levenshtein_distance(palabra, palabra_indexada)
                    if distancia < mejor_distancia and distancia < 3:
                        mejor_distancia = distancia
                        mejor_palabra = palabra_indexada
                if mejor_palabra:
                    sugerencias[palabra] = mejor_palabra
                    for doc, tfidf in self.indexer.TF_IDF[mejor_palabra].items():
                        scores[doc] += tfidf

        resultados = sorted(scores.items(), key=lambda x: -x[1])
        
        resultados_con_snippets = [
            (doc, score, self.obtener_snippet(doc, palabras_query)) for doc, score in resultados
        ]

        return resultados_con_snippets, sugerencias