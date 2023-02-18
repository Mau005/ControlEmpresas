DROP TABLE IF EXISTS cuentas;
DROP TABLE IF EXISTS personas;
DROP TABLE IF EXISTS empresas;
DROP TABLE IF EXISTS locales;
DROP TABLE IF EXISTS estados;
DROP TABLE IF EXISTS estados_preparativos;
DROP TABLE IF EXISTS trabajadores;
DROP TABLE IF EXISTS departamentos;
DROP TABLE IF EXISTS abonos_trabajadores;
DROP TABLE IF EXISTS empresas_personas;
DROP TABLE IF EXISTS notas;
DROP TABLE IF EXISTS empresas_notas;
DROP TABLE IF EXISTS personas_notas;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS servicios_mensuales;
DROP TABLE IF EXISTS servicios_diarios;
DROP TABLE IF EXISTS orden_trabajo;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS facturas;
DROP TABLE IF EXISTS facturas_productos;
DROP TABLE IF EXISTS empresas_facturas;
DROP TABLE IF EXISTS personas_facturas;
DROP TABLE IF EXISTS facturas_servicios;
DROP TABLE IF EXISTS servicios_productos;
DROP TABLE IF EXISTS gastos;
DROP TABLE IF EXISTS estado_gastos;
DROP TABLE IF EXISTS ot_historia;


CREATE TABLE cuentas (
rut_persona VARCHAR(12) PRIMARY KEY NOT NULL UNIQUE,
nombre_cuenta VARCHAR(55) NOT NULL UNIQUE,
contraseña VARCHAR(50) NOT NULL,
fecha_creacion DATETIME NOT NULL,
acceso INT(2) NOT NULL);

CREATE TABLE personas (
rut_persona VARCHAR(12) PRIMARY KEY NOT NULL,
nombres VARCHAR(100) NOT NULL,
apellidos VARCHAR(100) NOT NULL,
telefono VARCHAR(12),
celular VARCHAR(12) NOT NULL,
correo VARCHAR(100) NOT NULL);

CREATE TABLE empresas (
rut_empresa VARCHAR(12) PRIMARY KEY NOT NULL,
nombre_empresa VARCHAR(100) NOT NULL,
giro_empresa VARCHAR(150) NOT NULL,
direccion_empresa VARCHAR(150) NOT NULL,
correo_empresa VARCHAR(150) NOT NULL,
correo_respaldo VARCHAR(150),
telefono_empresa VARCHAR(12),
celular_empresa VARCHAR(12));

CREATE TABLE locales (
id_local INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre_local VARCHAR(150) NOT NULL,
direccion VARCHAR(150) NOT NULL,
telefono_local VARCHAR(12));

CREATE TABLE estados (
id_estado INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre_estado VARCHAR(50) NOT NULL);

CREATE TABLE estados_preparativos (
id_estado INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre_estado VARCHAR(50) NOT NULL);

CREATE TABLE trabajadores (
rut_persona VARCHAR(12) PRIMARY KEY NOT NULL,
id_departamento INT(11) NOT NULL,
sueldo INT(11) NOT NULL,
dia_pago INT(2) NOT NULL);

CREATE TABLE departamentos (
id_departamento INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
id_local INT(11) NOT NULL,
nombre_departamento VARCHAR(100) NOT NULL,
descripcion TEXT(250));

CREATE TABLE abonos_trabajadores (
id_abono INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
rut_persona VARCHAR(12) NOT NULL,
abono INT(11) NOT NULL,
descripcion TEXT(250),
fecha_creacion DATETIME NOT NULL);

CREATE TABLE empresas_personas (
id_empresas_personas INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
rut_empresa VARCHAR(12) NOT NULL,
rut_persona VARCHAR(12) NOT NULL);

CREATE TABLE notas (
id_nota INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nota TEXT(250) NOT NULL,
fecha_creacion DATETIME NOT NULL);

CREATE TABLE empresas_notas (
id_nota INT(11) PRIMARY KEY NOT NULL,
rut_empresa VARCHAR(12) NOT NULL);

CREATE TABLE personas_notas (
id_nota INT(11) PRIMARY KEY NOT NULL,
rut_persona VARCHAR(12) NOT NULL);

CREATE TABLE servicios (
id_servicios INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre_servicio VARCHAR(100) NOT NULL,
id_estado INT(11) NOT NULL,
url_posicion VARCHAR(250),
ubicacion VARCHAR(250) NOT NULL,
rut_usuario VARCHAR(12) NOT NULL,
descripcion TEXT(250),
fecha_creacion DATETIME NOT NULL);

