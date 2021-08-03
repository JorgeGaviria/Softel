instructions=[
    'SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";',
    'SET AUTOCOMMIT = 0;',
    'START TRANSACTION;',
    'SET time_zone = "+00:00";',

    """
        CREATE TABLE `tbl_cliente` (
            `idtbl_cliente` int auto_increment primary key,
            `dni` varchar(15) NOT NULL,
            `nombres` char(30) COLLATE utf8_spanish2_ci NOT NULL,
            `apellidos` char(30) COLLATE utf8_spanish2_ci NOT NULL,
            `fecha_nacimiento` date NOT NULL,
            `nacionalidad` int(11) COLLATE utf8_spanish2_ci NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        CREATE TABLE `tbl_paises` (
            `idtbl_paises` int(11) NOT NULL AUTO_INCREMENT,
            `iso` char(2) DEFAULT NULL,
            `nombre` varchar(80) DEFAULT NULL,
            PRIMARY KEY (`idtbl_paises`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
    """,

    """
        CREATE TABLE `tbl_empleado` (
            `idtbl_empleado` int auto_increment primary key not null,
            `dni` varchar(15) NOT NULL ,
            `nombres` char(30) COLLATE utf8_spanish2_ci NOT NULL,
            `apellidos` char(30) COLLATE utf8_spanish2_ci NOT NULL,
            `cargo` int(11) COLLATE utf8_spanish2_ci NOT NULL,
            `pass` varchar(255) COLLATE utf8_spanish2_ci NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        CREATE TABLE `tbl_factura` (
            `idtbl_factura` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `fecha_impresion` date NOT NULL,
            `descuentos` varchar(45) COLLATE utf8_spanish2_ci NULL,
            `total` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `idtbl_producto` int(11) NOT NULL,
            `idtbl_reserva` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        CREATE TABLE `tbl_habitacion` (
            `idtbl_habitacion` int(11) NOT NULL  PRIMARY KEY AUTO_INCREMENT,
            `nombre` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `valor` bigint(10) NOT NULL,
            `capacidad` int(2) NOT NULL,
            `foto` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
            `estado` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `descripcion` varchar(200) COLLATE utf8_spanish2_ci NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        CREATE TABLE `tbl_producto` (
            `idtbl_producto` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `nombre` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `precio` bigint(10) NOT NULL,
            `descripcion` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `imagen` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
            `categoria` int(11) not null
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        CREATE TABLE `tbl_categoria` (
        `idtbl_categoria` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `nombre` varchar(30) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

    """,
    """
        CREATE TABLE `tbl_reserva` (
            `idtbl_reserva` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
            `fecha_inicio` date NOT NULL,
            `fecha_fin` date NOT NULL,
            `estado` varchar(45) COLLATE utf8_spanish2_ci NOT NULL,
            `habitacion` int(11) NOT NULL,
            `empleado` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;
    """,

    """
        create table `tbl_cargo` (
            `idtbl_cargo` int(11) not null primary key auto_increment,
            `nombre` varchar(20) not null
        );
    """,

    """
        create table tbl_fotos(
            idtbl_fotos int AUTO_INCREMENT PRIMARY KEY,
            habitacion int not null,
            nombre varchar(100) not null,
            ruta varchar(260) not null
        );
    """,
    
    """
        alter table tbl_fotos ADD CONSTRAINT fk_tbl_fotos_tbl_habitacion FOREIGN key (habitacion) REFERENCES tbl_habitacion(idtbl_habitacion);
    """,


    """
        alter table tbl_cliente add constraint fk_tbl_cliente_tbl_paises foreign key (nacionalidad) references tbl_paises(idtbl_paises)
    """,

    """
        alter table tbl_reserva add constraint fk_tbl_reserva_tbl_empleado foreign key (empleado) references tbl_empleado(idtbl_empleado);
    """,
        
    """
     alter table tbl_reserva add constraint fk_tbl_reserva_tbl_habitacion foreign key (habitacion) references tbl_habitacion(idtbl_habitacion);
    """,

    """
        alter table tbl_factura add constraint fk_tbl_factura_tbl_reserva foreign key (idtbl_reserva) references tbl_reserva(idtbl_reserva);
    """,

    """
        alter table tbl_factura add constraint fk_tbl_factura_tbl_producto foreign key (idtbl_producto) references tbl_producto(idtbl_producto);
    """,

    """
        alter table tbl_producto add constraint fk_tbl_producto_tbl_categoria foreign key (categoria) references tbl_categoria(idtbl_categoria);
    """,

    """
        alter table tbl_empleado add CONSTRAINT fk_tbl_empleado_tbl_cargo FOREIGN key (cargo) REFERENCES tbl_cargo(idtbl_cargo)
    """,

    """
       create table tbl_cliente_reserva(
            idtbl_cliente_reserva int not null PRIMARY KEY AUTO_INCREMENT,
            cliente int(11) not null,
            reserva int(11) not null
        );
    """,    
    """
        alter table tbl_cliente_reserva ADD CONSTRAINT fk_tbl_cliente_reserva_tbl_cliente FOREIGN key(cliente) REFERENCES tbl_cliente(idtbl_cliente);
    """,

    """
        alter table tbl_cliente_reserva ADD CONSTRAINT fk_tbl_cliente_reserva_tbl_reserva FOREIGN key(reserva) REFERENCES tbl_reserva(idtbl_reserva);
    """
]