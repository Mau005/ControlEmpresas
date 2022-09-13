from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from entidades.registroservicio import RegistroServicios
from core.constantes import BUTTONCREATE
from entidades.registroempresas import RegistroEmpresas

class VEmpresas(MDScreenAbstrac):
        
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        self.data = BUTTONCREATE
        self.ids.botones.data = self.data
        self.correo = "prueba"
        
            
    def verificar_rut(self, rut):
        if not("-" in rut):
            return False, "Rut debe llevar -"
        
        rut = rut.split("-") #lista 2 donde se divie en -
        contenido_rut = rut[0].replace(".", "") #contener el contenido rut
        
        if len(contenido_rut) != 8:
            return False, "Rut debe tener los . bien puestos"
        
        if len(rut[1]) != 1:
            return False, "Rut debe tener un digito verificador"
        
        if "k" in contenido_rut or "0" in contenido_rut[0]: #comprobamos que no tenga uan K en el contenido del rut y si comienza en 0 tan bien se salga
            return False, "Rut no se logra verificar, Escrito mal"
        
        verificador_rut = rut[1] # vamos el ultimo digito verificador
        formato = "0123456789" #formato
        
        contenido_rut += rut[1]
        
        verificador_bool = [False for x in range(0,len(contenido_rut))]
        
        contador = 0
        for caracter_rut in contenido_rut:
            for caracter_formato in formato:
                if caracter_formato == caracter_rut:
                    verificador_bool[contador] = True
            contador += 1
        
        if False in verificador_bool:
            return False, f"No se puede comprobar el rut correctamente"
        return True, f"{rut[0]}-{rut[1]}"
        
        
        
    def accion_boton(self, arg):
        if arg.icon == "exit-run":
            self.siguiente()
        if arg.icon == "pencil":
            longitud = 1
            noti = Notificacion("Error","")
            estado = True
            if not(len(self.ids.rut_empresa.text) == 12):
                noti.text += "Debe tener 12 caracteres el RUT de Empresa\n"
                estado = False
            if not(len(self.ids.nombre_empresa.text) >= longitud):
                noti.text += "Debe tener Contenido el Nombre de Empresa\n"
                estado = False
            if not(len(self.ids.giro_empresa.text) >= longitud):
                noti.text += "Debe tener Contenido el Giro de la empresa\n"
                estado = False
            if not(len(self.ids.direccion_empresa.text) >= longitud):
                noti.text += "Debe tener contenido la direccion de la empresa\n"
                estado = False
            if not(len(self.ids.celular_empresa.text) >= 8):
                noti.text += "El celular de empresa debe tener almenos 8 numeros\n"
                estado = False
            if not("@" in self.ids.correo_empresa.text):
                noti.text += "El Correo de la empresa debe tener almenos un @\n"
                estado = False
            if estado:
                vericando_rut = self.verificar_rut(self.ids.rut_empresa.text)
                if vericando_rut[0]:
                    noti.title = "Correcto"
                    noti.text = vericando_rut[1]
                    noti.open()
                    objeto = RegistroEmpresas(
                        rut_empresa = self.ids.rut_empresa.text,
                        nombre_empresa = self.ids.nombre_empresa.text,
                        giro_empresa = self.ids.giro_empresa.text,
                        direccion_empresa = self.ids.direccion_empresa.text,
                        telefono = self.ids.telefono_empresa.text,
                        celular_empresa = self.ids.celular_empresa.text,
                        correo_empresa = self.ids.correo_empresa.text,
                        correo_respaldo= self.ids.correo_respaldo_empresa.text,
                    )
                    self.network.enviar(objeto.preparar())
                    info = self.network.recibir()
                    if info.get("estado"):
                        noti = Notificacion("Exito", info.get("condicion"))
                        noti.open()
                    else:
                        noti = Notificacion("Error", "No se ha podido ingresar los datos")
                        noti.open()
                else:
                    noti.text = vericando_rut[1]
                    noti.open()
            else:
                noti.open()
            
                
            
        if arg.icon == "delete":
            self.formatear()
            
    def formatear(self):
        self.ids.rut_empresa.text = ""
        self.ids.nombre_empresa.text = ""
        self.ids.giro_empresa.text = ""
        self.ids.direccion_empresa.text = ""
        self.ids.telefono_empresa.text = ""
        self.ids.celular_empresa.text = ""
        self.ids.correo_empresa.text = ""
        self.ids.correo_respaldo_empresa.text = ""
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)
        
    