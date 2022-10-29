from ventanas.widgets_predefinidos import MDScreenAbstrac, ItemNotas
from ventanas.widgets_predefinidos import MenuEntidades


class VListaNotasPersonas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_personas = MenuEntidades(self.network, "Rut Persona:", "Rut Persona:", self.ids.rut_persona)
        self.objetos_widgets = []

    def crear(self, *args):
        self.coleccion_personas.desplegar_menu()

    def activar(self, *args):
        self.coleccion_personas.generar_consulta("menu_personas")
        super().activar()

    def formatear(self, *args):
        for widget in self.objetos_widgets:
            self.ids.contenedor_registros.remove_widget(widget)
        self.objetos_widgets.clear()

    def actualizar(self, dt):
        super().actualizar(dt)
        if self.coleccion_personas.actualizado:
            self.network.enviar(
                {"estado": "listado_notas_persona_especifica", "contenido": self.coleccion_personas.dato_guardar})
            info = self.network.recibir()

            if info.get("estado"):
                self.formatear()
                for objetos in info.get("datos"):
                    obj = ItemNotas(self.network, objetos)
                    self.objetos_widgets.append(obj)
                    self.ids.contenedor_registros.add_widget(obj)

            self.coleccion_personas.actualizado = False

    def siguiente(self, *dt):
        self.formatear()
        super().siguiente()

    def volver(self):
        super().volver()
