import os
from abc import abstractmethod

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem, MDList
from kivymd.uix.textfield import MDTextField

from core.constantes import PROTOCOLOERROR
from entidades.menuitems import MenuGlobal
from entidades.registronotas import RegistroNotas
from entidades.registropersonas import RegistroPersonas
from entidades.serviciosproductos import ServiciosProductos


class ControlArchivos(MDFileManager):
    def __init__(self, funcion=None, **kargs):
        super().__init__(**kargs)
        Window.bind(on_keyboard=self.events)
        self.search = "dirs"
        self.preview = True
        self.manager_open = False
        self.ruta = None
        self.nombre_archivo = None
        self.captura_archivo = NotificacionText("", "Nombre Archivo", aceptar=None if funcion is None else funcion)

    def file_manager_open(self):
        self.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        self.ruta = path
        self.captura_archivo.title = self.ruta
        self.captura_archivo.open()
        self.exit_manager()

        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class ItemContable(TwoLineListItem):
    def __init__(self, id_producto, tipo, precio, usuario, departamento, fecha, boton=None, **kargs):
        # 1, 800000, 'admin', 'Transporte Hyndai', datetime.datetime(2022, 10, 12, 12, 3, 23)
        self.id_producto = id_producto
        self.tipo = tipo
        self.precio = precio
        self.departamento = departamento
        self.usuario = "Sin Usuario" if usuario is None else usuario
        self.fecha = fecha
        self.boton = boton
        super().__init__(**kargs)
        self.text = f"ID: {self.id_producto} Tipo: {self.tipo} Precio: {self.precio}"
        self.secondary_text = f"Creado: {self.usuario}, , Fecha: {self.fecha} Departamento: {self.departamento}"


class ItemProductos(MDBoxLayout):
    indice = 0

    def __init__(self, id_producto, nombre, contenedor=None, precio="0", cantidad="1", **kargs):
        self.contador()
        self.id_interno = self.indice
        self.contenedor = contenedor
        self.id_producto = id_producto
        self.nombre = nombre
        super().__init__(kargs)
        self.nombre = MDLabel(text=f"{self.id_interno} {self.nombre}")
        self.precio = MDTextField(hint_text="Precio", text=precio, input_filter="int")
        self.cantidad = MDTextField(hint_text="Cantidad", text=cantidad, input_filter="int", size_hint_x=None,
                                    width=dp(25))
        self.boton_eliminar = MDRoundFlatButton(text="Eliminar", on_release=self.eliminar, size_hint_x=None,
                                                width=dp(15))
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(75)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.add_widget(self.nombre)
        self.add_widget(self.precio)
        self.add_widget(self.cantidad)
        self.add_widget(self.boton_eliminar)

    def generar(self):
        if self.cantidad.text == "" or self.precio.text == "":
            return

        producto = ServiciosProductos(
            id_producto=self.id_producto,
            cantidad=int(self.cantidad.text),
            precio=int(self.precio.text)
        )
        return producto

    def eliminar(self, *args):
        if self.contenedor is not None:
            self.contenedor.remove_widget(self)

    @classmethod
    def contador(cls):
        cls.indice += 1


