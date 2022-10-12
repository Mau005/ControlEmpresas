TAMANIO_PAQUETE = 1024
IP = "localhost"
PORT = 7171

BUTTONCREATE = {'Crear': 'pencil', 'Formatear': 'delete', 'Salir': 'exit-run'}
PROTOCOLOERROR = {"USUARIOACTIVO": "Usuario ya se encuentra activo en el sistema",
                  "RECUPERACION": "Usuario se encuentra en un proceso de recuperacion de cuenta",
                  "NETWORK": "Sin conexión con el Servidor",
                  "PRIVILEGIOS": "Esta cuenta no tiene los privilegios necesarios para realizar esta accion",
                  "CONTRASEÑAS": "Usuario o Contraseñas incorrectas.",
                  "INSERCION": "Datos no se han podido guardar por un fallo en el contenido.",
                  "REGISTRARCUENTA":"Hubo un problema al poder registrar la cuenta de este usuario",
                  "RUT_EXISTE":"Este usuario ya se encuentra registrado"}

ERRORPRIVILEGIOS = "No tienes los privilegios para ejercer esta accion"
TIEMPOACTUALIZAR = 1  # segundos
REVISARCORREOS = 2
TIMEPOESPERAUSUARIO = 60 * 5
TIEMPOESPERADIGITO = 60 * 5

DIA_SEMANA = {1: "Lunes", 2: "Martes", 3: "Miercoles", 4: "Jueves", 5: "Viernes", 6: "Sabado", 7: "Domingo"}
