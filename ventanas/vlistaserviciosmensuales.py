from ventanas.widgets_predefinidos import MDScreenAbstrac, ItemNotas, MDDialogCheck
from ventanas.widgets_predefinidos import MenuEntidades


class VListaServiciosMensuales(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.objetos_widgets = []
        self.check_pop = MDDialogCheck(title= "Cuadro De Busqueda")

    def abrir_buscador(self, *args):
        self.check_pop.open()


    def crear(self, *args):
        data = {}
        data.update({"clausulas":self.check_pop.Generar_Activos(), "id":self.ids.buscador.text})


    def activar(self, *args):
        super().activar()

    def formatear(self, *args):
        pass

    def actualizar(self, dt):
        super().actualizar(dt)

    def siguiente(self, *dt):
        self.formatear()
        super().siguiente()

    def volver(self):
        super().volver()
