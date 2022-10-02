from kivymd.uix.bottomsheet import MDListBottomSheet

from entidades.registroserviciosdiarios import RegistroServiciosDiarios
from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE


class VServiciosDiarios(MDScreenAbstrac):
    nombre = ObjectProperty()
    descr = ObjectProperty()
    id_estado = ObjectProperty()
    precio = ObjectProperty()
    botones_servicios = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.botones_servicios.data = self.data
        self.correo = "prueba"
        self.servicio_actual = 1  # por defecto bd es operativo
        self.lista_estados = {}
        self.lista_personas = {}
        self.lista_trabajadores = {}
        self.cliente_actual = ""
        self.trabajador_actual = ""
        self.toda_la_semana = False
        self.coleccion_menu_estados = MenuEntidades(self.network, "Estado:", "Estado:", self.ids.id_estado, filtro="int")
        self.coleccion_menu_personas = MenuEntidades(self.network, "Rut Cliente:", "Rut:", self.ids.botton_rut_accion)
        self.coleccion_menu_trabajadores = MenuEntidades(self.network, "Rut Trabajador:", "Rut:",
                                                         self.ids.botton_rut_trabajador)
        self.coleccion_menu_productos = MenuEntidades(self.network, "ID Producto:", "ID:", self.ids.menu_producto,
                                                      filtro="int")

    def accion_boton(self, arg):
        if arg.icon == "delete":
            self.formatear()
        if arg.icon == "exit-run":
            self.botones_servicios.on_close()
            self.siguiente()
        if arg.icon == "pencil":
            objeto = RegistroServiciosDiarios(
                nombre_servicio=self.ids.nombre.text,
                id_estado=self.coleccion_menu_estados.dato_guardar,
                precio=int(self.ids.precio.text),
                fecha_semana=self.__dias_diarios(),
                url_posicion=self.ids.url_posicion.text,
                ubicacion=self.ids.ubicacion.text,
                rut_usuario=self.coleccion_menu_personas.dato_guardar,
                rut_trabajador=self.coleccion_menu_trabajadores.dato_guardar,
                descr=self.ids.descr.text,
                toda_semana=self.toda_la_semana,
                id_producto=self.coleccion_menu_productos.dato_guardar,
                cantidad=int(self.ids.cantidad_productos.text)
            )
            if not self.__prueba_check(objeto):
                return

            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            noti = Notificacion("Error", "")
            if info.get("estado"):
                noti.title = "Exito"
                noti.text = "Se ha generado el servicio con Exito"
                noti.open()
                return
            if info.get("condicion") == "REGISTRO":
                noti.text += "Ha ocurrido un problema al gestionar este servicio\n"
            if info.get("condicion") == "NETWORK":
                noti.text += "Seha desconectado del servidor.\n"
            noti.open()

    def __prueba_check(self, objeto):
        noti = Notificacion("Error", "")
        if not len(objeto.nombre_servicio) >= 5 and not len(objeto.nombre_servicio) <= 100:
            noti.text += "El Nombre del servicio debe tener almenos entre 5 a 100 caracteres\n"
        if self.ids.id_estado.text == "Estados":
            noti.text += "El Estado debe ser seleccionado\n"
        if objeto.id_producto is None:
            noti.text += "Debe seleccionar un producto\n"
        if objeto.id_producto == "":
            noti.text += "La cantidad de productos debe ser un numero positivo\n"
        if self.ids.precio.text == "":
            noti.text += "El Precio debe ser un numero positivo\n"
        if not len(objeto.fecha_semana) >= 1:
            noti.text += "Tiene que seleccionar almenos un dia de la semana\n"
        if not len(objeto.ubicacion) >= 5:
            noti.text += "La Ubicación tiene que tener entre 5 a 250 caracteres\n"
        if objeto.rut_usuario is None:
            noti.text += "Rut del Cliente tiene que ser seleccionado\n"
        if objeto.rut_trabajador is None:
            noti.text += "Rut del Trabajador tiene que ser seleccionado\n"
        if len(noti.text) >= 3:
            noti.open()
            return False
        return True

    def __dias_diarios(self):
        dias_diarios = ""
        if self.ids.lunes.active:
            dias_diarios += "1"
        if self.ids.martes.active:
            dias_diarios += "2"
        if self.ids.miercoles.active:
            dias_diarios += "3"
        if self.ids.jueves.active:
            dias_diarios += "4"
        if self.ids.viernes.active:
            dias_diarios += "5"
        if self.ids.sabado.active:
            dias_diarios += "6"
        if self.ids.domingo.active:
            dias_diarios += "7"
        self.toda_la_semana = self.ids.toda_semana.active

        return dias_diarios

    def formatear(self):
        self.nombre.text = ""
        self.id_estado.text = "Estado"
        self.descr.text = ""
        self.precio.text = ""

    def activar(self):
        super().activar()
        condicion = self.coleccion_menu_estados.generar_consulta("menu_estado")
        if condicion.get("estado"):
            self.ids.id_estado.bind(on_release=self.coleccion_menu_estados.desplegar_menu)

        condicion = self.coleccion_menu_personas.generar_consulta("menu_personas")
        if condicion.get("estado"):
            self.ids.botton_rut_accion.bind(on_release=self.coleccion_menu_personas.desplegar_menu)

        condicion = self.coleccion_menu_trabajadores.generar_consulta("menu_trabajadores")
        if condicion.get("estado"):
            self.ids.botton_rut_trabajador.bind(on_release=self.coleccion_menu_trabajadores.desplegar_menu)

        condicion = self.coleccion_menu_productos.generar_consulta("menu_productos")
        if condicion.get("estado"):
            self.ids.menu_producto.bind(on_release=self.coleccion_menu_productos.desplegar_menu)
        print("Condicion en servicios diarios, ", condicion)

    def desplegar_menu(self):
        bottom_sheet_menu = MDListBottomSheet()
        for objetos in self.lista_estados.keys():
            bottom_sheet_menu.add_item(objetos, self.callback_menu)
        bottom_sheet_menu.open()

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
