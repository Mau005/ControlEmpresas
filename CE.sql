-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-10-2022 a las 02:14:37
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ce`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `RUT_EMPRESA` varchar(12) NOT NULL,
  `NOMBRE_EMPRESA` varchar(150) NOT NULL,
  `GIRO_EMPRESA` varchar(150) NOT NULL,
  `DIRECCION` varchar(250) NOT NULL,
  `TELEFONO` varchar(100) DEFAULT NULL,
  `CORREO_EMPRESA` varchar(100) NOT NULL,
  `CORREO_RESPALDO` varchar(100) DEFAULT NULL,
  `CELULAR_EMPRESA` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`RUT_EMPRESA`, `NOMBRE_EMPRESA`, `GIRO_EMPRESA`, `DIRECCION`, `TELEFONO`, `CORREO_EMPRESA`, `CORREO_RESPALDO`, `CELULAR_EMPRESA`) VALUES
('76634406-2', 'Servicio Integrales Los Tres Pinos', 'Compra y venta de baños quimicos', 'michimalongo 14600', '', 'administracion@lostrespinos.cl', '', '+56945415455'),
('Sin Empresa', 'Sin Empresa', 'Sin Empresa', 'Sin Empresa', 'Sin Empresa', 'Sin Empresa', 'Sin Empresa', 'Sin Empresa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados`
--

