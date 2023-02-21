TAMANIO_PAQUETE = 2048
IP = "localhost"
PORT = 7171

PROTOCOLOERROR = {"USUARIOACTIVO": "Usuario ya se encuentra activo en el sistema",
                  "RECUPERACION": "Usuario se encuentra en un proceso de recuperacion de cuenta",
                  "NETWORK": "Sin conexión con el Servidor",
                  "PRIVILEGIOS": "Esta cuenta no tiene los privilegios necesarios para realizar esta accion",
                  "CONTRASEÑAS": "Usuario o Contraseñas incorrectas.",
                  "INSERCION": "Datos no se han podido guardar por un fallo en el contenido.",
                  "REGISTRARCUENTA":"Hubo un problema al poder registrar la cuenta de este usuario",
                  "RUT_EXISTE":"Este usuario ya se encuentra registrado",
                  "EMPRESA_EXISTE":"Esta empresa ya se encuentra registrado",
                  "SIN_DATOS": "La consulta pedida, no tiene información",
                  "SINSELECCION":"No Se ha ingresado una seleccion correspondiente",
                  "EXPIRACION": "Se ha expirado el tiempo de seccion activa.",
                  "NOSEENCUENTRA": "No se ha podido localizar los datos.",
                  "NOTRABAJADOR": "Usted no pertenece al equipo de trabajo de esta empresa"}

DIA_SEMANA = {1: "Lunes", 2: "Martes", 3: "Miercoles", 4: "Jueves", 5: "Viernes", 6: "Sabado", 7: "Domingo"}
