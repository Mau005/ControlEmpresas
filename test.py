def verificar_rut(rut):
    """Methodo usado para verificacion de rut, procesando cada segmento divido en 2
    desde el verificador a la cantidad de rut y lo formatea en xx.xxx.xxx-x

    Args:
        rut (str): rut de longitud de 12

    Returns:
        str: procesesado a xx.xxx.xxx-x
    """
    if not ("-" in rut):
        return False, "Rut debe llevar -"

    rut = rut.split("-")  # lista 2 donde se divie en -
    contenido_rut = rut[0].replace(".", "")  # contener el contenido rut
    longitud_rut = len(contenido_rut)

    if longitud_rut >=9 or longitud_rut <= 6:
        return False, "Rut debe tener los . bien puestos"

    if len(rut[1]) != 1:
        return False, "Rut debe tener un digito verificador"

    contenido_rut = contenido_rut.lower()
    if "k" in contenido_rut or "0" in contenido_rut[
        0]:  # comprobamos que no tenga uan K en el contenido del rut y si comienza en 0 tan bien se salga
        return False, "Rut no se logra verificar, Escrito mal"

    formato = "0123456789k"  # formato

    contenido_rut += rut[1].lower()

    verificador_bool = [False for x in range(0, len(contenido_rut))]

    contador = 0
    for caracter_rut in contenido_rut:
        for caracter_formato in formato:
            if caracter_formato == caracter_rut:
                verificador_bool[contador] = True
        contador += 1

    if False in verificador_bool:
        return False, f"No se puede comprobar el rut correctamente"
    if len(rut[0]) == 8:
        formato_nuevo = f"{rut[0][:2]}.{rut[0][2:5]}.{rut[0][5:8]}"  # es procesar el rut devido a la cantida dde informacion

    else:
        formato_nuevo = f"{rut[0][:1]}.{rut[0][1:4]}.{rut[0][4:8]}"  # es procesar el rut devido a la cantida dde informacion
    return True, f"{formato_nuevo}-{rut[1].lower()}"


print(verificar_rut("12347568-1"))