class MenuEntidades:

    def __init__(self, network, nombre_boton, nombre_busqueda, boton_modificar, filtro="str"):
        """
        Clase definida para crear multiples consulta de botones para seleccionar
        cosas, soporta 2 argumentos de retorno
        """
        self.nombre_boton = nombre_boton
        self.nombre_busqueda = nombre_busqueda
        self.network = network
        self.boton_modificar = boton_modificar
        self.listados = {}
        self.dato_guardar = None
        self.filtro = filtro
        self.boton_modificar.bind(on_release=self.desplegar_menu)
        self.actualizado = False

    def __limpiada(self):
        self.listados.clear()

    def __conversion(self):
        if self.filtro == "int":
            self.dato_guardar = int(self.dato_guardar)
        elif self.filtro == "float":
            self.dato_guardar = float(self.dato_guardar)
        elif self.filtro == "bool":
            self.dato_guardar = bool(self.dato_guardar)
        elif self.filtro == "str":
            if isinstance(self.dato_guardar, str):
                if len(self.dato_guardar) == 0:
                    self.dato_guardar = None

    def formateo(self):
        self.actualizado = False
        self.dato_guardar = None

    def callback(self, arg):
        procesar = arg.text.split(":")
        identificador = procesar[1].split("\n")

        objeto = self.listados.get(identificador[0].replace(" ", ""))
        self.dato_guardar = objeto.identificador
        self.boton_modificar.text = f"{self.nombre_boton} {identificador[0]}\n{identificador[1]}"
        self.__conversion()
        self.actualizado = True

    def desplegar_menu(self, *args):
        bottom_sheet_menu = MDListBottomSheet()
        for objetos in self.listados.values():
            bottom_sheet_menu.add_item(f"{self.nombre_busqueda} {objetos.identificador}\n{objetos.nombre}",
                                       self.callback)
        bottom_sheet_menu.open()

    def generar_consulta(self, consultar):
        self.__limpiada()
        self.network.enviar({"estado": consultar})
        info = self.network.recibir()
        if info.get("estado"):
            for elementos in info.get("datos"):
                objeto = MenuGlobal(str(elementos[0]), elementos[1])
                self.listados.update({objeto.identificador: objeto})
            return {"estado": True}
        return {"estado": False, "condicion": "CONSULTA"}


class MenuEntidadesMultiples:
    def __init__(self, network, contenedor, btn):
        self.network = network
        self.contenedor = contenedor
        self.lista_objetos = []
        self.btn = btn
        self.btn.bind(on_release=self.desplegar_menu)

    def callback(self, arg):
        procesar = arg.text.split(":")
        identificador = procesar[1].split("\n")
        self.contenedor.add_widget(ItemProductos(identificador[0], identificador[1], contenedor=self.contenedor))

    def desplegar_menu(self, *args):
        bottom_sheet_menu = MDListBottomSheet()
        for objetos in self.lista_objetos:
            bottom_sheet_menu.add_item(f"ID:{objetos.identificador}\n{objetos.nombre}",
                                       self.callback)
        bottom_sheet_menu.open()

    def generar_consulta(self, consulta):
        self.network.enviar({"estado": consulta})
        info = self.network.recibir()
        if info.get("estado"):
            for elementos in info.get("datos"):
                objeto = MenuGlobal(str(elementos[0]), elementos[1])
                self.lista_objetos.append(objeto)


class MDTreeLine(ThreeLineListItem):

    def __init__(self, id_identificador, nombres, cantidad, network, **kargs):
        super().__init__(**kargs)
        self.network = network
        self.id_identificador = id_identificador
        self.nombres = nombres
        self.cantidad = cantidad
        self.text = str(self.id_identificador)
        self.secondary_text = f"Nombre: {self.nombres}"
        self.tertiary_text = f"Cantidad: {self.cantidad}"
        self.procesar_colores(cantidad)

    def procesar_colores(self, cantidad):
        self.tertiary_theme_text_color = "Custom"
        if cantidad >= 0 and cantidad <= 3:
            self.tertiary_text_color = [1, 0, 0, 1]
        elif cantidad >= 4 and cantidad <= 10:
            self.tertiary_text_color = [0, .5, 0, 1]
        elif cantidad >= 11:
            self.tertiary_text_color = [0, 1, 0, 1]


class MDTwoLine(TwoLineListItem):
    def __init__(self, titulo, contenido, network, **kwargs):
        super().__init__(**kwargs)
        self.text = titulo
        self.secondary_text = contenido
        self.network = network


class MDTwoLinePersonas(TwoLineListItem):
    def __init__(self, titulo, contenido, network, **kwargs):
        super().__init__(**kwargs)
        self.titulo = titulo
        self.secondary_text = contenido
        self.network = network
        self.dialogo = InformacionPersona(self.network, f"Rut: {self.titulo}", self.titulo)

        self.bind(on_release=self.abrir)

    def abrir(self, *args):
        self.dialogo.activar()
        self.dialogo.open()