CREATE TABLE `estados` (
  `ID_ESTADO` int(11) NOT NULL,
  `NOMBRE` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `estados`
--

INSERT INTO `estados` (`ID_ESTADO`, `NOMBRE`) VALUES
(1, 'OPERATIVO'),
(2, 'DETENIDO'),
(3, 'TRANSLADO'),
(4, 'SINIESTRADO'),
(5, 'PREPARACIÓN');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `locales`
--

CREATE TABLE `locales` (
  `ID_LOCAL` int(11) NOT NULL,
  `NOMBRE_LOCAL` varchar(150) NOT NULL,
  `TELEFONO_LOCAL` varchar(14) NOT NULL,
  `DIRECCION` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `locales`
--

INSERT INTO `locales` (`ID_LOCAL`, `NOMBRE_LOCAL`, `TELEFONO_LOCAL`, `DIRECCION`) VALUES
(1, 'Principal', '+565656', 'Av Tusca con Chetes'),
(7, 'Los Tres Pinos santiago', '', 'michimalongo 14600 la pintana');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

CREATE TABLE `personas` (
  `RUT` varchar(12) NOT NULL,
  `NOMBRES` varchar(150) NOT NULL,
  `APELLIDOS` varchar(150) NOT NULL,
  `TELEFONO` varchar(14) DEFAULT NULL,
  `CELULAR` varchar(14) NOT NULL,
  `CORREO` varchar(150) NOT NULL,
  `RUT_EMPRESA` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`RUT`, `NOMBRES`, `APELLIDOS`, `TELEFONO`, `CELULAR`, `CORREO`, `RUT_EMPRESA`) VALUES
('18.881.495-6', 'Mauricio Andres', 'Pino Gonzalez', '', '+56946141941', 'arkinommo@gmail.com', 'Sin Empresa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `ID_PRODUCTO` int(11) NOT NULL,
  `NOMBRE_PRODUCTO` varchar(100) NOT NULL,
  `DESCRIPCION` varchar(250) NOT NULL,
  `FECHA_CREACION` datetime NOT NULL DEFAULT current_timestamp(),
  `CANTIDAD` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`ID_PRODUCTO`, `NOMBRE_PRODUCTO`, `DESCRIPCION`, `FECHA_CREACION`, `CANTIDAD`) VALUES
(3, 'Baños Sanitarios Estandar', 'Baño estandar sin ningun tipo de materiales extra', '2022-09-30 02:08:24', 50),
(4, 'Baños Sanitarios Ejecutivo', 'Baño ejecutivo con lavamanos y confort industrial,', '2022-09-30 02:08:51', 24);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_notas_empresas`
--

CREATE TABLE `registro_notas_empresas` (
  `ID_REGISTRO` int(11) NOT NULL,
  `NOTA` varchar(350) NOT NULL,
  `RUT_EMPRESA` varchar(12) NOT NULL,
  `CORREO` varchar(150) NOT NULL,
  `FECHA_CREACION` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `ID_SERVICIO` int(11) NOT NULL,
  `NOMBRE_SERVICIO` varchar(150) NOT NULL,
  `DESCRIPCION` varchar(250) DEFAULT NULL,
  `FECHA_INICIO` date NOT NULL,
  `FECHA_TERMINO` date DEFAULT NULL,
  `ID_ESTADO` int(11) NOT NULL,
  `PRECIO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`ID_SERVICIO`, `NOMBRE_SERVICIO`, `DESCRIPCION`, `FECHA_INICIO`, `FECHA_TERMINO`, `ID_ESTADO`, `PRECIO`) VALUES
(10, 'Mamá esta presa', 'Alguina descripcion que quiera', '2022-09-27', '2022-10-27', 2, 90000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `serviciosdiarios`
--

CREATE TABLE `serviciosdiarios` (
  `ID_SERVICIOS_DIARIOS` int(11) NOT NULL,
  `NOMBRE_SERVICIO` varchar(100) NOT NULL,
  `ID_ESTADO` int(1) NOT NULL,
  `PRECIO` int(11) NOT NULL,
  `FECHA_SEMANA` varchar(6) NOT NULL,
  `URL_POSICION` varchar(250) DEFAULT NULL,
  `UBICACION` varchar(250) NOT NULL,
  `RUT_USUARIO` varchar(12) NOT NULL,
  `RUT_TRABAJADOR` varchar(12) NOT NULL,
  `DESCR` varchar(250) DEFAULT NULL,
  `TODA_SEMANA` tinyint(1) NOT NULL DEFAULT 1,
  `ID_PRODUCTO` int(11) NOT NULL,
  `CANTIDAD` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `serviciosdiarios`
--

INSERT INTO `serviciosdiarios` (`ID_SERVICIOS_DIARIOS`, `NOMBRE_SERVICIO`, `ID_ESTADO`, `PRECIO`, `FECHA_SEMANA`, `URL_POSICION`, `UBICACION`, `RUT_USUARIO`, `RUT_TRABAJADOR`, `DESCR`, `TODA_SEMANA`, `ID_PRODUCTO`, `CANTIDAD`) VALUES
(2, 'Tongoy', 1, 9000, '27', NULL, 'av matta', '18.881.495-6', '18.881.495-6', NULL, 1, 3, 4),
(3, 'San Miguel', 3, 12000, '234567', NULL, 'av chiloe ', '18.881.495-6', '18.881.495-6', NULL, 1, 3, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajadores`
--

CREATE TABLE `trabajadores` (
  `RUT` varchar(12) NOT NULL,
  `ID_LOCAL` int(11) NOT NULL,
  `SUELDO` int(8) NOT NULL,
  `DIA_PAGO` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `trabajadores`
--

INSERT INTO `trabajadores` (`RUT`, `ID_LOCAL`, `SUELDO`, `DIA_PAGO`) VALUES
('18.881.495-6', 7, 550000, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `CORREO` varchar(150) NOT NULL,
  `CONTRASEÑA` varchar(150) NOT NULL,
  `FECHA_CREACION` date NOT NULL DEFAULT current_timestamp(),
  `ESTADO` int(1) NOT NULL DEFAULT 1,
  `GRUPOS` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`CORREO`, `CONTRASEÑA`, `FECHA_CREACION`, `ESTADO`, `GRUPOS`) VALUES
('arkinommo@gmail.com', '8cb2237d0679ca88db6464eac60da96345513964', '2022-09-29', 1, 1),
('mpino1701@gmail.com', 'dd3105f5a40070eaff30001b545b224bce14eaba', '2022-09-16', 1, 5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `empresas`
--
ALTER TABLE `empresas`
  ADD PRIMARY KEY (`RUT_EMPRESA`);

--
-- Indices de la tabla `estados`
--
ALTER TABLE `estados`
  ADD PRIMARY KEY (`ID_ESTADO`);

--
-- Indices de la tabla `locales`
--
ALTER TABLE `locales`
  ADD PRIMARY KEY (`ID_LOCAL`);

--
-- Indices de la tabla `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`RUT`),
  ADD KEY `PERSONAS_USUARIOS` (`CORREO`),
  ADD KEY `rut_empresas_personas_empresas` (`RUT_EMPRESA`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`ID_PRODUCTO`);

--
-- Indices de la tabla `registro_notas_empresas`
--
ALTER TABLE `registro_notas_empresas`
  ADD PRIMARY KEY (`ID_REGISTRO`),
  ADD KEY `NOTAS_EMRPESAS` (`RUT_EMPRESA`),
  ADD KEY `NOTAS_USUARIOS` (`CORREO`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`ID_SERVICIO`),
  ADD KEY `SERVICIOS_ESTADOS` (`ID_ESTADO`);

--
-- Indices de la tabla `serviciosdiarios`
--
ALTER TABLE `serviciosdiarios`
  ADD PRIMARY KEY (`ID_SERVICIOS_DIARIOS`),
  ADD KEY `SERVICIOS_DIARIOS_PRODUCTOS` (`ID_PRODUCTO`),
  ADD KEY `SERVICIOS_DIARIOS_ESTADOS` (`ID_ESTADO`),
  ADD KEY `SERVICIOS_DIARIOS_TRABAJADOR` (`RUT_TRABAJADOR`),
  ADD KEY `SERVICIOS_DARIOS_PERSONAS` (`RUT_USUARIO`);

--
-- Indices de la tabla `trabajadores`
--
ALTER TABLE `trabajadores`
  ADD PRIMARY KEY (`RUT`),
  ADD KEY `TRABAJADORES_LOCALES` (`ID_LOCAL`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`CORREO`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `estados`
--
ALTER TABLE `estados`
  MODIFY `ID_ESTADO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `locales`
--
ALTER TABLE `locales`
  MODIFY `ID_LOCAL` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `ID_PRODUCTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `registro_notas_empresas`
--
ALTER TABLE `registro_notas_empresas`
  MODIFY `ID_REGISTRO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `ID_SERVICIO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `serviciosdiarios`
--
ALTER TABLE `serviciosdiarios`
  MODIFY `ID_SERVICIOS_DIARIOS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `personas`
--
ALTER TABLE `personas`
  ADD CONSTRAINT `personas_usuarios_correo` FOREIGN KEY (`CORREO`) REFERENCES `usuarios` (`CORREO`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rut_empresas_personas_empresas` FOREIGN KEY (`RUT_EMPRESA`) REFERENCES `empresas` (`RUT_EMPRESA`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `registro_notas_empresas`
--
ALTER TABLE `registro_notas_empresas`
  ADD CONSTRAINT `NOTAS_EMRPESAS` FOREIGN KEY (`RUT_EMPRESA`) REFERENCES `empresas` (`RUT_EMPRESA`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `NOTAS_USUARIOS` FOREIGN KEY (`CORREO`) REFERENCES `usuarios` (`CORREO`) ON DELETE CASCADE;

--
-- Filtros para la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD CONSTRAINT `SERVICIOS_ESTADOS` FOREIGN KEY (`ID_ESTADO`) REFERENCES `estados` (`ID_ESTADO`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `serviciosdiarios`
--
ALTER TABLE `serviciosdiarios`
  ADD CONSTRAINT `SERVICIOS_DARIOS_PERSONAS` FOREIGN KEY (`RUT_USUARIO`) REFERENCES `personas` (`RUT`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `SERVICIOS_DIARIOS_ESTADOS` FOREIGN KEY (`ID_ESTADO`) REFERENCES `estados` (`ID_ESTADO`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `SERVICIOS_DIARIOS_PRODUCTOS` FOREIGN KEY (`ID_PRODUCTO`) REFERENCES `productos` (`ID_PRODUCTO`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `SERVICIOS_DIARIOS_TRABAJADOR` FOREIGN KEY (`RUT_TRABAJADOR`) REFERENCES `trabajadores` (`RUT`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `trabajadores`
--
ALTER TABLE `trabajadores`
  ADD CONSTRAINT `TRABAJADORES_LOCALES` FOREIGN KEY (`ID_LOCAL`) REFERENCES `locales` (`ID_LOCAL`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `TRABAJADORES_PERSONAS` FOREIGN KEY (`RUT`) REFERENCES `personas` (`RUT`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
