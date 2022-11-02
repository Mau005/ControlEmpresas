import pickle
import json
import os
import hashlib
import random
import uuid

import kivy

if kivy.utils.platform != 'android':
    import pandas as pd


class Herramientas:

    @staticmethod
    def generar_excel(ruta, nombre_archivo, lista_datos, columnas):
        if kivy.utils.platform != 'android':
            df_rss = pd.DataFrame(lista_datos, columns=columnas)
            df_rss.to_excel(f"{ruta}\\{nombre_archivo}.xlsx", index=False)

    @staticmethod
    def cargar_archivo(ruta, mensaje):
        if os.path.exists(ruta):
            archivo = open(ruta, "r", encoding="utf-8")
            print("[OK] ", mensaje)
            return archivo.read()
        return None

    @staticmethod
    def generar_numero_unico():
        return uuid.uuid4()

    @staticmethod
    def numero_aleatorio():
        return random.randint(100000, 999999)

    @staticmethod
    def empaquetar(paquete):
        return pickle.dumps(paquete)

    @staticmethod
    def desenpaquetar(paquete):
        try:
            return pickle.loads(paquete)
        except EOFError as error:
            print(error, "Cierre abrupto por parte del servidor")
            return {"estado": False, "condicion": "Caida abrupta del servidor"}

    @staticmethod
    def cifrado_sha1(mensaje):
        contenido = hashlib.sha1(mensaje.encode())
        return contenido.hexdigest()

    @staticmethod
    def cargar_json(ruta):
        if os.path.exists(ruta):
            archivo = open(ruta, "r", encoding="utf-8")
            return json.load(archivo)
        return None

    @staticmethod
    def escribir_json(contenido, ruta):
        if os.path.exists(ruta):
            archivo = open(ruta, "w", encoding="utf-8")
            json.dump(contenido, archivo, ensure_ascii=False)
            archivo.close()

    @staticmethod
    def generar_nombres(datos1, datos2, contador=0):
        """
        Methodo usado para generar nombres
        de usuarios segun sus nombres y apellidos
        """
        if " " in datos1:
            datos1 = datos1.split(" ")
            datos1 = datos1[0][0]
        else:
            datos1 = datos1[0]
        if " " in datos2:
            datos2 = datos2.split(" ")
            datos2 = f"{datos2[0]}{datos2[1][0]}"
        else:
            datos2 = datos2

        if contador >= 1:
            return (datos1 + (datos2 + "0" + str(contador))).lower()
        return (datos1 + datos2).lower()

    @staticmethod
    def recuperacion_sentencia(objeto):
        for elementos in objeto.__dict__.keys():
            if isinstance(objeto.__dict__[elementos], str):
                if objeto.__dict__[elementos] == "":
                    objeto.__dict__[elementos] = "NULL"
                else:
                    objeto.__dict__[elementos] = f'"{objeto.__dict__[elementos]}"'
            if isinstance(objeto.__dict__[elementos], int) or isinstance(objeto.__dict__[elementos], bool) \
                    or isinstance(objeto.__dict__[elementos], float):
                objeto.__dict__[elementos] = f"{objeto.__dict__[elementos]}"
            if objeto.__dict__[elementos] is None:
                objeto.__dict__[elementos] = "NULL"
        return objeto

    @staticmethod
    def verificar_rut(rut):
        """Methodo usado para verificacion de rut, procesando cada segmento divido en 2
        desde el verificador a la cantidad de rut y lo formatea en xx.xxx.xxx-x

        Args:
            rut (str): rut de longitud de 12

        Returns:
            str: procesesado a xx.xxx.xxx-x
        """
        if not ("-" in rut):
            return False, "Rut debe llevar -"

        rut = rut.split("-")  # lista 2 donde se divie en -
        contenido_rut = rut[0].replace(".", "")  # contener el contenido rut
        longitud_rut = len(contenido_rut)

        if longitud_rut >= 9 or longitud_rut <= 6:
            return False, "Rut debe tener entre 7 y 8 numeros"

        if len(rut[1]) != 1:
            return False, "Rut debe tener un digito verificador"

        contenido_rut = contenido_rut.lower()
        if "k" in contenido_rut or "0" in contenido_rut[
            0]:  # comprobamos que no tenga uan K en el contenido del rut y si comienza en 0 tan bien se salga
            return False, "Rut no se logra verificar, Escrito mal"

        formato = "0123456789k"  # formato

        contenido_rut += rut[1].lower()

        verificador_bool = [False for x in range(0, len(contenido_rut))]

        contador = 0
        for caracter_rut in contenido_rut:
            for caracter_formato in formato:
                if caracter_formato == caracter_rut:
                    verificador_bool[contador] = True
            contador += 1

        if False in verificador_bool:
            return False, f"No se puede comprobar el rut correctamente"
        if len(rut[0]) == 8:
            formato_nuevo = f"{rut[0][:2]}.{rut[0][2:5]}.{rut[0][5:8]}"  # es procesar el rut devido a la cantida dde informacion

        else:
            formato_nuevo = f"{rut[0][:1]}.{rut[0][1:4]}.{rut[0][4:8]}"  # es procesar el rut devido a la cantida dde informacion
        return True, f"{formato_nuevo}-{rut[1].lower()}"


if __name__ == "__main__":
    test = Herramientas()
    print(test.verificar_rut("18881888-2"))
