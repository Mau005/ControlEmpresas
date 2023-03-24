from entidades.cuentas import Cuentas
from entidades.personas import Personas


class ControlUsuarios:

    def __init__(self, **kargs):
        self._cuenta = kargs.get("cuenta")
        self._trabajador = kargs.get("trabajador")
        self._persona = kargs.get("persona")
        self._local = kargs.get("local")
        self.querys = kargs.get("querys")
        self._serial_user =kargs.get("serial_user")

    @property
    def serial_user(self):
        return self._serial_user
    @serial_user.setter
    def serial_user(self, serial:str):
        print(f"Serial: {serial}")
        self._serial_user = serial

    @property
    def persona(self):
        return self._persona
    @persona.setter
    def persona(self, per : Personas):
        self._persona = per
    @property
    def cuenta(self):
        return self._cuenta

    @cuenta.setter
    def cuenta(self, cue :Cuentas):
        self.serial_user = cue.serializacion
        self._cuenta = cue

    @property
    def trabajador(self):
        return self._trabajador

    @trabajador.setter
    def trabajador(self, tra: dict):
        self._trabajador = tra

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, lo:dict):
        self._local = lo