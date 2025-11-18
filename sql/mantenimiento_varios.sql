-- Tabla para tipos de mantenimiento varios
CREATE TABLE IF NOT EXISTS tipos_mantenimiento_varios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla para relacionar mantenimientos con tipos varios
CREATE TABLE IF NOT EXISTS mantenimiento_varios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT NOT NULL,
    tipo_mantenimiento_varios_id INT NOT NULL,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(ID) ON DELETE CASCADE,
    FOREIGN KEY (tipo_mantenimiento_varios_id) REFERENCES tipos_mantenimiento_varios(ID) ON DELETE CASCADE
);

-- Insertar algunos tipos comunes
INSERT IGNORE INTO tipos_mantenimiento_varios (nombre) VALUES 
('CAMBIO DE ACEITE'),
('CAMBIO RETEN CAJA'),
('CAMBIO BUJES DE TIJERA'),
('CAMBIO KIT DE CLUTCH');