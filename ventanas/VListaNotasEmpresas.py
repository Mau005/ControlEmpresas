from ventanas.widgets_predefinidos import MDScreenAbstrac, ItemNotaEmpresa
from ventanas.widgets_predefinidos import MenuEntidades
class VListaNotasEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_empresas = MenuEntidades(self.network, "Rut Empresa:", "Rut Empresa:", self.ids.rut_empresa)
        self.objetos_widgets = []
        self.ids.botones.data = {'Buscar': 'book-search', 'Formatear': 'delete', 'Salir': 'exit-run'}

    def activar(self):
        super().activar()
        self.coleccion_empresas.generar_consulta("menu_empresas")

    def accion_boton(self, arg):
        self.ids.botones.close_stack()
        if arg.icon == "delete":
            self.limpiar_widget()

        if arg.icon == "exit-run":
            self.siguiente()
        if arg.icon == "book-search":
            self.coleccion_empresas.desplegar_menu()

    def limpiar_items(self):
        for widget in self.objetos_widgets:
            self.ids.contenedor_registros.remove_widget(widget)
        self.objetos_widgets.clear()

    def actualizar(self, dt):
        super().actualizar(dt)
        if self.coleccion_empresas.actualizado:
            self.network.enviar({"estado": "listado_notas_empresa_especifica","contenido":self.coleccion_empresas.dato_guardar})
            info = self.network.recibir()

            if info.get("estado"):
                self.limpiar_items()
                for objetos in info.get("datos"):
                    obj = ItemNotaEmpresa(self.network, objetos)
                    self.objetos_widgets.append(obj)
                    self.ids.contenedor_registros.add_widget(obj)


            self.coleccion_empresas.actualizado = False


    def siguiente(self, *dt):
        super().siguiente()

    def volver(self):
        super().volver()
