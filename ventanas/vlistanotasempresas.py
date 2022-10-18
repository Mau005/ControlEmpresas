from ventanas.widgets_predefinidos import MDScreenAbstrac, ItemNotaEmpresa
from ventanas.widgets_predefinidos import MenuEntidades


class VListaNotasEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_empresas = MenuEntidades(self.network, "Rut Empresa:", "Rut Empresa:", self.ids.rut_empresa)
        self.objetos_widgets = []

    def crear(self, *args):
        self.coleccion_empresas.desplegar_menu()

    def activar(self, *args):
        self.coleccion_empresas.generar_consulta("menu_empresas")
        super().activar()

    def formatear(self, *args):
        for widget in self.objetos_widgets:
            self.ids.contenedor_registros.remove_widget(widget)
        self.objetos_widgets.clear()

    def actualizar(self, dt):
        super().actualizar(dt)
        if self.coleccion_empresas.actualizado:
            self.network.enviar(
                {"estado": "listado_notas_empresa_especifica", "contenido": self.coleccion_empresas.dato_guardar})
            info = self.network.recibir()

            if info.get("estado"):
                self.formatear()
                for objetos in info.get("datos"):
                    obj = ItemNotaEmpresa(self.network, objetos)
                    self.objetos_widgets.append(obj)
                    self.ids.contenedor_registros.add_widget(obj)

            self.coleccion_empresas.actualizado = False

    def siguiente(self, *dt):
        self.formatear()
        super().siguiente()

    def volver(self):
        super().volver()
