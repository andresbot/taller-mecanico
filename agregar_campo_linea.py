"""
Script para agregar la columna 'linea' a la tabla usuarios
Ejecutar este archivo una sola vez después de actualizar el código
"""
from services.db_service import DatabaseService
import mysql.connector

def agregar_columna_linea():
    try:
        # Verificar si la columna ya existe
        import mysql.connector
        connection = mysql.connector.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            database="registrodb",
            port="3306"
        )
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SHOW COLUMNS FROM vehiculos LIKE 'linea'")
        result = cursor.fetchall()
        
        if result:
            print("⚠️  La columna 'linea' ya existe en la tabla vehiculos")
            cursor.close()
            connection.close()
            return
        
        # Agregar la columna
        cursor.execute("ALTER TABLE vehiculos ADD COLUMN linea VARCHAR(50) AFTER Modelo")
        connection.commit()
        
        print("✓ Columna 'linea' agregada exitosamente a la tabla vehiculos")
        
        # Verificar
        cursor.execute("DESCRIBE vehiculos")
        columns = cursor.fetchall()
        print("\n📋 Estructura actual de la tabla vehiculos:")
        for col in columns:
            print(f"  - {col['Field']}: {col['Type']}")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"✗ Error al agregar columna: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

if __name__ == "__main__":
    print("Agregando columna 'linea' a la tabla vehiculos...")
    agregar_columna_linea()
    print("\nProceso completado")
