from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE
from entidades.registroproductos import RegistroProductos


class VProductos(MDScreenAbstrac):
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.botones.data = BUTTONCREATE

    def formatear(self):
        self.ids.nombre_producto.text = ""
        self.ids.descripcion.text = ""
        self.ids.cantidad.text = ""

    def accion_boton(self, arg):
        self.botones.close_stack()
        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "pencil":
            noti = Notificacion("Error", "")

            if not len(self.ids.nombre_producto.text) >= 3:
                noti.text += "El Nombre debe tener almenos 3 caracteres\n"
            if not len(self.ids.cantidad.text) <= 11:
                noti.text += "La cantida de productos no puede superar los 11 digitos\n"

            if noti.text == "":
                objeto = RegistroProductos(nombre_producto=self.ids.nombre_producto.text,
                                           descripcion=self.ids.descripcion.text,
                                           cantidad=int(self.ids.cantidad.text))
                self.network.enviar(objeto.preparar())
                info = self.network.recibir()

                if info.get("estado"):
                    noti.title = "Exito"
                    noti.text = "Se ha registrado con exito la información"
                else:
                    noti.text = info.get("condicion")

            noti.open()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
