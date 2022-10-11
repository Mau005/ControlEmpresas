

class RegistroProductos:
    #	id_producto	nombre_producto	descripcion	fecha_creacion	cantidad
    def __init__(self, **kargs):
        self.id_producto = kargs.get("id_producto")
        self.nombre_producto = kargs.get("nombre_producto")
        self.descripcion = kargs.get("descripcion")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.cantidad = kargs.get("cantidad")
        self.id_local = kargs.get("id_local")
        
    def __str__(self):
        return """
    
    ID Producto: {}
    Nombre Producto: {}
    Descripcion: {}
    Fecha_Creacion: {}
    cantidad: {}
    Local: {}
    """.format(self.id_producto, self.nombre_producto, self.descripcion, self.fecha_creacion,self.cantidad, self.id_local)
    
    def preparar(self):
        return {"estado": "registro_productos", "contenido": self}