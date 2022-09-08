

class Querys():
    
    def __init__(self, bd):
        self.bd = bd
        
    def consultar_usuario(self, correo, contraseña):
        querys = f'SELECT * FROM USUARIOS WHERE CORREO = "{correo}" AND CONTRASEÑA = SHA({contraseña});'
        return self.bd.consultar(querys)
    
    def registrar_usuario(self, correo, contraseña):
        querys = f'INSERT INTO USUARIOS(CORREO,CONTRASEÑA) VALUES("{correo}", SHA({contraseña}));'
        condicion = self.bd.insertar(querys)
        
        if condicion["estado"]:
            return self.__registrar_accesos(correo)
        
        return condicion #retorna usuario existente un dic
    
    def __registrar_accesos(self, correo):
        querys = f'INSERT INTO ACCESOS(CORREO) VALUES("{correo}")'
        return self.bd.insertar(querys)