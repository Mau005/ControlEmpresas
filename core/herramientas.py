import pickle
import json
import os
class Herramientas:
    
    @staticmethod
    def empaquetar(paquete):
        return pickle.dumps(paquete)
    
    @staticmethod
    def desenpaquetar(paquete):
        return pickle.loads(paquete)
    
    @staticmethod
    def cargar_json(ruta):
        if os.path.exists(ruta):
            archivo = open(ruta, "r" , encoding = "utf-8")
            return json.load(archivo)
    
if __name__ == "__main__":
    test = Herramientas()
    x = {1:"hola"}
    objeto = test.empaquetar(x)
    print(f"Encriptado: {objeto}")
    print(f"Desencriptar: {test.desenpaquetar(objeto)}")
    