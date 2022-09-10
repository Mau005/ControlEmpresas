

class RegistroServicios:
    
    def __init__(self):
        self.estructura = {
            "ID_Servicio": None,
            "Nombre": None,
            "Descr": None,
            "Fecha_Inicio": None,
            "Fecha_Termino": None,
            "Historial_Registros": None,
            "Correo": None,
            "Estado": None,
        }
        
        
    def asignar(self, key,valor):
        self.estructura[key] = valor
        
    def estructura(self):
        return self.estructura
    
    def preparar(self):
        self.estructura["estado"] = "registroservicio"
        return self.estructura
    
    
if __name__ == "__main__":
    test = RegistroServicios()
    
    print(test.estructura)