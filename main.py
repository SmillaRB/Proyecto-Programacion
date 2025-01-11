from index import DocumentIndexer
from search import SearchEngine
from app import MoogleApp
import tkinter as tk

def main():
    indexer = DocumentIndexer()
    indexer.cargar_stop_words("C:\Pro\Moogle in Py\stop_words.txt")
    indexer.cargar_documentos("C:\Pro\Moogle in Py\Edgar allan poe")  
    if not indexer.documentos:  
        print("No se encontraron documentos válidos en la ruta especificada.")
        return

if __name__ == "__main__":
    main()
