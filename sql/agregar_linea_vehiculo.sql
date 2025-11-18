-- Script para agregar el campo "linea" a la tabla de vehiculos
-- Ejecutar este script una sola vez

ALTER TABLE vehiculos 
ADD COLUMN linea VARCHAR(50) AFTER Modelo;

-- Verificar que se agregó correctamente
DESCRIBE vehiculos;
