from index import DocumentIndexer
from search import SearchEngine
from app import MoogleApp
import tkinter as tk

def main():
    indexer = DocumentIndexer()
    indexer.load_stop_words("stop_words.txt")
    indexer.load_doc("Edgar allan poe")

    if not indexer.documentos:  
        print("No se encontraron documentos válidos en la ruta especificada.")
        return
    
    indexer.calcular_umbral()  
    indexer.build_index()  

    engine = SearchEngine(indexer)

    root = tk.Tk()
    app = MoogleApp(root, engine)
    root.mainloop()
if __name__ == "__main__":
    main()
