-- Tabla para almacenar los precios de cada mantenimiento
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
