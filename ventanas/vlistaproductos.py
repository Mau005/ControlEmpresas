from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTreeLine
from kivy.properties import ObjectProperty


class VListaProductos(MDScreenAbstrac):
    contenedor = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.listas_widget = []

    def formatear(self, *args):
        for elementos in self.listas_widget:
            self.contenedor.remove_widget(elementos)

        self.listas_widget.clear()

    def activar(self):
        self.formatear()
        data = {"estado": "listadoproductos"}
        self.network.enviar(data)
        info = self.network.recibir()
        if info.get("estado"):
            for x in info.get("datos"):
                obj = MDTreeLine(str(x[0]), x[1], x[2], self.network)
                self.listas_widget.append(obj)
                self.contenedor.add_widget(obj)
        super().activar()

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self):
        return super().volver()

    def actualizar(self, *dt):
        return super().actualizar(*dt)
