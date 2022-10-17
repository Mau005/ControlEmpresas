from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from entidades.registroproductos import RegistroProductos


class VProductos(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.ids.botones_productos.data = {'Crear': ["pencil", "on_release", self.crear],
                                         'Formatear': ["delete", "on_release", self.formatear],
                                         'Salir': ["exit-run", "on_release", self.siguiente]}
        self.colecciones_menu_local = MenuEntidades(self.network, "Local:", "Local:", self.ids.menu_local, filtro="int")

    def crear(self, *args):
        noti = Notificacion("Error", "")
        estado = True
        if not len(self.ids.nombre_producto.text) >= 3:
            noti.text += "El Nombre debe tener almenos 3 caracteres\n"
            estado = False
        if not len(self.ids.cantidad.text) <= 11:
            noti.text += "La cantida de productos no puede superar los 11 digitos\n"
            estado = False

        if self.ids.menu_local.text == "Local:":
            noti.text += "Debe seleccionar un local."
            estado = False

        if not estado:
            noti.open()
            return None

        objeto = RegistroProductos(nombre_producto=self.ids.nombre_producto.text,
                                   descripcion=self.ids.descripcion.text,
                                   cantidad=int(self.ids.cantidad.text),
                                   id_local=self.colecciones_menu_local.dato_guardar)
        self.network.enviar(objeto.preparar())
        info = self.network.recibir()

        if info.get("estado"):
            noti.title = "Exito"
            noti.text = "Se ha registrado con exito la información"
            noti.open()
            self.formatear()
            return None

        noti.text = info.get("condicion")
        noti.open()
        return None
    def formatear(self, *args):
        self.ids.nombre_producto.text = ""
        self.ids.descripcion.text = ""
        self.ids.cantidad.text = ""
        self.colecciones_menu_local.dato_guardar = None
        self.ids.menu_local.text = "Local:"

    def activar(self):
        super().activar()
        self.colecciones_menu_local.generar_consulta("menu_locales")

    def accion_boton(self, arg):
        self.ids.botones_productos.close_stack()

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
