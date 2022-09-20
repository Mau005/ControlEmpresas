-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 20-09-2022 a las 02:14:38
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `CE`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ACCESOS`
--

CREATE TABLE `ACCESOS` (
  `CORREO` varchar(150) NOT NULL,
  `CREAR` tinyint(1) NOT NULL DEFAULT 0,
  `EDITAR` tinyint(1) NOT NULL DEFAULT 0,
  `BANEAR` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ACCESOS`
--

INSERT INTO `ACCESOS` (`CORREO`, `CREAR`, `EDITAR`, `BANEAR`) VALUES
('mpino1701@gmail.com', 0, 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `EMPRESAS`
--

CREATE TABLE `EMPRESAS` (
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
-- Volcado de datos para la tabla `EMPRESAS`
--

INSERT INTO `EMPRESAS` (`RUT_EMPRESA`, `NOMBRE_EMPRESA`, `GIRO_EMPRESA`, `DIRECCION`, `TELEFONO`, `CORREO_EMPRESA`, `CORREO_RESPALDO`, `CELULAR_EMPRESA`) VALUES
('11.111.111-1', '123123', '11.111.111-1', '11.111.111-1', '11.111.111-1', 'ejemplo@tudominio.cl', 'ejemplo@tudominio.cl', '11.111.111-1'),
('11.111.111-2', 'juansico', 'prueba1', 'prueba1', 'prueba12', 'ejemplo@ejemplo.cl', 'ejemplo@ejemplo.cl', 'prueba12'),
('11.112.111-2', 'pedritospa', 'prueba1', 'prueba1', 'prueba12', 'ejemplo@ejemplo.cl', 'ejemplo@ejemplo.cl', 'prueba12'),
('11.113.111-2', 'twitch', 'prueba1', 'prueba1', 'prueba12', 'ejemplo@ejemplo.cl', 'ejemplo@ejemplo.cl', 'prueba12'),
('11.114.111-2', 'sdsdsde', 'prueba1', 'prueba1', 'prueba12', 'ejemplo@ejemplo.cl', 'ejemplo@ejemplo.cl', 'prueba12'),
('11.115.111-2', 'None123123', 'prueba1', 'prueba1', 'prueba12', 'ejemplo@ejemplo.cl', 'ejemplo@ejemplo.cl', 'prueba12'),
('44444444-8', 'qweqeqeqweqwe', 'qweqweqweqwewqeqw', 'eqweqweqweqwe', 'qwewqeewq', 'qweqweqweq@eqweqwe', '', 'qweqweqwe'),
('76.634.406-2', 'Los Tres Pinos SPA', 'Arriendo y venta de baños quimicos', 'Michimalongo 14600, la pintana, santiago', '213123123123', 'ventas@lostrespinos.cl', 'ventas@lostrespinos.cl', '+569999999'),
('78845972-4', 'Empresa de Serviciios de tu hermana', 'Arriendo y venta de tu hermana', 'En Av Me importa un Pico', '111111111', 'sdsd@sdadas.cl', '', '11111111'),
('90.440.445-0', 'Roblex Drops', 'Venta de servicios de cuerpos humanos', 'a lado de mi vecina', '', 'tes@roblex.cl', '', '+56940403020');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ESTADOS`
--

CREATE TABLE `ESTADOS` (
  `ID_ESTADO` int(11) NOT NULL,
  `NOMBRE` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ESTADOS`
--

INSERT INTO `ESTADOS` (`ID_ESTADO`, `NOMBRE`) VALUES
(1, 'OPERATIVO'),
(2, 'DETENIDO'),
(3, 'TRANSLADO'),
(4, 'SINIESTRADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `HISTORIAL_BANEOS`
--

CREATE TABLE `HISTORIAL_BANEOS` (
  `CORREO` varchar(150) NOT NULL,
  `DESCR` varchar(250) NOT NULL,
  `FECHA` datetime NOT NULL DEFAULT current_timestamp(),
  `IP` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PERSONAS`
--

CREATE TABLE `PERSONAS` (
  `RUT_PERSONA` varchar(12) NOT NULL,
  `NOMBRES` varchar(150) NOT NULL,
  `APELLIDOS` varchar(150) NOT NULL,
  `TELEFONO` varchar(14) DEFAULT NULL,
  `CELULAR` varchar(14) NOT NULL,
  `CORREO` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `PERSONAS`
--

INSERT INTO `PERSONAS` (`RUT_PERSONA`, `NOMBRES`, `APELLIDOS`, `TELEFONO`, `CELULAR`, `CORREO`) VALUES
('11.111.111-1', '11111111-1', '11111111-1', '11111111-1', '11111111-1', '11111111-1@11111111-1'),
('11.456.890-k', 'Culito zacallama', 'ICL creyo', '', '+56999234455', 'test@test.cl');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `PRODUCTOS`
--

CREATE TABLE `PRODUCTOS` (
  `ID_PRODUCTO` int(11) NOT NULL,
  `NOMBRE_PRODUCTO` varchar(100) NOT NULL,
  `DESCRIPCION` varchar(250) NOT NULL,
  `FECHA_CREACION` datetime NOT NULL DEFAULT current_timestamp(),
  `CANTIDAD` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `PRODUCTOS`
--

INSERT INTO `PRODUCTOS` (`ID_PRODUCTO`, `NOMBRE_PRODUCTO`, `DESCRIPCION`, `FECHA_CREACION`, `CANTIDAD`) VALUES
(1, 'Jabon Adulto', 'Muy resfaloso para que se caiga cada vez que lo tomes en el baño', '2022-09-15 03:43:08', 10),
(2, 'probando un nuevo producto', 'sdaasdas\ndas\nd\nasd\nas\ndas\nda\nsd\nas\ndas\ndas\nd', '2022-09-15 03:51:27', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `REGISTRO_NOTAS_EMRPESAS`
--

CREATE TABLE `REGISTRO_NOTAS_EMRPESAS` (
  `ID_REGISTRO` int(11) NOT NULL,
  `NOTA` varchar(350) NOT NULL,
  `RUT_EMPRESA` varchar(12) NOT NULL,
  `CORREO` varchar(150) NOT NULL,
  `FECHA_CREACION` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `SERVICIOS`
--

CREATE TABLE `SERVICIOS` (
  `ID_SERVICIO` int(11) NOT NULL,
  `NOMBRE_SERVICIO` varchar(150) NOT NULL,
  `DESCRIPCION` varchar(250) DEFAULT NULL,
  `FECHA_INICIO` date NOT NULL,
  `FECHA_TERMINO` date DEFAULT NULL,
  `ID_ESTADO` int(11) NOT NULL,
  `PRECIO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `SERVICIOS`
--

INSERT INTO `SERVICIOS` (`ID_SERVICIO`, `NOMBRE_SERVICIO`, `DESCRIPCION`, `FECHA_INICIO`, `FECHA_TERMINO`, `ID_ESTADO`, `PRECIO`) VALUES
(1, 'test', 'asdasdasd\nasd', '2022-09-13', '2022-09-20', 2, 213123),
(2, 'Claudia Obra', 'Tucapel 13623423', '2022-09-27', '2022-10-27', 2, 90000),
(3, 'Pelao Juanita', 'Ferias keodhaskdjapsd', '2022-09-23', '2022-12-30', 2, 9000),
(4, 'Vanessa', 'asdasd', '2022-09-14', '2022-09-21', 1, 9000),
(5, 'patoods', 'Un usuario de twith', '2022-09-12', '2022-10-12', 1, 90000),
(6, 'sadasd', 'sadasdasd', '2022-09-01', NULL, 1, 12312),
(7, 'asdasdasd', 'asdasdasd', '2022-09-01', NULL, 1, 2131231),
(8, 'Servicio Nuevo en twitch', 'sadasdasd\nasd\nasd\nasd', '2022-09-06', '2022-09-22', 1, 9999999);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `USUARIOS`
--

CREATE TABLE `USUARIOS` (
  `CORREO` varchar(150) NOT NULL,
  `CONTRASEÑA` varchar(150) NOT NULL,
  `FECHA_CREACION` date NOT NULL DEFAULT current_timestamp(),
  `ESTADO` int(1) NOT NULL DEFAULT 1,
  `GRUPOS` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `USUARIOS`
--

INSERT INTO `USUARIOS` (`CORREO`, `CONTRASEÑA`, `FECHA_CREACION`, `ESTADO`, `GRUPOS`) VALUES
('mpino1701@gmail.com', '8dbef3d81542a4ed6f4f7c36e6bcb7c2e16ee9b1', '2022-09-16', 1, 4);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ACCESOS`
--
ALTER TABLE `ACCESOS`
  ADD PRIMARY KEY (`CORREO`);

--
-- Indices de la tabla `EMPRESAS`
--
ALTER TABLE `EMPRESAS`
  ADD PRIMARY KEY (`RUT_EMPRESA`);

--
-- Indices de la tabla `ESTADOS`
--
ALTER TABLE `ESTADOS`
  ADD PRIMARY KEY (`ID_ESTADO`);

--
-- Indices de la tabla `HISTORIAL_BANEOS`
--
ALTER TABLE `HISTORIAL_BANEOS`
  ADD PRIMARY KEY (`CORREO`);

--
-- Indices de la tabla `PERSONAS`
--
ALTER TABLE `PERSONAS`
  ADD PRIMARY KEY (`RUT_PERSONA`),
  ADD KEY `PERSONAS_USUARIOS` (`CORREO`);

--
-- Indices de la tabla `PRODUCTOS`
--
ALTER TABLE `PRODUCTOS`
  ADD PRIMARY KEY (`ID_PRODUCTO`);

--
-- Indices de la tabla `REGISTRO_NOTAS_EMRPESAS`
--
ALTER TABLE `REGISTRO_NOTAS_EMRPESAS`
  ADD PRIMARY KEY (`ID_REGISTRO`),
  ADD KEY `NOTAS_EMRPESAS` (`RUT_EMPRESA`),
  ADD KEY `NOTAS_USUARIOS` (`CORREO`);

--
-- Indices de la tabla `SERVICIOS`
--
ALTER TABLE `SERVICIOS`
  ADD PRIMARY KEY (`ID_SERVICIO`),
  ADD KEY `SERVICIOS_ESTADOS` (`ID_ESTADO`);

--
-- Indices de la tabla `USUARIOS`
--
ALTER TABLE `USUARIOS`
  ADD PRIMARY KEY (`CORREO`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ESTADOS`
--
ALTER TABLE `ESTADOS`
  MODIFY `ID_ESTADO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `PRODUCTOS`
--
ALTER TABLE `PRODUCTOS`
  MODIFY `ID_PRODUCTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `REGISTRO_NOTAS_EMRPESAS`
--
ALTER TABLE `REGISTRO_NOTAS_EMRPESAS`
  MODIFY `ID_REGISTRO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `SERVICIOS`
--
ALTER TABLE `SERVICIOS`
  MODIFY `ID_SERVICIO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ACCESOS`
--
ALTER TABLE `ACCESOS`
  ADD CONSTRAINT `ACCESOS_USUARIOS` FOREIGN KEY (`CORREO`) REFERENCES `USUARIOS` (`CORREO`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `HISTORIAL_BANEOS`
--
ALTER TABLE `HISTORIAL_BANEOS`
  ADD CONSTRAINT `BANEOS_USUARIOS` FOREIGN KEY (`CORREO`) REFERENCES `USUARIOS` (`CORREO`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Filtros para la tabla `REGISTRO_NOTAS_EMRPESAS`
--
ALTER TABLE `REGISTRO_NOTAS_EMRPESAS`
  ADD CONSTRAINT `NOTAS_EMRPESAS` FOREIGN KEY (`RUT_EMPRESA`) REFERENCES `EMPRESAS` (`RUT_EMPRESA`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `NOTAS_USUARIOS` FOREIGN KEY (`CORREO`) REFERENCES `USUARIOS` (`CORREO`) ON DELETE CASCADE;

--
-- Filtros para la tabla `SERVICIOS`
--
ALTER TABLE `SERVICIOS`
  ADD CONSTRAINT `SERVICIOS_ESTADOS` FOREIGN KEY (`ID_ESTADO`) REFERENCES `ESTADOS` (`ID_ESTADO`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
