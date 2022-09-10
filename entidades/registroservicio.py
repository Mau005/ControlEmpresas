

class RegistroServicios:
    
    def __init__(self, **kargs):
        self.estructura = {
            "ID_Servicio": kargs.get("id_servicio"),
            "Nombre": kargs.get("nombre"),
            "Descr": kargs.get("descr"),
            "fecha_inicio": kargs.get("fecha_inicio"),
            "fecha_final": kargs.get("fecha_final"),
            "correo": kargs.get("correo"),
            "Estado": kargs.get("estado"),
        }
        
        
    def asignar(self, key,valor):
        self.estructura.update({key:valor})
        
    def estructura(self):
        return self.estructura
    
    def preparar(self):
        self.estructura.update({"estado":"registroservicios"})
        return self.estructura
    
    
if __name__ == "__main__":
    test = RegistroServicios()
    
    print(test.estructura)