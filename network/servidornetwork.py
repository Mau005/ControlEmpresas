from threading import Thread
from core.constantes import TAMANIO_PAQUETE, ERRORPRIVILEGIOS, TIMEPOESPERAUSUARIO, TIEMPOESPERADIGITO
from core.herramientas import Herramientas as her
from network.recuperacion_cuenta import RecuperacionCuenta

from entidades.registrousaurios import RegistroUsuarios


class ServidorNetwork(Thread):

    def __init__(self, cliente, direccion, querys, info, grupos, control_network, servicio_correos):
        Thread.__init__(self)
        self.__variable_usuarios()
        self.cliente = cliente
        self.direccion = direccion
        self.querys = querys
        self.info = info
        self.grupos = grupos
        self.control_network = control_network
        self.servicio_correos = servicio_correos
        self.recuperacion_cuenta = RecuperacionCuenta(self.servicio_correos,self.control_network)
    def __variable_usuarios(self):
        self.ventana_actual = "entrada"
        self.intentos = 0
        self.tiempo_actividad = 0
        self.enfuncionamiento = True
        self.usuario = RegistroUsuarios()

    def actualizar(self):
        if self.ventana_actual != "entrada":
            self.tiempo_actividad += 1

        if self.recuperacion_cuenta.activo:
            self.recuperacion_cuenta.actualizar()

    def enviar(self, datos):
        return self.cliente.send(her.empaquetar(datos))

    def recibir(self):
        try:
            datos = self.cliente.recv(TAMANIO_PAQUETE)
        except ConnectionResetError:
            return None

        if datos != b'':
            return her.desenpaquetar(datos)
        return {"estado": "cierreAbrupto"}


    def run(self):
        while self.enfuncionamiento:
            datos = self.recibir()
            if datos.get("estado") == "saludo":
                self.saludo()

            if datos.get("estado") == "actualizar":
                self.actualizar_ventanas(datos.get("contenido"))

            if datos.get("estado") == "login":
                self.login(datos)

            if datos.get("estado") == "recuperacion":
                self.inciar_recuperacion(datos.get("contenido"))

            if datos.get("estado") == "recuperacion_digito":
                self.recuperacion_digito(datos.get("contenido"))

            if datos.get("estado") == "nueva_contraseña":
                self.nueva_contraseña(datos.get("contenido"))

            if datos.get("estado") == "registroservicio":
                self.registro_servicios(datos)

            if datos.get("estado") == "registroempresa":
                self.registroempresas(datos.get("contenido"))

            if datos.get("estado") == "registro_notas_empresas":
                self.registro_notas_empresas(datos.get("contenido"))

            if datos.get("estado") == "listaEmpresas":
                self.lista_empresa()

            if datos.get("estado") == "registropersona":
                self.registrar_persona(datos.get("contenido"))

            if datos.get("estado") == "listadoservicios":
                self.listado_servicios()

            if datos.get("estado") == "registroproductos":
                self.registrar_productos(datos.get("contenido"))

            if datos.get("estado") == "salir":
                print("el usuario intenta salir")
                pass

            elif datos.get("estado") == "cierreAbrupto":
                print(
                    "Cliente se ha desconectado de forma anormal, por que nos abe que el ctm tiene que colocar salir seccion")
                break
        self.cerrar()

    def inciar_recuperacion(self, contenido):
        info = self.querys.existe_usuario(contenido)
        if info.get("estado"):
            self.recuperacion_cuenta.iniciar(info.get("datos")[0])

        self.enviar({"estado":True, "condicion": "Se ha enviado un correo electronico."})
    def recuperacion_digito(self, contenido):
        condicion = self.control_network.comprobar_control_recuperacion(self.usuario.correo, contenido)

        print(f"COndicion de recuperacion despues de la comprobacion : {condicion}")
        if condicion:
            self.enviar({"estado":True, "condicion":"desde recuperacion_digito"})
        else:
            self.enviar({"estado":False, "condicion":"desde recuperacion_digito"})
    def nueva_contraseña(self, contraseña_nueva):
        print(f"Se intenta cambia la contraseña nueva: {contraseña_nueva}")
        info = self.querys.nueva_contraseña(self.usuario.correo, contraseña_nueva)
        print(f"informacion recupilada por el cambio de contraseña {info}")
        if info.get("estado"):
            self.enviar({"estado":True})
        else:
            self.enviar({"estado": False})
    def cerrar(self):
        self.cliente.close()

    def registrar_productos(self, datos):
        if self.grupos.get(str(self.usuario.grupos)).get("CrearProductos"):
            datos = self.querys.registrar_productos(datos.nombre_producto, datos.descripcion, datos.cantidad)
            self.enviar(datos)
        else:
            self.enviar({"estado": False, "condicion": ERRORPRIVILEGIOS})

    def listado_servicios(self):
        datos = self.querys.solicitar_listado_servicios()
        self.enviar(datos)

    def lista_empresa(self):
        datos = self.querys.solicitar_lista_empresas()
        self.enviar(datos)

    def registro_notas_empresas(self, notas):
        self.querys.registrar_notas_empresas(notas.notas, notas.rut_empresa, self.usuario.correo, )

    def login(self, datos):
        self.usuario = RegistroUsuarios()
        self.usuario.correo = datos.get("correo")
        self.usuario.contraseña = datos.get("password")

        datosnuevos = self.querys.consultar_usuario(self.usuario.correo, self.usuario.contraseña)
        datosnuevos.update({"MOTD": self.info["Servidor"]["MOTD"]})

        if datosnuevos.get("estado"):
            self.intentos = 0
            self.usuario = RegistroUsuarios(correo=datosnuevos["datos"][0], contraseña=datosnuevos["datos"][1],
                                            fecha_creacion=datosnuevos["datos"][2],
                                            estado_usuario=datosnuevos["datos"][3], grupos=datosnuevos["datos"][4])
            estado = self.control_network.agregar_hilo(self)
            if not estado:
                datosnuevos.update(
                    {"estado": False, "condicion": "Usuario ya ha iniciado seccion espere unos momentos"})
                self.usuario = RegistroUsuarios()
        else:
            if self.control_network.buscar_control_recuperacion(self.usuario.correo):
                self.enviar({"estado": False, "condicion":"recuperacion"})
                return None

            self.intentos += 1
            if self.intentos >= 3:
                self.enviar({"estado": False, "condicion": "Intentos completados procedaras a ser baneado FDP"})
                self.cliente.close()
                return None
                print(f"Intentos: {self.intentos}")

        self.enviar(datosnuevos)

    def registrar_persona(self, datos):
        datos = self.querys.registrar_usuarios(datos.rut_persona, datos.nombres, datos.apellidos, datos.telefono,
                                               datos.celular, datos.correo_sistema)

    def registro_servicios(self, datos):
        if self.grupos.get(str(self.usuario.grupos)).get("CrearServicios"):
            estado = self.querys.registrar_servicios(datos)
            self.enviar(estado)
        else:
            self.enviar({"estado": False, "condicion": ERRORPRIVILEGIOS})

    def registroempresas(self, empresa):
        if self.grupos.get(str(self.usuario.grupos)).get("CrearEmpresas"):
            estado = self.querys.registrar_empresas(empresa)
            self.enviar(estado)
        else:
            self.enviar({"estado": False, "condicion": ERRORPRIVILEGIOS})

    def saludo(self):
        self.enviar({"estado": "saludo", "contenido": "Hola fdp del servidor"})

    def actualizar_ventanas(self, contenido):
        if self.tiempo_actividad >= TIMEPOESPERAUSUARIO:
            self.enviar({"estado": False, "contenido": "Se ha expirado el tiempo de seccion activa."})
            self.control_network.agregar_pendiente_hilos(self.usuario.correo)
        if self.ventana_actual == contenido:
            self.enviar({"estado": True})
        else:
            self.ventana_actual = contenido
            self.tiempo_actividad = 0
            self.enviar({"estado": True})
