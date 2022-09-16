from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTwoLine
from core.constantes import BUTTONCREATE
from kivy.properties import ObjectProperty


class VListadoServicios(MDScreenAbstrac):
    botones = ObjectProperty()
    contenedor = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.listas_widget = []
        self.botones.data = BUTTONCREATE

    def limpiar_widget(self):
        for elementos in self.listas_widget:
            self.contenedor.remove_widget(elementos)

        self.listas_widget.clear()

    def accion_boton(self, arg):

        if arg.icon == "delete":
            self.limpiar_widget()

        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "pencil":
            data = {"estado": "listadoservicios"}
            self.network.enviar(data)
            info = self.network.recibir()

            if info.get("estado"):
                for x in info.get("datos"):
                    print(f"Que vale x: {x}")
                    obj = MDTwoLine(str(x[0]), x[1], self.network)
                    self.listas_widget.append(obj)
                    self.contenedor.add_widget(obj)

    def activar(self):
        self.limpiar_widget()
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
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
