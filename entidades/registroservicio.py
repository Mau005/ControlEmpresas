

class RegistroServicios:
    
    def __init__(self, **kargs):
        self.id_servicio = kargs.get("id_servicio")
        self.nombre = kargs.get("nombre")
        self.descr = kargs.get("descr")
        self.fecha_inicio = kargs.get("fecha_inicio")
        self.fecha_termino = kargs.get("fecha_termino")
        self.correo = kargs.get("correo")
        self.id_estado = kargs.get("id_estado")
        self.precio = kargs.get("precio")
        self.rut_persona = kargs.get("rut_persona")
        self.rut_trabajador = kargs.get("rut_trabajador")
        

    def __str__(self):
        return """
        ID Servicios:  {}
        Nombre: {}
        Descripcion: {}
        Fecha Inicio: {}
        Fecha Termino: {}
        Correo {}
        ID_Estado: {}
        Precio: {}
        Rut Persona: {}
        Rut Trabajador: {}
        """.format(self.id_servicio, self.nombre, self.descr,
                   self.fecha_inicio, self.fecha_termino, self.correo,
                   self.id_estado, self.precio, self.rut_persona,
                   self.rut_trabajador)
    
    def preparar(self):
        return {"estado":"registro_servicio", "contenido":self}
    
    
if __name__ == "__main__":
    test = RegistroServicios()
    
    print(test.estructura)