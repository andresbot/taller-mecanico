PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Cedula TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Telefono TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vehiculos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Placa TEXT NOT NULL,
    Marca TEXT NOT NULL,
    Modelo TEXT NOT NULL,
    linea TEXT,
    Kilometraje INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(ID) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS mantenimientos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id INTEGER NOT NULL,
    tipo_mantenimiento TEXT NOT NULL CHECK (tipo_mantenimiento IN ('cambio_aceite', 'frenos', 'general', 'correctivo')),
    fecha_mantenimiento TEXT NOT NULL,
    kilometraje INTEGER,
    mecanico TEXT,
    observaciones TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cambio_aceite (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL UNIQUE,
    filtro_aceite TEXT,
    filtro_aire TEXT,
    tipo_aceite TEXT,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mantenimiento_frenos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL UNIQUE,
    estado_pastillas TEXT,
    estado_discos TEXT,
    estado_liquido TEXT,
    estado_campanas TEXT,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mantenimiento_general (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL UNIQUE,
    fecha_ultima_correa TEXT,
    estado_luces TEXT,
    estado_frenos TEXT,
    estado_correa_accesorios TEXT,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mantenimiento_correctivo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL UNIQUE,
    detalles_falla TEXT,
    danos_colaterales TEXT,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tipos_mantenimiento_varios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mantenimiento_varios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL,
    tipo_mantenimiento_varios_id INTEGER NOT NULL,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE,
    FOREIGN KEY (tipo_mantenimiento_varios_id) REFERENCES tipos_mantenimiento_varios(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS precios_mantenimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mantenimiento_id INTEGER NOT NULL UNIQUE,
    precio_principal REAL DEFAULT 0.00,
    detalles_adicionales TEXT,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS trg_precios_mantenimiento_fecha_actualizacion
AFTER UPDATE ON precios_mantenimiento
FOR EACH ROW
BEGIN
    UPDATE precios_mantenimiento
    SET fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

CREATE INDEX IF NOT EXISTS idx_vehiculos_cliente_id ON vehiculos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_mantenimientos_vehiculo_id ON mantenimientos(vehiculo_id);
CREATE INDEX IF NOT EXISTS idx_mantenimiento_varios_mantenimiento_id ON mantenimiento_varios(mantenimiento_id);

INSERT OR IGNORE INTO tipos_mantenimiento_varios (ID, nombre) VALUES
    (1, 'CAMBIO DE ACEITE'),
    (2, 'CAMBIO RETEN CAJA'),
    (3, 'CAMBIO BUJES DE TIJERA'),
    (4, 'CAMBIO KIT DE CLUTCH');