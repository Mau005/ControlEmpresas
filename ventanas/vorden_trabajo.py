from entidades.orden_trabajos import Orden_Trabajos
from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades


class VOrden_Trabajos(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.orden_trabajo = Orden_Trabajos()
        self.coleccion_departamento = MenuEntidades(self.network, "Departamento:",
                                                    "Departamento:", self.ids.id_departamento_ot, filtro="int")
        self.coleccion_servicios = MenuEntidades(self.network, "Servicios:",
                                                    "Servicios:", self.ids.id_servicios, filtro="int")


    def activar(self):
        super().activar()
        self.coleccion_departamento.generar_consulta("menu_departamentos")
        #self.coleccion_servicios.generar_consulta("menu_servicios_activos")

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
