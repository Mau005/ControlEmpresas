from threading import Thread
from core.constantes import TAMANIO_PAQUETE, ERRORPRIVILEGIOS, TIMEPOESPERAUSUARIO
from core.herramientas import Herramientas as her
from entidades.registrarlocales import RegistrarLocales
from entidades.registro_notas_empresas import Registro_Notas_Empresas
from entidades.registrotrabajador import RegistroTrabajador
from network.recuperacion_cuenta import RecuperacionCuenta
from entidades.registrousaurios import RegistroUsuarios
from servicios_correos.base_correos import Base_Correos


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
        self.base_correo = Base_Correos(servicio_correos)
        self.recuperacion_cuenta = RecuperacionCuenta(servicio_correos, self.control_network)

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
            return {"estado": "cierre_abrupto"}

        if datos != b'':
            return her.desenpaquetar(datos)
        return {"estado": "cierre_abrupto"}

    def run(self):
        while self.enfuncionamiento:
            datos = self.recibir()
            if not datos.get("estado") == "actualizar":
                print(f"Recibo de datos del servidor: {datos}")

            if datos.get("estado") == "saludo":
                self.saludo()

            if datos.get("estado") == "actualizar":
                self.actualizar_ventanas(datos.get("contenido"))

            if datos.get("estado") == "login":
                self.login(datos)
            if datos.get("estado") == "desconectar":
                print("se ha desconectado el usuario")
                self.desconectar()

            if datos.get("estado") == "recuperacion":
                self.inciar_recuperacion(datos.get("contenido"))

            if datos.get("estado") == "recuperacion_digito":
                self.recuperacion_digito(datos.get("contenido"))

            if datos.get("estado") == "nueva_contraseña":
                self.nueva_contraseña(datos.get("contenido"))

            if datos.get("estado") == "registro_servicio":
                self.registro_servicios(datos.get("contenido"))

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

            if datos.get("estado") == "listadoproductos":
                self.listado_productos()

            if datos.get("estado") == "lista_empresas":
                self.listado_empresas()

            if datos.get("estado") == "menu_estado":
                # Se procede a enviar informacion de los estados
                self.enviar(self.querys.lista_menu_estados())

            if datos.get("estado") == "menu_personas":
                self.enviar(self.querys.lista_menu_personas())

            if datos.get("estado") == "menu_locales":
                self.enviar(self.querys.lista_menu_locales())

            if datos.get("estado") == "registrartrabajador":
                self.registrar_trabajador(datos.get("contenido"))

            if datos.get("estado") == "registrarlocal":
                self.registrar_local(datos.get("contenido"))

            if datos.get("estado") == "menu_trabajadores":
                self.enviar(self.querys.lista_menu_trabajadores())

            if datos.get("estado") == "menu_productos":
                self.enviar(self.querys.lista_menu_productos())

            if datos.get("estado") == "menu_empresas":
                self.enviar(self.querys.lista_menu_empresas())

            if datos.get("estado") == "registro_servicio_diario":
                self.registro_servicio_diario(datos.get("contenido"))

            if datos.get("estado") == "listado_notas_empresa_especifica":
                self.enviar(self.querys.listado_notas_empresa_especifica(datos.get("contenido")))

            if datos.get("estado") == "registrar_grupo":
                self.enviar(self.querys.registrar_grupos(datos.get("contenido")))

            if datos.get("estado") == "cierre_abrupto":
                print(f"Se Desconecta usuario: {self.usuario.correo}")
                self.control_network.pendientes_desconexion.append(self.usuario.correo)
                break
            #else:
            #    self.enviar({"estado": False, "condicion": "datos"})

        self.cerrar()

    def registro_servicio_diario(self, contenido):
        info = self.querys.registrar_servicio_diario(contenido)
        if info.get("estado"):
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "REGISTRO"})

    def registrar_local(self, contenido):
        objeto = RegistrarLocales()
        objeto.__dict__ = contenido.__dict__

        if self.consultar_privilegios("RegistrarLocales"):
            info = self.querys.registrar_locales(objeto.nombre_local, objeto.telefono_local, objeto.direccion)

            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def registrar_trabajador(self, contenido):
        objeto = RegistroTrabajador()
        objeto.__dict__ = contenido.__dict__
        if self.grupos.get(str(self.usuario.grupos)).get("RegistrarTrabajadores"):
            info = self.querys.registrar_trabajador(objeto.rut, objeto.id_local, objeto.sueldo, objeto.dia_pago)
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def listado_empresas(self):
        if self.grupos.get(str(self.usuario.grupos)).get("VerEmpresas"):
            return self.enviar(self.querys.lista_empresas())
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def listado_productos(self):
        if self.grupos.get(str(self.usuario.grupos)).get("VerProductos"):
            return self.enviar(self.querys.solicitar_lista_productos())
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def desconectar(self):
        self.control_network.hilos_cliente.pop(self.usuario.correo)
        self.usuario = RegistroUsuarios()

    def inciar_recuperacion(self, contenido):
        info = self.querys.existe_usuario(contenido)
        if info.get("estado"):
            self.recuperacion_cuenta.iniciar(info.get("datos")[0])

        self.enviar({"estado": True, "condicion": "Se ha enviado un correo electronico."})

    def recuperacion_digito(self, contenido):
        condicion = self.control_network.comprobar_control_recuperacion(self.usuario.correo, contenido)

        if condicion:
            self.enviar({"estado": True, "condicion": "desde recuperacion_digito"})
        else:
            self.enviar({"estado": False, "condicion": "desde recuperacion_digito"})

    def nueva_contraseña(self, contraseña_nueva):
        info = self.querys.nueva_contraseña(self.usuario.correo, contraseña_nueva)
        if info.get("estado"):
            self.enviar({"estado": True})
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

    def registro_notas_empresas(self, contenido):
        if self.consultar_privilegios("CrearNotaEmpresa"):
            notas = Registro_Notas_Empresas()
            notas.__dict__ = contenido.__dict__
            datos = self.querys.registrar_notas_empresas(notas.notas, notas.rut_empresa,
                                                         self.usuario.correo,
                                                         )
            return self.enviar(datos)
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def login(self, datos):
        self.usuario = RegistroUsuarios()
        self.usuario.correo = datos.get("correo")
        self.usuario.contraseña = datos.get("password")

        if self.control_network.buscar_control_recuperacion(self.usuario.correo):
            return self.enviar({"estado": False, "condicion": "recuperacion"})

        if self.control_network.comprobar_control_hilos(self.usuario.correo):
            self.desconectar()
            return self.enviar({"estado": False, "condicion": "usuarioactivo"})

        datosnuevos = self.querys.consultar_usuario(self.usuario.correo, self.usuario.contraseña)

        if datosnuevos.get("estado"):
            self.intentos = 0
            self.usuario = RegistroUsuarios(correo=datosnuevos["datos"][0], contraseña=datosnuevos["datos"][1],
                                            fecha_creacion=datosnuevos["datos"][2],
                                            estado_usuario=datosnuevos["datos"][3], grupos=datosnuevos["datos"][4])
            datosnuevos.update({"MOTD": self.info["Servidor"]["MOTD"], "condicion": "iniciando"})
            self.control_network.agregar_hilo(self)

            return self.enviar(datosnuevos)
        else:
            self.usuario = RegistroUsuarios()
            return self.enviar({"estado": False, "condicion": "contraseñas"})

    def registrar_persona(self, datos):
        datos_procesados = self.querys.registrar_personas(datos.rut_persona, datos.nombres, datos.apellidos,
                                                          datos.telefono,
                                                          datos.celular, datos.correo.lower(), datos.rut_empresa)

        if datos_procesados.get("estado"):
            self.base_correo.Correo_Bienvenida(datos.nombres, datos.correo.lower(), "12345")

        return self.enviar(datos_procesados)

    def registro_servicios(self, datos):
        if self.consultar_privilegios("CrearServicios"):
            return self.enviar(self.querys.registrar_servicios(datos))
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def registroempresas(self, empresa):
        if self.consultar_privilegios("CrearEmpresas"):
            estado = self.querys.registrar_empresas(empresa)
            self.enviar(estado)
        else:
            self.enviar({"estado": False, "condicion": ERRORPRIVILEGIOS})

    def saludo(self):
        self.enviar({"estado": "saludo", "contenido": "Mensaje desde el servidor FDP"})

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

    def consultar_privilegios(self, consulta):
        return self.grupos.get(str(self.usuario.grupos)).get(consulta)


