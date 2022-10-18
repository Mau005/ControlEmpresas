from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTwoLine
from kivy.properties import ObjectProperty


class VListadoServicios(MDScreenAbstrac):
    contenedor = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.listas_widget = []

    def crear(self, *args):
        data = {"estado": "listadoservicios"}
        self.network.enviar(data)
        info = self.network.recibir()

        if info.get("estado"):
            for x in info.get("datos"):
                print(f"Que vale x: {x}")
                obj = MDTwoLine(str(x[0]), x[1], self.network)
                self.listas_widget.append(obj)
                self.contenedor.add_widget(obj)

    def formatear(self, *args):
        for elementos in self.listas_widget:
            self.contenedor.remove_widget(elementos)

        self.listas_widget.clear()

    def accion_boton(self, *args):
        self.ids.botones_lista_servicios.close_stack()

    def activar(self):
        self.formatear()
        data = {"estado": "listadoservicios"}
        self.network.enviar(data)
        info = self.network.recibir()
        if info.get("estado"):
            for x in info.get("datos"):
                obj = MDTwoLine(str(x[0]), x[1], self.network)
                self.listas_widget.append(obj)
                self.contenedor.add_widget(obj)
        super().activar()

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