CREATE TABLE servicios_mensuales (
id_servicios INT(11) PRIMARY KEY NOT NULL,
fecha_inicio DATE NOT NULL,
fecha_termino DATE NOT NULL);

CREATE TABLE servicios_diarios (
id_servicios INT(11) PRIMARY KEY NOT NULL,
dias_diarios VARCHAR(7) NOT NULL,
id_departamento INT(11) NOT NULL);

CREATE TABLE orden_trabajo (
id_orden INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
id_servicios INT(11) NOT NULL,
fecha_creacion DATETIME NOT NULL,
fecha_termino DATETIME NOT NULL,
id_estado INT(11) NOT NULL,
id_estado_pre INT(11) NOT NULL,
precio_ot INT(11) NOT NULL,
descripcion TEXT(250));

CREATE TABLE productos (
id_producto INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre_producto VARCHAR(100) NOT NULL,
descripcion TEXT(250),
fecha_creacion DATETIME NOT NULL,
cantidad INT(11) NOT NULL,
id_local INT(11) NOT NULL);

CREATE TABLE facturas (
folio_factura INT(11) PRIMARY KEY NOT NULL UNIQUE,
iva INT(11) NOT NULL,
total INT(11) NOT NULL,
neto INT(11) NOT NULL);

CREATE TABLE facturas_productos (
id_facturas_productos INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
folio_factura INT(11) NOT NULL,
id_producto INT(11) NOT NULL,
precio INT(11) NOT NULL,
cantidad INT(11) NOT NULL);

CREATE TABLE empresas_facturas (
folio_factura INT(11) PRIMARY KEY NOT NULL,
rut_empresa VARCHAR(12) NOT NULL);

CREATE TABLE personas_facturas (
folio_factura INT(11) PRIMARY KEY NOT NULL,
rut_persona VARCHAR(12) NOT NULL);

CREATE TABLE facturas_servicios (
id_factura_servicios INT(11) PRIMARY KEY NOT NULL,
folio_factura INT(11) NOT NULL,
id_servicios INT(11) NOT NULL);

CREATE TABLE servicios_productos (
id_servicios_productos INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
id_producto INT(11) NOT NULL,
cantidad INT(11) NOT NULL,
precio INT(11) NOT NULL,
id_servicio INT(11) NOT NULL);

CREATE TABLE gastos (
id_gasto INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
descripcion TEXT(250),
saldo INT(11) NOT NULL,
fecha_creacion DATETIME NOT NULL,
id_departamento INT(11) NOT NULL,
id_estado_gastos INT(11) NOT NULL,
rut_persona VARCHAR(12) NOT NULL);

CREATE TABLE estado_gastos (
id_estado_gastos INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
nombre VARCHAR(100) NOT NULL);

CREATE TABLE ot_historia (
id_ot_historia INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
id_orden INT(11) NOT NULL,
fecha_creacion DATETIME NOT NULL,
id_pre_anterior INT(11) NOT NULL,
id_pre_nuevo INT(11) NOT NULL,
descripcion TEXT(250));

