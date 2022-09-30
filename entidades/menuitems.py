class MenuItemPersonas:
    def __init__(self, rut, nombre):
        self.rut = rut
        self.nombre = nombre


class MenuItemEstado:
    def __init__(self, id_estado, nombre):
        self.id_estado = id_estado
        self.nombre = nombre


class MenuItemLocales:
    def __init__(self, id_local, nombre_local):
        self.id_local = id_local
        self.nombre_local = nombre_local


class MenuGlobal:
    def __init__(self, identificador, nombre):
        self.identificador = identificador
        self.nombre = nombre
