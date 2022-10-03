from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTreeLine
from core.constantes import BUTTONCREATE
from kivy.properties import ObjectProperty


class VListaProductos(MDScreenAbstrac):
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
        self.botones.close_stack()
        if arg.icon == "delete":
            pass

        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "pencil":
            pass

    def activar(self):
        self.limpiar_widget()
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
        return super().siguiente(*dt)

    def volver(self):
        return super().volver()

    def actualizar(self, *dt):
        return super().actualizar(*dt)
