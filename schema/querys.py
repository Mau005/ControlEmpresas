

class Querys():
    
    def __init__(self, bd):
        self.bd = bd
        
    def consultar_usuario(self, correo, contraseña):
        querys = f'SELECT * FROM USUARIOS WHERE CORREO = "{correo}" AND CONTRASEÑA = SHA({contraseña});'
        return self.bd.consultar(querys)
    
    def registrar_usuario(self, correo, contraseña):
        querys = f'INSERT INTO USUARIOS(CORREO,CONTRASEÑA) VALUES("{correo}", SHA({contraseña}));'
        return self.bd.insertar(querys)
        