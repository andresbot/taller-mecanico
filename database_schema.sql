-- Existing table (assumed structure based on the code)
CREATE TABLE IF NOT EXISTS usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR(20),
    Nombre VARCHAR(100),
    Telefono VARCHAR(20),
    Fecha DATE,
    Placa VARCHAR(20),
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Kilometraje INT
);

-- New table for maintenance records
CREATE TABLE IF NOT EXISTS mantenimientos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT,
    tipo_mantenimiento ENUM('cambio_aceite', 'frenos', 'general', 'correctivo'),
    fecha_mantenimiento DATE,
    kilometraje INT,
    mecanico VARCHAR(100),
    observaciones TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES usuarios(ID)
);

-- Table for oil changes
CREATE TABLE IF NOT EXISTS cambio_aceite (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT,
    filtro_aceite VARCHAR(50),
    filtro_aire VARCHAR(50),
    tipo_aceite VARCHAR(50),
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID)
);

-- Table for brake maintenance
CREATE TABLE IF NOT EXISTS mantenimiento_frenos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT,
    estado_pastillas VARCHAR(50),
    estado_discos VARCHAR(50),
    estado_liquido VARCHAR(50),
    estado_campanas VARCHAR(50),
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID)
);

-- Table for general maintenance
CREATE TABLE IF NOT EXISTS mantenimiento_general (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT,
    fecha_ultima_correa DATE,
    estado_luces VARCHAR(100),
    estado_frenos VARCHAR(100),
    estado_correa_accesorios VARCHAR(100),
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID)
);

-- Table for corrective maintenance
CREATE TABLE IF NOT EXISTS mantenimiento_correctivo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT,
    detalles_falla TEXT,
    danos_colaterales TEXT,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID)
);