class NotificacionText(MDDialog):

    def __init__(self, title, ayuda, aceptar=None, **kargs):
        self.auto_dismiss = True
        self.title = title
        self.campo = MDTextField(hint_text=ayuda, size_hint_x=None, width="350")
        self.mensaje_capturado = ""
        self.botonCancelar = MDRoundFlatButton(text="Cancelar", on_release=self.cancelar)
        self.botonAceptar = MDRoundFlatButton(text="Aceptar", on_release=self.cancelar)
        if aceptar is not None:
            self.botonAceptar.bind(on_release=aceptar)

        self.buttons = [self.botonCancelar, self.botonAceptar]

        super().__init__(**kargs)
        self.add_widget(self.campo)

    def cancelar(self, *args):
        self.dismiss()


class Notificacion(MDDialog):

    def __init__(self, titulo, mensaje, funcion_concurrente=None, **kwargs):
        self.title = titulo
        self.text = mensaje
        self.auto_dismiss = True
        self.aceptar = MDRoundFlatButton(text="Aceptar", on_release=self.salir)
        self.cancelar = MDRoundFlatButton(text="Cancelar", on_release=self.salir)
        self.buttons = [self.aceptar, self.cancelar]

        if funcion_concurrente is not None:
            self.aceptar.bind(on_release=funcion_concurrente)

        super().__init__(**kwargs)

    def salir(self, *Arg):
        self.dismiss()


class InformacionPersona(MDDialog):
    def __init__(self, network, titulo, rut, **kwargs):
        self.title = titulo
        self.network = network
        self.rut_principal = rut

        self.contenedor_principal = MDBoxLayout(padding=dp(15))
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=[None, None],width=dp(250), height=dp(100))
        self.contenedor = MDList()

        self.scroll.add_widget(self.contenedor)
        self.contenedor_principal.add_widget(self.scroll)

        self.maqueta = None

        self.rut = MDTextField(hint_text="Rut", disabled=True)
        self.nombres = MDTextField(hint_text="Nombres")
        self.apellidos = MDTextField(hint_text="Nombres")
        self.telefono = MDTextField(hint_text="Telefono")
        self.celular = MDTextField(hint_text="Celular")
        self.correo = MDTextField(hint_text="Correo")
        self.ubicacion = MDTextField(hint_text="ubicacion")
        self.cuenta = MDTextField(hint_text="Cuenta", disabled=True)
        self.contenedor.add_widget(self.rut)
        self.contenedor.add_widget(self.nombres)
        self.contenedor.add_widget(self.apellidos)
        self.contenedor.add_widget(self.telefono)
        self.contenedor.add_widget(self.celular)
        self.contenedor.add_widget(self.correo)
        self.contenedor.add_widget(self.ubicacion)
        self.contenedor.add_widget(self.cuenta)
        self.type = "custom"

        self.editar = MDRoundFlatButton(text="Editar", on_release=self.chequear)
        self.cancelar = MDRoundFlatButton(text="Cerrar", on_release=self.salir)
        self.buttons = [self.editar, self.cancelar]
        super().__init__(**kwargs)
        self.add_widget(self.contenedor_principal)



    def chequear(self, *args):
        noti = Notificacion("Error", "")
        if self.nombres.text == "":
            noti.text += "Debe Tener contenido el Nombre.\n"
        if self.apellidos.text == "":
            noti.text += "Debe Tener contenido el Apellido.\n"
        if self.celular.text == "":
            noti.text += "Debe Tener contenido el Celular.\n"
        if self.correo.text == "":
            noti.text += "Debe Tener contenido el Correo.\n"

        if len(noti.text) >= 1:
            noti.open()
            return False
        return True

    def activar(self):
        self.network.enviar({"estado": "buscar_persona_rut", "rut": self.rut_principal})
        info = self.network.recibir()
        if info.get("estado"):
            self.maqueta = RegistroPersonas()
            self.maqueta.__dict__ = info.get("datos").__dict__
            self.rut.text = self.maqueta.rut_persona
            self.nombres.text = self.maqueta.nombres
            self.apellidos.text = self.maqueta.apellidos
            self.telefono.text = self.maqueta.telefono if self.maqueta.telefono is not None else "No Asignado"
            self.celular.text = self.maqueta.celular
            self.correo.text = self.maqueta.correo
            self.ubicacion.text = self.maqueta.ubicacion if self.maqueta.ubicacion is not None else "No Asignado"
            self.cuenta.text = self.maqueta.id_cuenta
            return
        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        return

    def salir(self, *Arg):
        self.dismiss()


