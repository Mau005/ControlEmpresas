from threading import Thread
from core.constantes import TAMANIO_PAQUETE, ERRORPRIVILEGIOS
from core.herramientas import Herramientas as her

from entidades.registrousaurios import RegistroUsuarios


class ServidorNetwork(Thread):

    def __init__(self, cliente, direccion, querys, info, grupos, control_network):
        Thread.__init__(self)
        self.cliente = cliente
        self.direccion = direccion
        self.querys = querys
        self.intentos = 0
        self.info = info
        self.tiempo_actividad = 0
        self.usuario = RegistroUsuarios()
        self.grupos = grupos
        self.control_network = control_network

    def actualizar(self, dt):
        print("se ejecuta actualzar? ", dt)
        pass

    def enviar(self, datos):
        return self.cliente.send(her.empaquetar(datos))

    def recibir(self):
        datos = self.cliente.recv(TAMANIO_PAQUETE)

        if datos != b'':
            return her.desenpaquetar(datos)
        return {"estado": "cierreAbrupto"}

    def run(self):
        while True:
            datos = self.recibir()
            if datos.get("estado") == "saludo":
                self.saludo()

            if datos.get("estado") == "login":
                self.login(datos)

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

        self.enviar(datos)

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
        correo = datos.get("correo")
        passw = datos.get("password")
        datosnuevos = self.querys.consultar_usuario(correo, passw)
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
            self.intentos += 1
            if self.intentos >= 3:
                self.enviar({"estado": False, "condicion": "Intentos completados procedaras a ser baneado FDP"})
                self.cliente.close()
                print(f"Intentos: {self.intentos}")

        self.enviar(datosnuevos)

    def registrar_persona(self, datos):
        datos = self.querys.registrar_usuarios(datos.rut_persona, datos.nombres, datos.apellidos, datos.telefono,
                                               datos.celular, datos.correo)

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
