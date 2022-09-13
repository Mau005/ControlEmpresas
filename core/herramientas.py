
import pickle
import json
import os
import hashlib
class Herramientas:
    
    @staticmethod
    def empaquetar(paquete):
        return pickle.dumps(paquete)
    
    @staticmethod
    def desenpaquetar(paquete):
        return pickle.loads(paquete)
    
    @staticmethod
    def cifrado_sha1(mensaje):
        contenido = hashlib.sha1(mensaje.encode())
        return  contenido.hexdigest()
    
    @staticmethod
    def cargar_json(ruta):
        if os.path.exists(ruta):
            archivo = open(ruta, "r" , encoding = "utf-8")
            print("[OK] Variables importadas correctamente!")
            return json.load(archivo)
        
    @staticmethod
    def escribir_json(contenido, ruta):
        if os.path.exists(ruta):
            archivo = open(ruta,"w", encoding = "utf-8")
            contenido = json.dump(contenido, archivo, ensure_ascii=False)
            archivo.close()
    
if __name__ == "__main__":
    test = Herramientas()
    x = {1:"hola"}
    test.escribir_json(x, "uno.json")