class MDScreenAbstrac(MDScreen):

    @abstractmethod
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(**kw)
        self.name = nombre
        self.network = network
        self.manejador = manejador
        self.nombre_siguiente = siguiente
        self.nombre_volver = volver
        self.activo = False

    @abstractmethod
    def activar(self):
        self.desactivar_ventanas()
        self.activo = True

    def desactivar_ventanas(self):
        for elementos in self.manager.screen_names:
            self.manager.get_screen(elementos).activo = False

    def __desconectar(self):
        self.manager.current = "entrada"
        self.manager.get_screen("entrada").activar()
        self.network.iniciar()

    @abstractmethod
    def actualizar(self, dt):
        if self.name != "entrada" and self.activo:
            self.network.enviar({"estado": "actualizar", "contenido": self.name})
            info = self.network.recibir()
            if not info.get("estado"):
                noti = Notificacion("Error", info.get("condicion") if info.get(
                    "condicion") is not None else "Se ha perdido Conexion del servidor")
                noti.open()
                self.__desconectar()

    @abstractmethod
    def siguiente(self, *dt):
        if self.nombre_siguiente:
            self.manager.get_screen(self.nombre_siguiente).activar()
            self.manager.current = self.nombre_siguiente

    @abstractmethod
    def volver(self):
        if self.nombre_volver:
            self.manejador.get_screen(self.nombre_volver).activar()
            self.manager.current = self.nombre_volver


class ItemCard(MDCard):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.elevation = 3
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(420)
        self.padding = dp(20)
        self.adaptative_size = True
        self.contenedor = MDList(size_hint_y=None, size=self.size)
        self.add_widget(self.contenedor)


class ItemNotaEmpresa(ItemCard):
    def __init__(self, network, objeto, **kargs):
        super().__init__(**kargs)

        self.maqueta = RegistroNotas()
        self.maqueta.__dict__ = objeto.__dict__
        self.network = network

        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint_y=None, height=dp(100))
        self.id_registro = MDTextField(hint_text="ID Registro", text=str(self.maqueta.id_registro), disabled=True,
                                       mode="fill")
        self.nota = MDTextField(hint_text="Nota", text=self.maqueta.nota, multiline=True)
        self.rut_empresa = MDTextField(hint_text="Rut Empresa:", text=self.maqueta.rut_asociado, disabled=True)
        self.correo = MDTextField(hint_text="Usuario", text=self.maqueta.id_cuenta, disabled=True)
        self.fecha_creacion = MDTextField(hint_text="Fecha Creación", text=str(self.maqueta.fecha_creacion),
                                          disabled=True)
        self.editar = MDRoundFlatButton(text="Editar", on_release=self.editar_nota)

        self.contenedor.add_widget(self.id_registro)
        self.scroll.add_widget(self.nota)
        self.contenedor.add_widget(self.scroll)
        self.contenedor.add_widget(self.rut_empresa)
        self.contenedor.add_widget(self.correo)
        self.contenedor.add_widget(self.fecha_creacion)
        self.contenedor.add_widget(self.editar)

    def editar_nota(self, *args):
        if self.maqueta.nota == self.nota.text:
            noti = Notificacion("Error", "No ha cambiado nada en la nota como para poder editarla")
            noti.open()
            return

        self.network.enviar({"estado": "editar_nota", "nota": self.nota.text,
                             "id": self.maqueta.id_registro})
        info = self.network.recibir()

        if info.get("estado"):
            noti = Notificacion("Exito", "Se ha editado con exito!")
            noti.open()
            return

        noti = Notificacion("Error", info.get("condicion"))
        noti.open()
        return
