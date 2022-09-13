

class RegistroUsuarios():
    def __init__(self,**kargs):
        self.estructura = kargs
        self.correo = kargs.get("correo")
        self.contraseña = kargs.get("contraseña")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.estado_usuario = kargs.get("estado_usuario")
        
    def __str__(self):
        return '''
    Correo: {}
    Contraseña: {}
    Fecha Creacion: {}
    Estado Usuario: {}
    '''.format(self.correo, self.contraseña, self.fecha_creacion, self.estado_usuario)
    
    def preparar(self):
        return {"estado":"registrousuarios", "contenido":self}
    
if __name__ == "__main__":
    estructura = {"correo":"mpino1701@gmail.com", "contraseña": "123", "fecha_creacion": "2022-09-02", "estado_usuario": 2}
    user = RegistroUsuarios(**estructura)
    print(user)