ALTER TABLE cuentas ADD CONSTRAINT cuentas_rut_persona_personas_rut_persona FOREIGN KEY (rut_persona) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE trabajadores ADD CONSTRAINT trabajadores_rut_persona_personas_rut_persona FOREIGN KEY (rut_persona) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE trabajadores ADD CONSTRAINT trabajadores_id_departamento_departamentos_id_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE departamentos ADD CONSTRAINT departamentos_id_local_locales_id_local FOREIGN KEY (id_local) REFERENCES locales(id_local) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE abonos_trabajadores ADD CONSTRAINT abonos_trabajadores_rut_persona_trabajadores_rut_persona FOREIGN KEY (rut_persona) REFERENCES trabajadores(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_personas ADD CONSTRAINT empresas_personas_rut_empresa_empresas_rut_empresa FOREIGN KEY (rut_empresa) REFERENCES empresas(rut_empresa) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_personas ADD CONSTRAINT empresas_personas_rut_persona_personas_rut_persona FOREIGN KEY (rut_persona) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_notas ADD CONSTRAINT empresas_notas_id_nota_notas_id_nota FOREIGN KEY (id_nota) REFERENCES notas(id_nota) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_notas ADD CONSTRAINT empresas_notas_rut_empresa_empresas_rut_empresa FOREIGN KEY (rut_empresa) REFERENCES empresas(rut_empresa) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE personas_notas ADD CONSTRAINT personas_notas_id_nota_notas_id_nota FOREIGN KEY (id_nota) REFERENCES notas(id_nota) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE personas_notas ADD CONSTRAINT personas_notas_rut_persona_personas_rut_persona FOREIGN KEY (rut_persona) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios ADD CONSTRAINT servicios_id_estado_estados_id_estado FOREIGN KEY (id_estado) REFERENCES estados(id_estado) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios ADD CONSTRAINT servicios_rut_usuario_personas_rut_persona FOREIGN KEY (rut_usuario) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios_mensuales ADD CONSTRAINT servicios_mensuales_id_servicios_servicios_id_servicios FOREIGN KEY (id_servicios) REFERENCES servicios(id_servicios) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios_diarios ADD CONSTRAINT servicios_diarios_id_servicios_servicios_id_servicios FOREIGN KEY (id_servicios) REFERENCES servicios(id_servicios) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios_diarios ADD CONSTRAINT servicios_diarios_id_departamento_departamentos_id_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE orden_trabajo ADD CONSTRAINT orden_trabajo_id_servicios_servicios_id_servicios FOREIGN KEY (id_servicios) REFERENCES servicios(id_servicios) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE orden_trabajo ADD CONSTRAINT orden_trabajo_id_estado_estados_id_estado FOREIGN KEY (id_estado) REFERENCES estados(id_estado) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE orden_trabajo ADD CONSTRAINT orden_trabajo_id_estado_pre_estados_preparativos_id_estado FOREIGN KEY (id_estado_pre) REFERENCES estados_preparativos(id_estado) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE facturas_productos ADD CONSTRAINT facturas_productos_folio_factura_facturas_folio_factura FOREIGN KEY (folio_factura) REFERENCES facturas(folio_factura) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE facturas_productos ADD CONSTRAINT facturas_productos_id_producto_productos_id_producto FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_facturas ADD CONSTRAINT empresas_facturas_folio_factura_facturas_folio_factura FOREIGN KEY (folio_factura) REFERENCES facturas(folio_factura) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE empresas_facturas ADD CONSTRAINT empresas_facturas_rut_empresa_empresas_rut_empresa FOREIGN KEY (rut_empresa) REFERENCES empresas(rut_empresa) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE personas_facturas ADD CONSTRAINT personas_facturas_folio_factura_facturas_folio_factura FOREIGN KEY (folio_factura) REFERENCES facturas(folio_factura) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE personas_facturas ADD CONSTRAINT personas_facturas_rut_persona_personas_rut_persona FOREIGN KEY (rut_persona) REFERENCES personas(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE facturas_servicios ADD CONSTRAINT facturas_servicios_folio_factura_facturas_folio_factura FOREIGN KEY (folio_factura) REFERENCES facturas(folio_factura) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE facturas_servicios ADD CONSTRAINT facturas_servicios_id_servicios_servicios_id_servicios FOREIGN KEY (id_servicios) REFERENCES servicios(id_servicios) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE servicios_productos ADD CONSTRAINT servicios_productos_id_producto_productos_id_producto FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE servicios_productos ADD CONSTRAINT servicios_productos_id_servicio_servicios_id_servicios FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicios) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE gastos ADD CONSTRAINT gastos_id_departamento_departamentos_id_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE gastos ADD CONSTRAINT gastos_id_estado_gastos_estado_gastos_id_estado_gastos FOREIGN KEY (id_estado_gastos) REFERENCES estado_gastos(id_estado_gastos) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE gastos ADD CONSTRAINT gastos_rut_persona_trabajadores_rut_persona FOREIGN KEY (rut_persona) REFERENCES trabajadores(rut_persona) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE ot_historia ADD CONSTRAINT ot_historia_id_orden_orden_trabajo_id_orden FOREIGN KEY (id_orden) REFERENCES orden_trabajo(id_orden) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE ot_historia ADD CONSTRAINT ot_historia_id_pre_anterior_estados_preparativos_id_estado FOREIGN KEY (id_pre_anterior) REFERENCES estados_preparativos(id_estado) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE ot_historia ADD CONSTRAINT ot_historia_id_pre_nuevo_estados_preparativos_id_estado FOREIGN KEY (id_pre_nuevo) REFERENCES estados_preparativos(id_estado) ON DELETE CASCADE ON UPDATE CASCADE;
