

class RegistroServicios:
    
    def __init__(self, **kargs):
        self.estructura = {
            "id_servicio": kargs.get("id_servicio"),
            "nombre": kargs.get("nombre"),
            "descr": kargs.get("descr"),
            "fecha_inicio": kargs.get("fecha_inicio"),
            "fecha_termino": kargs.get("fecha_termino"),
            "correo": kargs.get("correo"),
            "id_estado": kargs.get("id_estado"),
            "precio": kargs.get("precio")
        }
        
        
    def asignar(self, key,valor):
        self.estructura.update({key:valor})
        
    def estructura(self):
        return self.estructura
    
    def preparar(self):
        self.estructura.update({"estado":"registroservicio"})
        return self.estructura
    
    
if __name__ == "__main__":
    test = RegistroServicios()
    
    print(test.estructura)