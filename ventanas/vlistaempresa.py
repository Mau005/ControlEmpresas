from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTwoLine
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE


class VListasEmpresas(MDScreenAbstrac):
    contenedor = ObjectProperty()
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.botones.data = BUTTONCREATE
        self.contenido_empresas = []

    def accion_boton(self, arg):
        if arg.icon == "pencil":
            self.activar()
        if arg.icon == "exit-run":
            self.siguiente()
        if arg.icon == "delete":
            self.limpiar_objetos()

    def limpiar_objetos(self):
        for obj in self.contenido_empresas:
            self.contenedor.remove_widget(obj)
        self.contenido_empresas.clear()

    def activar(self):
        # self.limpiar_objetos()
        data = {"estado": "listaEmpresas"}
        self.network.enviar(data)
        info = self.network.recibir()

        if info.get("estado"):
            for x in info.get("datos"):
                obj = MDTwoLine(x[0], x[1], self.network)
                self.contenido_empresas.append(obj)
                self.contenedor.add_widget(obj)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
