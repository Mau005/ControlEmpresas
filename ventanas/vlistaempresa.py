from ventanas.widgets_predefinidos import MDScreenAbstrac, MDTwoLine, MDTwoLineObjecto
from kivy.properties import ObjectProperty


class VListasEmpresas(MDScreenAbstrac):
    contenedor = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.contenido_empresas = []

    def formatear(self, *args):
        for obj in self.contenido_empresas:
            self.contenedor.remove_widget(obj)
        self.contenido_empresas.clear()

    def activar(self):
        self.formatear()
        data = {"estado": "lista_empresas"}
        self.network.enviar(data)
        info = self.network.recibir()

        if info.get("estado"):
            for x in info.get("datos"):
                obj = MDTwoLineObjecto(x[0], x[1], self.network, self.manager, "editar_empresa", "buscar_empresa_rut")
                self.contenido_empresas.append(obj)
                self.contenedor.add_widget(obj)
        super().activar()

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
