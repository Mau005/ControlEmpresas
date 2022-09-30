from entidades.registroserviciosdiarios import RegistroServiciosDiarios

objeto = RegistroServiciosDiarios(
    nombre_servicio="Prueba de Nombre",
    id_estado= 1,
    precio=55,
    fecha_semana="135",
    url_posicion=None,
    ubicacion="Av mama esta presa",
    rut_usuario="18.881.495-6",
    rut_trabajador="18.881.495-6",
    descr=None,
    toda_semana=True,
    id_producto=4,
    cantidad=4
)

def recuperacion_sentencia(objeto):
    for elementos in objeto.__dict__.keys():
        if isinstance(objeto.__dict__[elementos], str):
            objeto.__dict__[elementos] = f'"{objeto.__dict__[elementos]}"'
        if isinstance(objeto.__dict__[elementos],int) or isinstance(objeto.__dict__[elementos], bool) \
                or isinstance(objeto.__dict__[elementos], float):
            objeto.__dict__[elementos] = f"{objeto.__dict__[elementos]}"
        if objeto.__dict__[elementos] is None:
            objeto.__dict__[elementos] =  "NULL"
    return objeto



def registrar_servicio_diario(objeto):
    obj = RegistroServiciosDiarios()
    obj.__dict__ = objeto.__dict__
    obj = recuperacion_sentencia(obj)
    querys = '''
    INSERT INTO serviciosdiarios(NOMBRE_SERVICIO, ID_ESTADO, PRECIO, FECHA_SEMANA, URL_POSICION, UBICACION,
    RUT_USUARIO, RUT_TRABAJADOR, DESCR, TODA_SEMANA, ID_PRODUCTO, CANTIDAD)
    VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
    '''.format(obj.nombre_servicio, obj.id_estado, obj.precio, obj.fecha_semana, obj.url_posicion, obj.ubicacion,
               obj.rut_usuario, obj.rut_trabajador, obj.descr, obj.toda_semana, obj.id_producto, obj.cantidad)
    print(querys)


print(registrar_servicio_diario(objeto))
