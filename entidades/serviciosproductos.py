

class ServiciosProductos:
    def __init__(self, **kargs):
        self.id_servicio_productos = kargs.get("id_servicio_productos")
        self.id_producto = kargs.get("id_producto")
        self.cantidad = kargs.get("cantidad")
        self.precio = kargs.get("precio")
        self.id_servicio = kargs.get("id_servicio")

    def __str__(self):
        return """
        ID: {}
        Id Producto: {}
        Cantidad: {}
        Precio: {}
        Id Servicio_ {}
        """.format(self.id_servicio_productos, self.id_producto,
                   self.cantidad, self.precio, self.id_servicio)