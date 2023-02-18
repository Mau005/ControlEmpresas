from typing import Dict

from entidades.abstracservicio import AbstracServicio
from entidades.registrargastos import RegistrarGastos
from entidades.registrarlocales import RegistrarLocales
from entidades.cuentas import Cuentas
from entidades.registronotas import RegistroNotas
from entidades.registroempresas import RegistroEmpresas
from entidades.registrardepartamento import RegistrarDepartamento
from entidades.personas import Personas
from entidades.registroproductos import RegistroProductos
from entidades.serviciodiarios import ServicioDiarios
from core.herramientas import Herramientas as her
from entidades.registrotrabajador import RegistroTrabajador
from entidades.serviciomensual import ServicioMensual
from entidades.serviciosproductos import ServiciosProductos


class Querys:

    def __init__(self, bd):
        self.bd = bd

    def existe_cuenta(self, nombre_cuenta: str):
        """
        Methodo utilizado para gestionar si existe una cuenta
        """
        querys = f'SELECT nombre_cuenta FROM cuentas WHERE nombre_cuenta = "{nombre_cuenta}";'
        return self.bd.consultar(querys)

    def existe_persona(self, rut: str):
        """
        Methodo utilizado para gestionar si existe una persona
        """
        rut = rut.replace('"', "")
        querys = f'SELECT rut_persona from personas WHERE rut_persona = "{rut}";'
        return self.bd.consultar(querys)

    def registrar_cuenta(self, cuenta: Cuentas) -> dict:
        """
        Methodo utilizado para registrar una cuenta
        """
        cuenta.__dict__ = her.recuperacion_sentencia(cuenta).__dict__
        print(f"estao de cuenta antes de registrar: {cuenta.rut_persona}")
        querys = f'INSERT INTO cuentas(rut_persona, nombre_cuenta, contraseña, acceso) ' \
                 f'VALUES({cuenta.rut_persona},{cuenta.nombre_cuenta}, SHA({cuenta.contraseña}),{cuenta.acceso});'
        print(f"Querys: {querys}")
        return self.bd.insertar(querys)

    def consultar_cuenta(self, usuario: str, contraseña: str):
        """
        Methodo Utilizado para poder gestionar si el usuario ha escrito bien sus contraseñas
        y pueda iniciar seccion
        """
        querys = f'SELECT * FROM cuentas WHERE nombre_cuenta = "{usuario}" AND contraseña = "{contraseña}";'
        datos = self.bd.consultar(querys)
        return datos

    def registrar_persona_sin_cuenta(self, persona: Personas):
        """
        Methodo usado para registrar usuarios que no necesariamente necesiten cuenta
        
        """
        persona.__dict__ = her.recuperacion_sentencia(persona).__dict__

        rut_existe = self.existe_persona(persona.rut_persona)


        if rut_existe.get("estado"):
            print(f"Rut: Existe")
            return {"estado": False, "condicion": "RUT_EXISTE"}
        querys = '''
        INSERT INTO personas(rut_persona, nombres, apellidos, telefono, celular, correo)
        VALUES({}, {}, {}, {}, {}, {}); 
        '''.format(persona.rut_persona, persona.nombres, persona.apellidos, persona.telefono,
                   persona.celular,  persona.correo)
        persona_status = self.bd.insertar(querys)
        if persona_status.get("estado"):
            self.registrar_personas_empresas(persona.rut_empresa, persona.rut_persona)
        return persona_status

    def registrar_productos(self, objeto: RegistroProductos) -> dict:
        """
        Methodo utilizado para gestionar registros de productos
        objeto es de tipo RegistroProductos()
        """
        objeto = her.recuperacion_sentencia(objeto)
        productos = RegistroProductos()
        productos.__dict__ = objeto.__dict__
        querys = '''
        INSERT INTO productos(nombre_producto, descripcion, cantidad, id_local)
        VALUES({}, {}, {}, {});
        '''.format(productos.nombre_producto, productos.descripcion, productos.cantidad, productos.id_local)
        return self.bd.insertar(querys)

    def buscar_empresa_rut(self, rut : str):
        print(f"Estado del rut en buscar empresa: {rut}")
        querys = """
        SELECT *
        FROM empresas
        WHERE rut_empresa = "{}";
        """.format(rut)
        datos = self.bd.consultar(querys)
        if datos.get("estado"):
            datos = datos.get("datos")
            empresa = RegistroEmpresas(
                rut_empresa=datos[0],
                nombre_empresa=datos[1],
                giro_empresa=datos[2],
                direccion_empresa=datos[3],
                correo_empresa=datos[4],
                correo_respaldo=datos[5],
                telefono_empresa=datos[6],
                celular_empresa=datos[7]
            )
            return {"estado": True, "datos": empresa}

        return {"estado": False, "condicion": "NOSEENCUENTRA"}

    def editar_empresa(self, empresa: RegistroEmpresas) -> dict:
        empresa = her.recuperacion_sentencia(empresa)
        querys = """
        UPDATE empresas
        SET nombre_empresa = {},
        giro_empresa = {},
        direccion_empresa = {},
        telefono_empresa = {},
        celular_empresa = {},
        correo_empresa = {},
        correo_respaldo = {}
        WHERE rut_empresa = {};
        """.format(empresa.nombre_empresa, empresa.giro_empresa, empresa.direccion_empresa,
                   empresa.telefono_empresa, empresa.celular_empresa, empresa.correo_empresa,
                   empresa.correo_respaldo, empresa.rut_empresa)
        return self.bd.insertar(querys)

    def registrar_empresas(self, empresa: RegistroEmpresas):
        """
        Methodo utilizado para gestionar registros de empresas
        objeto es tipo RegistroEmpresas()
        """
        check = self.buscar_empresa_rut(empresa.rut_empresa)
        if check.get("estado"):
            return {"estado": False, "condicion": "EMPRESA_EXISTE"}

        empresa.__dict__ = her.recuperacion_sentencia(empresa).__dict__

        querys = '''
        INSERT INTO empresas(rut_empresa, nombre_empresa, giro_empresa, direccion_empresa, correo_empresa, 
        correo_respaldo, telefono_empresa, celular_empresa)
        VALUES({}, {}, {}, {}, {}, {}, {}, {});
        '''.format(empresa.rut_empresa, empresa.nombre_empresa, empresa.giro_empresa, empresa.direccion_empresa,
                   empresa.correo_empresa,
                   empresa.correo_respaldo, empresa.telefono_empresa, empresa.celular_empresa)
        return self.bd.insertar(querys)

    def buscar_persona(self, rut):
        querys = """
        SELECT * 
        FROM personas
        WHERE rut_persona = "{}"
        """.format(rut)
        return self.bd.consultar(rut)

    def buscar_mis_rutas_id_departamento(self, cuenta):
        querys = """
        SELECT *
        FROM servicios se
        INNER JOIN servicios_mensuales seme ON seme.id_servicios = se.id_servicios
        WHERE se.id_departamento = {}
        """.format(cuenta.id_departamento)

    def buscar_persona_rut_persona(self, cuenta: Cuentas):
        """
        MEthodo para buscar rut de personas y retorna una persona completa
        """
        cuenta.__dict__ = her.recuperacion_sentencia(cuenta).__dict__
        querys = """
        SELECT pe.rut_persona, pe.nombres, pe.apellidos, pe.telefono, pe.celular, pe.correo
        FROM cuentas cu
        INNER JOIN personas pe ON pe.rut_persona = cu.rut_persona
        where cu.rut_persona = {};
        """.format(cuenta.rut_persona)
        return self.bd.consultar(querys)

    def registrar_personas_empresas(self, rut_empresa, rut_persona):
        """
        Methodo utilizado para gestionar empresas de usuarios
        este existe dado que un usuario puede participar en mas de una empresa
        """
        querys = f"INSERT INTO empresas_personas(rut_empresa, rut_persona) VALUES({rut_empresa}, {rut_persona});"
        return self.bd.insertar(querys)

    def registrar_departamento(self, objeto):
        """
        Methodo Utilizado para registrar departamentos
        """
        objeto = her.recuperacion_sentencia(objeto)
        obj = RegistrarDepartamento()
        obj.__dict__ = objeto.__dict__
        querys = """
        INSERT INTO departamentos (nombre_departamento, descripcion, id_local) 
        VALUES ({}, {}, {});
        """.format(obj.nombre_departamento, obj.descripcion, obj.id_local)
        return self.bd.insertar(querys)

    def registrar_personas(self, personas: Personas):
        """
        Methodo utilizado para que gestione la creacion de usuarios nuevos
        comprobare si el correo existe, si no existe lo creara con default de password
        TODO: Se registra usuario, y su cuenta con default, falta implementar sistema de avisos
        """

        rut_existe = self.existe_persona(personas.rut_persona)

        if rut_existe.get("estado"):
            return {"estado": False, "condicion": "RUT_EXISTE"}

        apellido_antiguo = personas.apellidos
        contador = 0
        while True:
            nombre_cuenta = her.generar_nombres(personas.nombres, personas.apellidos, contador=contador)
            info = self.existe_cuenta(nombre_cuenta)
            if info.get("datos") is None:
                personas.apellidos = apellido_antiguo
                break
            contador += 1

        personas.__dict__ = her.recuperacion_sentencia(personas).__dict__
        querys = '''
        INSERT INTO personas(rut_persona, nombres, apellidos, telefono, celular, correo)
        VALUES({}, {}, {}, {}, {}, {}); 
        '''.format(personas.rut_persona, personas.nombres, personas.apellidos, personas.telefono, personas.celular,
                   personas.correo)
        self.bd.insertar(querys)

        self.registrar_personas_empresas(personas.rut_empresa, personas.rut_persona)



        print(f"Estado de persona antes de registrar: {personas.rut_persona}")
        cuenta = self.registrar_cuenta(Cuentas(nombre_cuenta=nombre_cuenta, contraseña="12345", rut_persona=personas.rut_persona.replace('"',"")))
        return cuenta

    def actualizar_nota(self, datos):
        querys = '''
        UPDATE notas
        SET nota = "{}"
        WHERE id_nota = {}
        '''.format(datos["nota"], datos["id"])
        return self.bd.insertar(querys)

    def registrar_estados(self, nombre):
        """
        Methodo Utilizado para ingresar los estados
        """
        querys = f'INSERT INTO estados(nombre_estado) VALUES("{nombre}")'
        self.bd.insertar(querys)

    def registrar_notas(self, nota:RegistroNotas, cuenta:Cuentas, objetivo="empresas"):
        """
        Methodo utilizado para gestionar notas de empresas y personas
        """
        nota.__dict__ = her.recuperacion_sentencia(nota).__dict__
        querys = '''
        INSERT INTO notas(nota)
        VALUES({});
        '''.format(nota.nota)
        nota_resgistrada = self.bd.insertar(querys)
        if not nota_resgistrada.get("estado"):
            return {"estado": False, "condicion": "INSERCION"}

        if objetivo == "empresas":
            querys = '''
                INSERT INTO empresas_notas(id_nota, rut_empresa)
                VALUES({},{});'''.format(nota_resgistrada.get("ultimo_id"), nota.rut_asociado)
            empresa_notas = self.bd.insertar(querys)
            if empresa_notas.get("estado"):
                return empresa_notas
            return {"estado": False, "condicion": "INSERCION"}
        elif objetivo == "personas":
            querys = '''
                INSERT INTO personas_notas(id_nota, rut_persona)
                VALUES({},{});
                '''.format(nota_resgistrada.get("ultimo_id"), nota.rut_asociado)
            persona_notas = self.bd.insertar(querys)

            if persona_notas.get("estado"):
                return persona_notas
            return {"estado": False, "condicion": "INSERCION"}

        return {"estado": False, "condicion": "SINSELECCION"}

    def registrar_estado_gastos(self, nombre):
        """
        Methodo utilizado para ingresar los estados de los gastos
        """
        querys = f'INSERT INTO estado_gastos(nombre) VALUES("{nombre}")'
        self.bd.insertar(querys)

    def registrar_gasto(self, contenido, persona: Personas):
        gastos = RegistrarGastos()
        gastos.__dict__ = her.recuperacion_sentencia(contenido).__dict__

        querys = """
        INSERT INTO gastos(descripcion, saldo, fecha_creacion, id_departamento, id_estado_gastos, rut_persona)
        VALUES({}, {}, {}, {}, {}, {});
        """.format(gastos.descripcion, gastos.saldo, gastos.fecha_creacion,
                   gastos.id_departamento, gastos.id_estado_gastos, persona.rut_persona)
        return self.bd.insertar(querys)

    def lista_menu_empresas(self):
        """
        Methodo utilizado para gestionar menus de empresas
        """
        querys = "SELECT rut_empresa, nombre_empresa FROM empresas;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_estados(self):
        """
        Methodo que gestiona estados de el programa
        """
        querys = f'SELECT id_estado, nombre_estado FROM estados;'
        return self.bd.consultar(querys, all=True)

    def lista_menu_personas(self):
        """
        Methodo utilizado para gstionar lista de personas
        """
        querys = "SELECT rut_persona, CONCAT(nombres, ' ', apellidos) as Nombres FROM personas;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_locales(self):
        """
        Methodo Utilizado para gestionar menus de locales
        """
        querys = "SELECT id_local, nombre_local	FROM locales;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_departamentos(self):
        """
        Methodo utulizar para gestionar departamentos
        """
        querys = """
        select dp.id_departamento, concat(dp.nombre_departamento, ' Local: ', l.nombre_local)
        from locales l
        inner join departamentos dp
        on l.id_local = dp.id_local
        """
        return self.bd.consultar(querys, all=True)

    def lista_menu_estado_gastos(self):
        """
        Methodo utlizado para los menus de estado de los gastos
        predefinidos por el sistema
        """
        querys = "SELECT * FROM estado_gastos;"
        return self.bd.consultar(querys, all=True)

    def actualizar_grupo_usuario(self, correo, grupo):
        querys = f'UPDATE USUARIOS SET GRUPOS = {grupo} WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def solicitar_estados(self):
        querys = f'SELECT * FROM ESTADOS;'
        return self.bd.consultar(querys, all=True)

    def registrar_servicios(self, datos):
        return
        objeto = RegistroServicios()
        objeto.__dict__ = her.recuperacion_sentencia(datos).__dict__
        print(objeto)
        querys = f'''
        INSERT INTO SERVICIOS(NOMBRE_SERVICIO, DESCRIPCION, FECHA_INICIO, FECHA_TERMINO, 
        ID_ESTADO, RUT_TRABAJADOR, RUT_PERSONA)
        VALUES({objeto.nombre}, {objeto.descr}, {objeto.fecha_inicio}, {objeto.fecha_termino},
        {objeto.id_estado}, {objeto.rut_trabajador}, {objeto.rut_persona})
        '''
        print(querys)

        return self.bd.insertar(querys)

    def solicitar_listado_servicios(self):
        querys = f'SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS;'
        return self.bd.consultar(querys, all=True)

    def nueva_contraseña(self, correo, contraseña_nueva):
        querys = f'UPDATE USUARIOS SET CONTRASEÑA = "{contraseña_nueva}" WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def solicitar_lista_productos(self):
        querys = f'SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, CANTIDAD FROM productos;'
        return self.bd.consultar(querys, all=True)

    def registrar_servicio_mensual(self, datos):
        servicio = ServicioMensual()
        servicio.__dict__ = her.recuperacion_sentencia(datos.get("contenido")).__dict__

        # id_servicios	nombre_servicio	id_estado	url_posicion
        # ubicacion	rut_usuario	descripcion	id_departamento	fecha_creacion
        querys_servicio = f'INSERT INTO servicios(nombre_servicio, id_estado, url_posicion,' \
                          f'ubicacion, rut_usuario, descripcion, id_departamento)' \
                          f'VALUES({servicio.nombre_servicio}, {servicio.id_estado}, {servicio.url_posicion},' \
                          f'{servicio.ubicacion}, {servicio.rut_usuario}, {servicio.descripcion}, ' \
                          f'{servicio.id_departamento});'
        qr_servicio = self.bd.insertar(querys_servicio)

        if not qr_servicio.get("estado"):
            return {"estado": False, "condicion": "INSERCION"}

        querys_servicio_mensual = f'INSERT INTO servicios_mensuales(id_servicios, fecha_inicio, fecha_termino)' \
                                  f'VALUES({qr_servicio.get("ultimo_id")}, {servicio.fecha_inicio}, ' \
                                  f'{servicio.fecha_termino});'

        qr_servicio_mensual = self.bd.insertar(querys_servicio_mensual)
        if not qr_servicio_mensual.get("estado"):
            return {"estado": False, "condicion": "INSERCION"}

        productos = datos.get("productos")

        base_producto = ServiciosProductos()
        for prod in productos:
            base_producto.__dict__ = her.recuperacion_sentencia(prod).__dict__
            querys_productos = f'INSERT INTO servicios_productos(id_producto, cantidad, precio, id_servicio)' \
                               f'VALUES({base_producto.id_producto}, {base_producto.cantidad},' \
                               f'{base_producto.precio}, {qr_servicio.get("ultimo_id")});'
            qr_productos = self.bd.insertar(querys_productos)
            if not qr_productos.get("estado"):
                return {"estado": False, "condicion": "INSERCION"}

        return {"estado": True}

    def registrar_servicio_diario(self, datos):
        servicio = ServicioDiarios()
        servicio.__dict__ = her.recuperacion_sentencia(datos.get("contenido")).__dict__

        # id_servicios	nombre_servicio	id_estado	url_posicion
        # ubicacion	rut_usuario	descripcion	id_departamento	fecha_creacion
        querys_servicio = f'INSERT INTO servicios(nombre_servicio, id_estado, url_posicion,' \
                          f'ubicacion, rut_usuario, descripcion, id_departamento)' \
                          f'VALUES({servicio.nombre_servicio}, {servicio.id_estado}, {servicio.url_posicion},' \
                          f'{servicio.ubicacion}, {servicio.rut_usuario}, {servicio.descripcion}, ' \
                          f'{servicio.id_departamento});'
        qr_servicio = self.bd.insertar(querys_servicio)

        if not qr_servicio.get("estado"):
            return {"estado": False, "condicion": "INSERCION"}

        querys_servicio_diarios = f'INSERT INTO servicios_diarios(id_servicios, dias_diarios)' \
                                  f'VALUES({qr_servicio.get("ultimo_id")}, {servicio.dias_diarios});'

        qr_servicio_diarios = self.bd.insertar(querys_servicio_diarios)
        if not qr_servicio_diarios.get("estado"):
            return {"estado": False, "condicion": "INSERCION"}

        productos = datos.get("productos")

        base_producto = ServiciosProductos()
        for prod in productos:
            base_producto.__dict__ = her.recuperacion_sentencia(prod).__dict__
            querys_productos = f'INSERT INTO servicios_productos(id_producto, cantidad, precio, id_servicio)' \
                               f'VALUES({base_producto.id_producto}, {base_producto.cantidad},' \
                               f'{base_producto.precio}, {qr_servicio.get("ultimo_id")});'
            qr_productos = self.bd.insertar(querys_productos)
            if not qr_productos.get("estado"):
                return {"estado": False, "condicion": "INSERCION"}

        return {"estado": True}

    def listado_gastos_fechas(self, contenido):
        fecha_inicio = contenido.get("fecha_inicio")
        fecha_termino = contenido.get("fecha_termino")
        departamento = contenido.get("departamento")
        print(f"inicio: {fecha_inicio} termino: {fecha_termino} departamento: {departamento}")

        sentencia = """
        SELECT ga.id_gasto, eg.nombre, ga.saldo, cu.nombre_cuenta, dep.nombre_departamento, ga.fecha_creacion,
        ga.descripcion
        FROM gastos ga
        LEFT JOIN cuentas cu ON cu.id_cuenta = ga.id_cuenta
        LEFT JOIN departamentos dep ON dep.id_departamento = ga.id_departamento
        LEFT JOIN estado_gastos eg ON eg.id_estado_gastos = ga.id_estado_gastos
        """

        if fecha_termino is None:
            sentencia += f"WHERE ga.fecha_creacion = DATE('{fecha_inicio}')\n"
        else:
            sentencia += f"WHERE ga.fecha_creacion BETWEEN '{fecha_inicio}' AND '{fecha_termino}'\n"

        if departamento is not None:
            sentencia += f"AND ga.id_departamento = {departamento}"

        sentencia += ";"
        print(sentencia)
        return self.bd.consultar(sentencia, all=True)

    def lista_empresas(self):
        querys = '''
        select RUT_EMPRESA, NOMBRE_EMPRESA  from empresas;
        '''
        return self.bd.consultar(querys, all=True)

    def consultar_correo_existente(self, correo):
        querys = f'select CORREO  from usuarios where CORREO = "{correo}";'
        return self.bd.consultar(querys)

    def registrar_trabajador(self, contenido):
        trabajador = RegistroTrabajador()
        trabajador.__dict__ = her.recuperacion_sentencia(contenido).__dict__
        querys = '''
        INSERT INTO trabajadores(rut_persona, id_departamento, sueldo, dia_pago)
        VALUES({}, {}, {}, {});
        '''.format(trabajador.rut_persona, trabajador.id_departamento,
                   trabajador.sueldo, trabajador.dia_pago)
        return self.bd.insertar(querys)

    def buscar_persona_rut(self, datos):
        querys = '''
        SELECT pe.rut_persona, pe.nombres, pe.apellidos, pe.telefono, pe.celular, pe.correo
        FROM personas pe
        INNER JOIN cuentas cu ON cu.rut_persona = pe.rut_persona
        WHERE pe.rut_persona = "{}"
        '''.format(datos.get("rut"))
        info = self.bd.consultar(querys)
        if info.get("estado"):
            if len(info.get("datos")) >= 1:
                datos = info.get("datos")
                maqueta = Personas(
                    rut_persona=datos[0],
                    nombres=datos[1],
                    apellidos=datos[2],
                    telefono=datos[3],
                    celular=datos[4],
                    correo=datos[5]
                )
                return {"estado": True, "datos": maqueta}
            return {"estado": False, "condicion": "SIN_DATOS"}
        return {"estado": False, "condicion": "SINSELECCION"}

    def lista_personas(self):
        querys = """
        SELECT rut_persona, CONCAT(nombres, ' ', apellidos) AS nombres
        FROM personas
        """
        return self.bd.consultar(querys, all=True)

    def registrar_locales(self, objeto):
        objeto = her.recuperacion_sentencia(objeto)
        local = RegistrarLocales()
        local.__dict__ = objeto.__dict__

        querys = '''
        INSERT INTO locales(nombre_local, telefono_local, direccion)
        VALUES({}, {}, {})
        '''.format(local.nombre_local, local.telefono_local, local.direccion)
        return self.bd.insertar(querys)

    def lista_menu_trabajadores(self):
        querys = """
        SELECT t.RUT, CONCAT(p.NOMBRES, ' ', p.APELLIDOS) as Nombres
        FROM trabajadores t
        JOIN personas p ON p.RUT = t.RUT;
        """
        return self.bd.consultar(querys, all=True)

    def lista_menu_productos(self):
        querys = "SELECT ID_PRODUCTO, NOMBRE_PRODUCTO FROM productos;"
        return self.bd.consultar(querys, all=True)

    def mis_servicios(self, persona):
        querys = """
        SELECT se.id_servicios, pe.rut_persona, se.nombre_servicio,  se.fecha_creacion, se.id_estado, es.nombre_estado
        FROM cuentas cu
        INNER JOIN personas pe ON pe.rut_persona = cu.rut_persona
        INNER JOIN servicios se ON se.rut_usuario = pe.rut_persona
        INNER JOIN estados es ON es.id_estado = se.id_estado
        WHERE pe.rut_persona = "{}"
        """.format(persona.rut_persona)
        return self.bd.consultar(querys, all=True)

    def listado_notas_empresa_especifica(self, contenido):
        querys = """
            SELECT n.id_nota, en.rut_empresa, n.nota, n.fecha_creacion, cu.nombre_cuenta
            FROM notas n
            INNER JOIN empresas_notas en
                ON en.id_nota = n.id_nota
            INNER JOIN cuentas cu
                ON cu.id_cuenta = n.id_cuenta
            WHERE en.rut_empresa = "{}"
            GROUP BY n.fecha_creacion DESC;
        """.format(contenido)
        datos = self.bd.consultar(querys, all=True)
        lista_notas = []
        for nota in datos.get("datos"):
            lista_notas.append(RegistroNotas(id_registro=nota[0], rut_asociado=nota[1],
                                             nota=nota[2], fecha_creacion=nota[3],
                                             id_cuenta=nota[4]))
        datos.update({"datos": lista_notas})
        return datos

    def listado_notas_persona_especifica(self, rut_persona):
        querys = """
            SELECT n.id_nota, pe.rut_persona, n.nota, n.fecha_creacion, cu.nombre_cuenta
            FROM notas n
            INNER JOIN personas_notas pe
                ON pe.id_nota = n.id_nota
            INNER JOIN trabajadores tra
                ON tra.rut_persona = n.rut_persona
            INNER JOIN cuenta cu
                ON cu.rut_persona = pe.rut_persona
            WHERE pe.rut_persona = "{}"
            GROUP BY n.fecha_creacion DESC;
        """.format(rut_persona)
        datos = self.bd.consultar(querys, all=True)
        lista_notas = []
        for nota in datos.get("datos"):
            lista_notas.append(RegistroNotas(id_registro=nota[0], rut_asociado=nota[1],
                                             nota=nota[2], fecha_creacion=nota[3],
                                             nombre_creado=nota[4]))
        datos.update({"datos": lista_notas})
        return datos

    def asignar_grupo(self, rut_Trabajador, id_grupo):
        querys = """
        INSERT INTO grupos_trabajadores(ID_GRUPO, RUT_TRABAJADOR) 
        VALUES ('{}', '{}')
        """.format(id_grupo, rut_Trabajador)
        return self.bd.insertar(querys)

    def buscar_trabajador_rut(self, rut: str) -> RegistroTrabajador:
        querys = """
        SELECT * 
        FROM trabajadores
        WHERE rut_persona = '{}'
        """.format(rut)
        # rut_persona	id_departamento	sueldo	dia_pago
        info = self.bd.consultar(querys)
        if info.get("estado"):
            datos = info.get("datos")
            return RegistroTrabajador(rut_persona=datos[0],
                                      id_departamento=datos[1],
                                      sueldo=datos[2],
                                      dia_pago=datos[3])
        return None

    def buscar_servicio_id(self, id_servicio):
        querys = """
        SELECT *
        FROM servicios
        WHERE id_servicios = {}
        """.format(id_servicio)
        info = self.bd.consultar(querys)
        if info.get("estado"):
            datos = info.get("datos")
            contenido = {"estado": True, "datos": AbstracServicio(id_servicio=datos[0],
                                                                  nombre_servicio=datos[1],
                                                                  id_estado=datos[2],
                                                                  url_posicion=datos[3],
                                                                  ubicacion=datos[4],
                                                                  rut_usuario=datos[5],
                                                                  descripcion=datos[6],
                                                                  id_departamento=datos[7],
                                                                  fecha_creacion=datos[8])}
            return contenido
        return info

    def buscar_servicios_mensuales_id(self, id_servicio_mensual):
        querys = """
        SELECT *
        FROM servicios ser
        INNER JOIN servicios_mensuales serm ON serm.id_servicios = ser.id_servicios
        WHERE ser.id_servicios = {}
        """.format(id_servicio_mensual)
        info = self.bd.consultar(querys)
        if info.get("estado"):
            datos = info.get("datos")
            contenido = {"estado": True, "contenido": ServicioMensual(id_servicio=datos[0],
                                                                      nombre_servicio=datos[1],
                                                                      id_estado=datos[2],
                                                                      url_posicion=datos[3],
                                                                      ubicacion=datos[4],
                                                                      rut_usuario=datos[5],
                                                                      descripcion=datos[6],
                                                                      id_departamento=datos[7],
                                                                      fecha_creacion=datos[8],
                                                                      fecha_inicio=datos[9],
                                                                      fecha_termino=datos[10])}
            return {"estado": True, "datos": contenido}

    def buscar_servicios_diarios_id(self, id_servicio_diario):
        querys = """
        SELECT *
        FROM servicios ser
        INNER JOIN servicios_diarios serm ON serm.id_servicios = ser.id_servicios
        WHERE ser.id_servicios = {}
        """.format(id_servicio_diario)

    def buscar_servicios(self, trabajador: RegistroTrabajador):
        if trabajador is None:
            return {"estado": False}

        # Sentencia Servicios Enteros
        # querys = """
        # SELECT ser.id_servicios, ser.nombre_servicio, ser.url_posicion, ser.ubicacion, ser.descripcion,
        # pe.nombres, pe.apellidos, pe.celular, pe.telefono,
        # est.nombre_estado
        #
        # FROM servicios ser
        # INNER JOIN personas pe ON pe.rut_persona = ser.rut_usuario
        # INNER JOIN estados est ON est.id_estado = ser.id_estado
        # WHERE ser.id_departamento = {}
        # """.format(trabajador.id_departamento)

        querys = """
            SELECT ser.id_servicios, ser.nombre_servicio, ser.url_posicion, ser.ubicacion, ser.descripcion,
            pe.nombres, pe.apellidos, pe.celular, pe.telefono,
            est.nombre_estado
            
            FROM servicios ser
            INNER JOIN personas pe ON pe.rut_persona = ser.rut_usuario
            INNER JOIN estados est ON est.id_estado = ser.id_estado
            INNER JOIN servicios_mensuales smen ON smen.id_servicios = ser.id_servicios
            WHERE ser.id_departamento = {} AND
            ser.id_estado = 1 OR ser.id_estado = 4 OR
            ser.id_estado = 5
        """.format(trabajador.id_departamento)
        return self.bd.consultar(querys, all=True)

    """
        SELECT ser.id_servicios, ser.nombre_servicio, ser.url_posicion, ser.ubicacion, ser.descripcion,
        pe.nombres, pe.apellidos, pe.celular, pe.telefono,
        est.nombre_estado
        
        FROM servicios ser
        INNER JOIN personas pe ON pe.rut_persona = ser.rut_usuario
        INNER JOIN estados est ON est.id_estado = ser.id_estado
        INNER JOIN servicios_mensuales smen ON smen.id_servicios = ser.id_servicios
        WHERE ser.id_departamento = 1 AND
        ser.id_estado = 1 OR ser.id_estado = 4 OR
		ser.id_estado = 5
    """
