from threading import Thread
from core.herramientas import Herramientas as her
from entidades.cuentas import Cuentas
from entidades.registroempresas import RegistroEmpresas
from entidades.personas import Personas
from network.recuperacion_cuenta import RecuperacionCuenta
from entidades.registrousaurios import RegistroUsuarios
from servicios_correos.base_correos import Base_Correos


class ServidorNetwork(Thread):

    def __init__(self, cliente, direccion, querys, info, grupos, control_network, servicio_correos):
        Thread.__init__(self)
        self.__variable_usuarios()
        self.cuenta = Cuentas()
        self.persona = Personas()
        self.trabajador = None
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
            self.recuperacion_cuenta.actuaactualizar()

    def enviar(self, datos):
        return self.cliente.send(her.empaquetar(datos))

    def recibir(self):
        try:
            datos = self.cliente.recv(self.info["Servidor"]["paquetes"])
        except ConnectionResetError:
            return {"estado": "cierre_abrupto"}

        if datos != b'':
            paquete = her.desenpaquetar(datos)
            return paquete
        return {"estado": "cierre_abrupto"}

    def login(self, datos):
        self.cuenta = Cuentas()
        self.cuenta.__dict__ = datos.__dict__
        # se suspende el sistema de recuperacion de cuenta
        # if self.control_network.buscar_control_recuperacion(self.usuario.nombre_cuenta):
        #    return self.enviar({"estado": False, "condicion": "RECUPERACION"})

        if self.control_network.comprobar_control_hilos(self.cuenta.nombre_cuenta):
            self.desconectar()
            return self.enviar({"estado": False, "condicion": "USUARIOACTIVO"})

        info = self.querys.consultar_cuenta(self.cuenta.nombre_cuenta, self.cuenta.contraseña)
        if info.get("estado"):
            self.intentos = 0
            self.cuenta = Cuentas(rut_persona=info["datos"][0],
                                  nombre_cuenta=info["datos"][1],
                                  contraseña=info["datos"][2],
                                  fecha_creacion=info["datos"][3],
                                  acceso=info["datos"][4],
                                  serializacion=her.generar_numero_unico())
            # pe.rut_persona, pe.nombres, pe.apellidos, pe.telefono, pe.celular, pe.correo
            persona_temp = self.querys.buscar_persona_rut_persona(self.cuenta)
            if persona_temp.get("estado"):
                self.persona = Personas(
                    rut_persona=persona_temp["datos"][0],
                    nombres=persona_temp["datos"][1],
                    apellidos=persona_temp["datos"][2],
                    telefono=persona_temp["datos"][3],
                    celular=persona_temp["datos"][4],
                    correo=persona_temp["datos"][5],
                    ubicacion=persona_temp["datos"][6]
                )
                self.trabajador = self.querys.buscar_trabajador_rut(self.persona.rut_persona)
            info.update({"MOTD": self.info["Servidor"]["MOTD"], "condicion": "iniciando"})
            self.control_network.agregar_hilo(self)
            return self.enviar(info)
        self.cuenta = Cuentas()
        return self.enviar({"estado": False, "condicion": "CONTRASEÑAS"})

    def registrar_local(self, contenido):
        if self.consultar_privilegios("RegistrarLocales"):
            info = self.querys.registrar_locales(contenido)
            return self.enviar(info)
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def desconectar(self):
        self.control_network.hilos_cliente.pop(self.cuenta.nombre_cuenta)
        self.cuenta = RegistroUsuarios()
        self.persona = Personas()

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

    def registrar_servicio_mensual(self, contenido):
        if self.consultar_privilegios("CrearServicioMensual"):
            return self.enviar(self.querys.registrar_servicio_mensual(contenido.get("contenido"),contenido.get("productos")))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def actualizar_cambios(self):
        self.tiempo_actividad = 0

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
                self.actualizar_cambios()

            if datos.get("estado") == "servicio_mensual":
                self.registrar_servicio_mensual(datos)
                self.actualizar_cambios()

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
                self.actualizar_cambios()

            if datos.get("estado") == "registro_productos":
                self.registrar_productos(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "lista_empresas":
                self.listado_empresas()

            if datos.get("estado") == "registrar_departamento":
                self.enviar(self.querys.registrar_departamento(datos.get("contenido")))
                self.actualizar_cambios()

            if datos.get("estado") == "menu_locales":
                self.enviar(self.querys.lista_menu_locales())

            if datos.get("estado") == "menu_productos":
                self.enviar(self.querys.lista_menu_productos())

            if datos.get("estado") == "menu_departamentos":
                self.enviar(self.querys.lista_menu_departamentos())

            if datos.get("estado") == "menu_estado_gastos":
                self.enviar(self.querys.lista_menu_estado_gastos())

            if datos.get("estado") == "registro_notas_empresas":
                self.registro_notas_empresas(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "registrar_gasto":
                if self.consultar_privilegios("CrearGastos"):
                    self.enviar(self.querys.registrar_gasto(datos.get("contenido"), self.cuenta))
                    self.actualizar_cambios()
                else:
                    self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

            if datos.get("estado") == "listado_gastos_fechas":
                self.listado_gastos_fechas(datos)

            if datos.get("estado") == "registro_servicio":
                self.registro_servicios(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "registro_notas_personas":
                self.registro_notas_personas(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "registrar_persona":
                self.registrar_persona(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "listadoservicios":
                self.listado_servicios()

            if datos.get("estado") == "listadoproductos":
                self.listado_productos()

            if datos.get("estado") == "menu_estado":
                # Se procede a enviar informacion de los estados
                self.enviar(self.querys.lista_menu_estados())

            if datos.get("estado") == "menu_personas":
                self.enviar(self.querys.lista_menu_personas())

            if datos.get("estado") == "registrar_trabajador":
                self.registrar_trabajador(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "menu_trabajadores":
                self.enviar(self.querys.lista_menu_trabajadores())

            if datos.get("estado") == "menu_empresas":
                self.enviar(self.querys.lista_menu_empresas())

            if datos.get("estado") == "registro_servicio_diario":
                self.registro_servicio_diario(datos)
                self.actualizar_cambios()

            if datos.get("estado") == "mis servicios":
                self.enviar(self.querys.mis_servicios(self.persona))

            if datos.get("estado") == "listado_notas_empresa_especifica":
                self.enviar(self.querys.listado_notas_empresa_especifica(datos.get("contenido")))

            if datos.get("estado") == "listado_notas_persona_especifica":
                self.enviar(self.querys.listado_notas_persona_especifica(datos.get("contenido")))

            if datos.get("estado") == "editar_nota":
                self.actualizar_nota(datos)
                self.actualizar_cambios()

            if datos.get("estado") == "buscar_persona_rut":
                self.enviar(self.querys.buscar_persona_rut(datos))

            if datos.get("estado") == "buscar_empresa_rut":
                self.buscar_empresa_rut(datos.get("contenido"))

            if datos.get("estado") == "editar_empresa":
                self.editar_empresa(datos.get("contenido"))
                self.actualizar_cambios()

            if datos.get("estado") == "lista_personas":
                self.enviar(self.querys.lista_personas())

            if datos.get("estado") == "mis trabajos":
                self.enviar(self.querys.buscar_servicios(self.trabajador))

            if datos.get("estado") == "cierre_abrupto":
                print(f"Se Desconecta usuario: {self.cuenta.nombre_cuenta}")
                self.control_network.pendientes_desconexion.append(self.cuenta.nombre_cuenta)
                break
            # else:
            #    self.enviar({"estado": False, "condicion": "datos"})

        self.cerrar()

    def buscar_empresa_rut(self, rut: str):
        if self.consultar_privilegios("BuscarEmpresa"):
            return self.enviar(self.querys.buscar_empresa_rut(rut))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def editar_empresa(self, empresa: RegistroEmpresas):
        if self.consultar_privilegios("EditarEmpresa"):
            return self.enviar(self.querys.editar_empresa(empresa))
        return self.enviar({"estado": False, "condicion": "PRIVIELGIOS"})

    def actualizar_nota(self, datos):
        if self.consultar_privilegios("EditarNotas"):
            return self.enviar(self.querys.actualizar_nota(datos))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def registro_servicio_diario(self, contenido):
        if self.consultar_privilegios("CrearServicioMensual"):
            return self.enviar(self.querys.registrar_servicio_diario(contenido))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def listado_gastos_fechas(self, contenido):
        if self.consultar_privilegios("ConsultarGastos"):
            return self.enviar(self.querys.listado_gastos_fechas(contenido))
        return self.enviar({"estado": False, "condicion": "PRIVILEGIOS"})

    def registrar_trabajador(self, contenido):
        if self.consultar_privilegios("RegistrarTrabajadores"):
            return self.enviar(self.querys.registrar_trabajador(contenido))
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
        if self.tiempo_actividad >= 60 * self.info["Servidor"]["TIMEPOESPERAUSUARIO"]:
            self.enviar({"estado": False, "condicion": "EXPIRACION"})
            self.control_network.agregar_pendiente_hilos(self.cuenta.nombre_cuenta)
        if self.ventana_actual == contenido:
            self.enviar({"estado": True})
        else:
            self.ventana_actual = contenido
            self.tiempo_actividad = 0
            self.enviar({"estado": True})

    def consultar_privilegios(self, consulta):
        consulta = self.grupos.get(str(self.cuenta.acceso)).get(consulta)
        if consulta is not None or "TodoPoderoso":
            return True
        return False
