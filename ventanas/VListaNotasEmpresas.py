from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty
from ventanas.widgets_predefinidos import MenuEntidades


class VListaNotasEmpresas(MDScreenAbstrac):
    contenedor_registros = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_empresas = MenuEntidades(self.network, "Rut Empresa:", "Rut Empresa:", self.ids.rut_empresa)

    def activar(self):
        super().activar()
        self.coleccion_empresas.generar_consulta("menu_empresas")


    def actualizar(self, dt):
        super().actualizar(dt)

        if self.coleccion_empresas.actualizado:
            self.network.enviar({"estado": "listado_notas_empresa_especifica","contenido":self.coleccion_empresas.dato_guardar})
            info = self.network.recibir()

            if info.get("estado"):
                print(info.get("datos"))

            self.coleccion_empresas.actualizado = False


    def siguiente(self, *dt):
        super().siguiente()

    def volver(self):
        super().volver()
