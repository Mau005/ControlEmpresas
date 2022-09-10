import mysql.connector
import sys
from core.constantes import PROTOCOLO
class BaseDatos():
    def __init__(self, estrucura):
        self.estructura = estrucura
        self.conec = None
        self.cursor = None
        self.__conectar()
        self.__cerrar()
        print("BD a Iniciado correctamente")
        
        
    def consultar(self, querys, all = False):
        self.__conectar()
        self.cursor.execute(querys)
        contenido = None
        if all:
            contenido =  self.cursor.fetchall()
        else: 
            contenido = self.cursor.fetchone()
        self.__cerrar()
        
        if contenido != None:
            return {"estado": True, "datos": contenido}
        return {"estado": False}
    
    def insertar(self, querys):
        self.__conectar()
        try: 
            self.cursor.execute(querys)
            self.conec.commit()
            return {"estado":True, "condicion": "Usuario registrado con exito"}
        except mysql.connector.errors.IntegrityError:
            return {"estado": False, "condicion": "Usuario o contraseña ya existe"}
        
    def __conectar(self):
        try:
            self.conec = mysql.connector.connect(
                user = self.estructura.get("usuario"),
                password = self.estructura.get("password"),
                database = self.estructura.get("bd"),
                port= self.estructura.get("port"),
                host = self.estructura.get("host"),
            )
            self.cursor = self.conec.cursor()
            
        except mysql.connector.Error as error:
            print(error)
            input("Precione para continuar... ")
            sys.exit(0)
            
    def __cerrar(self):
        self.conec.close()
        self.cursor.close()
        