-- Tabla para almacenar los precios de cada mantenimiento
CREATE TABLE IF NOT EXISTS precios_mantenimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mantenimiento_id INT NOT NULL,
    precio_principal DECIMAL(10, 2) DEFAULT 0.00,
    detalles_adicionales TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (mantenimiento_id) REFERENCES mantenimientos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_mantenimiento (mantenimiento_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
