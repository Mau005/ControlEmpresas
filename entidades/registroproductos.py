

class RegistroProductos():
    
    def __init__(self, **kargs):
        self.id_producto = kargs.get("id_producto")
        self.nombre_producto = kargs.get("nombre_producto")
        self.descripcion = kargs.get("descripcion")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.cantidad = kargs.get("cantidad")
        
    def __str__(self):
        return """
    
    ID Producto: {}
    Nombre Producto: {}
    Descripcion: {}
    Fecha_Creacion: {}
    cantidad: {}
    """.format(self.id_producto, self.nombre_producto, self.descripcion, self.fecha_creacion,self.cantidad)
    
    def preparar(self):
        return {"estado": "registroproductos", "contenido": self}