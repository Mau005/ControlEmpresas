
def generar_nombres(datos1, datos2):
    """
    Methodo usado para generar nombres
    de usuarios segun sus nombres y apellidos
    """
    if " " in datos1:
        datos1 = datos1.split(" ")
        datos1 = datos1[0][0]
    else:
        datos1 = datos1[0]
    if " " in datos2:
        datos2 = datos2.split(" ")
        datos2 = f"{datos2[0]}{datos2[1][0]}"
    else:
        datos2 = datos2

    return (datos1+datos2).lower()




print(generar_nombres("Mauricio", "Pino 1"))