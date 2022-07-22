import os, json
def cargar_json(ruta):
    if os.path.exists(ruta):
        archivo = open(ruta, "r" , encoding = "utf-8")
        return json.load(archivo)


print(cargar_json("data/ConfiguracionServidor.json"))