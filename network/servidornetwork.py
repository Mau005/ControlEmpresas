from threading import Thread
from core.constantes import TAMANIO_PAQUETE, TIMEPOESPERAUSUARIO
from core.herramientas import Herramientas as her
from entidades.registronotas import RegistroNotas
from entidades.registrocuentas import RegistroCuentas
from entidades.registrotrabajador import RegistroTrabajador
from network.recuperacion_cuenta import RecuperacionCuenta
from entidades.registrousaurios import RegistroUsuarios
from servicios_correos.base_correos import Base_Correos


class ServidorNetwork(Thread):

    def __init__(self, cliente, direccion, querys, info, grupos, control_network, servicio_correos):
        Thread.__init__(self)
        self.__variable_usuarios()
        self.cuenta = RegistroCuentas()
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

    def login(self, datos):
        self.cuenta = RegistroCuentas()
        self.cuenta.__dict__ = datos.__dict__
        # se suspende el sistema de recuperacion de cuenta
        # if self.control_network.buscar_control_recuperacion(self.usuario.nombre_cuenta):
        #    return self.enviar({"estado": False, "condicion": "RECUPERACION"})

        if self.control_network.comprobar_control_hilos(self.cuenta.nombre_cuenta):
            self.desconectar()
            return self.enviar({"estado": False, "condicion": "USUARIOACTIVO"})

        info = self.querys.consultar_cuenta(self.cuenta.nombre_cuenta, self.cuenta.contraseña)
        print(f"Info vale esto: {info}")
        if info.get("estado"):
            self.intentos = 0
            self.cuenta = RegistroCuentas(id_cuenta=info["datos"][0],
                                          nombre_cuenta=info["datos"][1],
                                          contraseña=info["datos"][2],
                                          fecha_creacion=info["datos"][3],
                                          acceso=info["datos"][4],
                                          serializacion=her.generar_numero_unico())

            info.update({"MOTD": self.info["Servidor"]["MOTD"], "condicion": "iniciando"})
            self.control_network.agregar_hilo(self)

            return self.enviar(info)
        self.cuenta = RegistroCuentas()
        return self.enviar({"estado": False, "condicion": "CONTRASEÑAS"})

    def registrar_local(self, contenido):
        if self.consultar_privilegios("RegistrarLocales"):
            info = self.querys.registrar_locales(contenido)
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def desconectar(self):
        self.control_network.hilos_cliente.pop(self.cuenta.nombre_cuenta)
        self.cuenta = RegistroUsuarios()

    def registrar_empresas(self, empresa):
        if self.consultar_privilegios("CrearEmpresas"):
            estado = self.querys.registrar_empresas(empresa)
            self.enviar(estado)
        else:
            self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def registrar_productos(self, datos):
        if self.consultar_privilegios("CrearProductos"):
            datos = self.querys.registrar_productos(datos)
            self.enviar(datos)
        else:
            self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def run(self):
        while self.enfuncionamiento:
            datos = self.recibir()
            if not datos.get("estado") == "actualizar":
                print(f"Recibo de datos del servidor: {datos}")

            if datos.get("estado") == "saludo":
                self.saludo()

            if datos.get("estado") == "actualizar":
                self.actualizar_ventanas(datos.get("contenido"))

            if datos.get("estado") == "login":  # methodo actualizado
                self.login(datos.get("contenido"))

            if datos.get("estado") == "registrar_local":
                self.registrar_local(datos.get("contenido"))

            if datos.get("estado") == "desconectar":
                self.desconectar()

            if datos.get("estado") == "recuperacion":  # no se esta utilizando
                self.inciar_recuperacion(datos.get("contenido"))

            if datos.get("estado") == "recuperacion_digito":
                self.recuperacion_digito(datos.get("contenido"))

            if datos.get("estado") == "nueva_contraseña":  # no se esta utilizando
                self.nueva_contraseña(datos.get("contenido"))

            if datos.get("estado") == "registro_empresa":
                self.registrar_empresas(datos.get("contenido"))

            if datos.get("estado") == "registro_productos":
                self.registrar_productos(datos.get("contenido"))

            if datos.get("estado") == "lista_empresas":
                self.listado_empresas()

            if datos.get("estado") == "registrar_departamento":
                self.enviar(self.querys.registrar_departamento(datos.get("contenido")))

            if datos.get("estado") == "menu_locales":
                self.enviar(self.querys.lista_menu_locales())

            if datos.get("estado") == "menu_productos":
                self.enviar(self.querys.lista_menu_productos())


            if datos.get("estado") == "registro_notas_empresas":
                self.registro_notas_empresas(datos.get("contenido"))

            if datos.get("estado") == "registro_servicio":
                self.registro_servicios(datos.get("contenido"))

            if datos.get("estado") == "registro_notas_personas":
                self.registro_notas_personas(datos.get("contenido"))

            if datos.get("estado") == "registrar_persona":
                self.registrar_persona(datos.get("contenido"))

            if datos.get("estado") == "listadoservicios":
                self.listado_servicios()

            if datos.get("estado") == "listadoproductos":
                self.listado_productos()

            if datos.get("estado") == "menu_estado":
                # Se procede a enviar informacion de los estados
                self.enviar(self.querys.lista_menu_estados())

            if datos.get("estado") == "menu_personas":
                self.enviar(self.querys.lista_menu_personas())

            if datos.get("estado") == "registrartrabajador":
                self.registrar_trabajador(datos.get("contenido"))

            if datos.get("estado") == "menu_trabajadores":
                self.enviar(self.querys.lista_menu_trabajadores())

            if datos.get("estado") == "menu_empresas":
                self.enviar(self.querys.lista_menu_empresas())

            if datos.get("estado") == "registro_servicio_diario":
                self.registro_servicio_diario(datos.get("contenido"))

            if datos.get("estado") == "listado_notas_empresa_especifica":
                self.enviar(self.querys.listado_notas_empresa_especifica(datos.get("contenido")))

            if datos.get("estado") == "cierre_abrupto":
                print(f"Se Desconecta usuario: {self.cuenta.nombre_cuenta}")
                self.control_network.pendientes_desconexion.append(self.cuenta.nombre_cuenta)
                break
            # else:
            #    self.enviar({"estado": False, "condicion": "datos"})

        self.cerrar()

    def registro_servicio_diario(self, contenido):
        info = self.querys.registrar_servicio_diario(contenido)
        if info.get("estado"):
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "REGISTRO"})

    def registrar_trabajador(self, contenido):
        objeto = RegistroTrabajador()
        objeto.__dict__ = contenido.__dict__
        if self.grupos.get(str(self.cuenta.grupos)).get("RegistrarTrabajadores"):
            info = self.querys.registrar_trabajador(objeto.rut, objeto.id_local, objeto.sueldo, objeto.dia_pago)
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def listado_empresas(self):
        if self.consultar_privilegios("VerEmpresas"):
            return self.enviar(self.querys.lista_empresas())
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def listado_productos(self):
        if self.consultar_privilegios("VerProductos"):
            return self.enviar(self.querys.solicitar_lista_productos())
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def inciar_recuperacion(self, contenido):
        info = self.querys.existe_cuenta(contenido)
        if info.get("estado"):
            self.recuperacion_cuenta.iniciar(info.get("datos")[0])

        self.enviar({"estado": True, "condicion": "Se ha enviado un correo electronico."})

    def recuperacion_digito(self, contenido):
        condicion = self.control_network.comprobar_control_recuperacion(self.cuenta.correo, contenido)

        if condicion:
            self.enviar({"estado": True, "condicion": "desde recuperacion_digito"})
        else:
            self.enviar({"estado": False, "condicion": "desde recuperacion_digito"})

    def nueva_contraseña(self, contraseña_nueva):
        info = self.querys.nueva_contraseña(self.cuenta.correo, contraseña_nueva)
        if info.get("estado"):
            self.enviar({"estado": True})
        else:
            self.enviar({"estado": False})

    def cerrar(self):
        self.cliente.close()

    def listado_servicios(self):
        datos = self.querys.solicitar_listado_servicios()
        self.enviar(datos)

    def registro_notas_empresas(self, contenido):
        if self.consultar_privilegios("CrearNotaEmpresa"):
            return self.enviar(self.querys.registrar_notas(contenido, self.cuenta, objetivo="empresas"))
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def registro_notas_personas(self, contenido):
        if self.consultar_privilegios("CrearNotaPersona"):
            return self.enviar(self.querys.registrar_notas(contenido, self.cuenta, objetivo="personas"))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def registrar_persona(self, datos):
        if self.consultar_privilegios("CrearPersona"):
            return self.enviar(self.querys.registrar_personas(datos))
            # if info.get("estado"): se suspende el envio de correos electornicos
            #    self.base_correo.Correo_Bienvenida(datos.nombres, datos.correo, "12345")
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def registro_servicios(self, datos):
        if self.consultar_privilegios("CrearServicios"):
            return self.enviar(self.querys.registrar_servicios(datos))
        return self.enviar({"estado": False, "condicion": "privilegios"})

    def saludo(self):
        self.enviar({"estado": "saludo", "contenido": "Mensaje desde el servidor FDP"})

    def actualizar_ventanas(self, contenido):
        if self.tiempo_actividad >= TIMEPOESPERAUSUARIO:
            self.enviar({"estado": False, "contenido": "Se ha expirado el tiempo de seccion activa."})
            self.control_network.agregar_pendiente_hilos(self.cuenta.nombre_cuenta)
        if self.ventana_actual == contenido:
            self.enviar({"estado": True})
        else:
            self.ventana_actual = contenido
            self.tiempo_actividad = 0
            self.enviar({"estado": True})

    def consultar_privilegios(self, consulta):
        return self.grupos.get(str(self.cuenta.acceso)).get(consulta)
