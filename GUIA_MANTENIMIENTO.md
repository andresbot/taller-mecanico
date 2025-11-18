# 📖 GUÍA DE MANTENIMIENTO DEL CÓDIGO

## 🎯 INTRODUCCIÓN

Esta guía explica cómo mantener y actualizar el sistema de gestión de mantenimiento de vehículos.

---

## 🔧 TIPOS DE MANTENIMIENTO

### 1. **MANTENIMIENTO PREVENTIVO**
Acciones regulares para evitar problemas futuros.

#### A. **Control de Versiones con GIT**

```bash
# Inicializar repositorio (primera vez)
git init
git add .
git commit -m "Versión inicial del proyecto"

# Crear rama para nueva funcionalidad
git checkout -b feature/nombre-funcionalidad
# ... realizar cambios ...
git add .
git commit -m "Descripción clara de los cambios"

# Volver a main y fusionar
git checkout main
git merge feature/nombre-funcionalidad

# Crear tags para versiones
git tag -a v1.0.0 -m "Versión 1.0.0 - Primera versión estable"
git push origin --tags
```

#### B. **Respaldos de Base de Datos**

```bash
# Hacer backup manual (ejecutar periódicamente)
mysqldump -u root -p registrodb > backup_$(date +%Y%m%d).sql

# Backup de solo estructura
mysqldump -u root -p --no-data registrodb > estructura_$(date +%Y%m%d).sql

# Restaurar desde backup
mysql -u root -p registrodb < backup_20250105.sql
```

**Recomendación**: Hacer backup antes de:
- Actualizar la estructura de la base de datos
- Desplegar a producción
- Hacer cambios importantes

#### C. **Actualización de Dependencias**

```bash
# Ver dependencias actuales y sus versiones
pip list

# Ver dependencias desactualizadas
pip list --outdated

# Actualizar una dependencia específica
pip install --upgrade nombre-paquete

# Actualizar todas (CON PRECAUCIÓN)
pip install --upgrade -r requirements.txt

# Actualizar requirements.txt
pip freeze > requirements.txt
```

**Proceso seguro de actualización**:
1. Crear backup de la aplicación
2. Actualizar UNA dependencia a la vez
3. Probar la aplicación
4. Si funciona, actualizar requirements.txt
5. Si falla, revertir: `pip install nombre-paquete==version-anterior`

---

### 2. **MANTENIMIENTO CORRECTIVO**
Solución de errores y bugs.

#### Proceso de Solución de Errores:

```
1. IDENTIFICAR
   └─> Reproducir el error
   └─> Capturar el mensaje de error completo
   └─> Identificar en qué parte del código ocurre

2. UBICAR
   └─> Revisar el archivo indicado en el error
   └─> Buscar el método/función problemática
   └─> Entender el contexto del código

3. CORREGIR
   └─> Aplicar la solución según la arquitectura MVC:
       ├─> models/ → Errores de datos/base de datos
       ├─> views/ → Errores de interfaz/visualización
       ├─> controllers/ → Errores de lógica de negocio
       └─> services/ → Errores de servicios (BD, etc.)

4. PROBAR
   └─> Reproducir el escenario que causaba el error
   └─> Verificar que ya no ocurre
   └─> Verificar que no se rompió otra funcionalidad

5. DOCUMENTAR
   └─> Comentar el cambio en el código
   └─> Actualizar el commit de git
```

#### Herramientas de Debugging:

```python
# Agregar prints para debugging
print(f"DEBUG: Variable x = {x}")

# Usar try-except para capturar errores
try:
    # código problemático
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

---

### 3. **MANTENIMIENTO EVOLUTIVO**
Agregar nuevas funcionalidades.

#### Proceso Completo (Ejemplo: Agregar "Línea del Vehículo"):

##### PASO 1: Modificar la Base de Datos

```python
# Crear script: agregar_campo_linea.py
import mysql.connector

def agregar_columna_linea():
    try:
        connection = mysql.connector.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            database="registrodb",
            port="3306"
        )
        cursor = connection.cursor(dictionary=True)
        
        # Verificar si ya existe
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'linea'")
        if cursor.fetchall():
            print("⚠️  La columna ya existe")
            return
        
        # Agregar columna
        cursor.execute("ALTER TABLE usuarios ADD COLUMN linea VARCHAR(50) AFTER Modelo")
        connection.commit()
        print("✓ Columna agregada")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

agregar_columna_linea()
```

**Ejecutar**: `python agregar_campo_linea.py`

##### PASO 2: Actualizar el Modelo

Archivo: `models/vehiculo_model.py`

```python
# 1. Agregar parámetro al __init__
def __init__(self, placa=None, marca=None, modelo=None, linea=None, ...):
    ...
    self.linea = linea

# 2. Actualizar método save()
query = """
    INSERT INTO vehiculos (Placa, Marca, Modelo, linea, ...)
    VALUES (%s, %s, %s, %s, ...)
"""
params = (self.placa, self.marca, self.modelo, self.linea, ...)

# 3. Actualizar método update()
query = """
    UPDATE vehiculos 
    SET Placa = %s, Marca = %s, Modelo = %s, linea = %s, ...
    WHERE ID = %s
"""

# 4. Actualizar métodos de consulta (get_all, get_by_id, etc.)
query = "SELECT ID, Placa, Marca, Modelo, linea, ... FROM vehiculos"
formatted_result = {
    ...
    'linea': result.get('linea', ''),
    ...
}
```

##### PASO 3: Actualizar el Controlador

Archivo: `controllers/vehiculo_controller.py`

```python
# Agregar parámetro a create()
def create(self, placa, marca, modelo, linea, ...):
    vehiculo = Vehiculo(
        placa=placa,
        marca=marca,
        modelo=modelo,
        linea=linea,
        ...
    )
    return vehiculo.save()

# Agregar parámetro a update()
def update(self, id, placa, marca, modelo, linea, ...):
    vehiculo = Vehiculo(
        id=id,
        ...
        linea=linea,
        ...
    )
    return vehiculo.update()
```

##### PASO 4: Actualizar la Vista

Archivo: `views/vehiculo_view.py`

```python
# 1. Agregar variable en setup_ui()
self.linea_var = StringVar()

# 2. Agregar campo en el formulario
ttk.Label(data_frame, text="Línea:").grid(row=4, column=0, sticky="w")
linea_entry = ttk.Entry(data_frame, textvariable=self.linea_var)
linea_entry.grid(row=4, column=1, padx=5, pady=2)
linea_entry.bind('<KeyRelease>', lambda e: self.validar_linea(self.linea_var))

# 3. Agregar columna a la tabla
self.tree = ttk.Treeview(table_frame, columns=(
    "Placa", "Marca", "Modelo", "Línea", "Kilometraje", "Cliente"
), ...)

self.tree.heading("Línea", text="Línea", anchor="center")
self.tree.column("Línea", width=100, anchor="center")

# 4. Actualizar load_data()
self.tree.insert("", "end", values=(
    vehiculo.placa,
    vehiculo.marca,
    vehiculo.modelo,
    vehiculo.linea or "",
    ...
))

# 5. Actualizar clear_fields()
self.linea_var.set("")

# 6. Actualizar save() y update()
linea = self.linea_var.get().strip()
self.controller.create(
    ...
    linea=linea,
    ...
)

# 7. Actualizar on_select()
self.linea_var.set(values[3])

# 8. Agregar validación
def validar_linea(self, variable):
    valor = variable.get()
    valor_limpio = ''.join(c for c in valor if c.isalnum() or c.isspace() or c in '-')
    valor_limpio = valor_limpio.upper()
    if valor != valor_limpio:
        variable.set(valor_limpio)
```

##### PASO 5: Probar

```bash
# Verificar errores
python -m py_compile views/vehiculo_view.py
python -m py_compile models/vehiculo_model.py
python -m py_compile controllers/vehiculo_controller.py

# Ejecutar aplicación
python main.py

# Probar:
# 1. Crear un vehículo nuevo con línea
# 2. Editar un vehículo y agregar línea
# 3. Verificar que se muestra en la tabla
# 4. Buscar un vehículo y verificar que se carga el campo
```

---

## 🚀 PREPARACIÓN PARA PRODUCCIÓN

### 1. **Lista de Verificación Pre-Despliegue**

```
□ Todos los archivos obsoletos eliminados
□ Backup de base de datos realizado
□ requirements.txt actualizado
□ Sin errores de sintaxis (ejecutar compilación)
□ Todas las validaciones funcionando
□ Tests manuales completados
□ Documentación actualizada
□ Variables de configuración verificadas
□ Credenciales de BD configuradas para producción
```

### 2. **Configurar para Producción**

Crear archivo: `config.py`

```python
import os

class Config:
    # Desarrollo
    DEBUG = True
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = "root"
    DB_NAME = "registrodb"
    DB_PORT = "3306"

class ProductionConfig(Config):
    # Producción
    DEBUG = False
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "usuario_prod")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password_seguro")
    DB_NAME = os.getenv("DB_NAME", "registrodb_prod")
    DB_PORT = os.getenv("DB_PORT", "3306")
```

Usar en `services/db_service.py`:

```python
from config import ProductionConfig as Config

connection = mysql.connector.connect(
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    host=Config.DB_HOST,
    database=Config.DB_NAME,
    port=Config.DB_PORT
)
```

### 3. **Crear Ejecutable**

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --icon=icono.ico main.py

# El ejecutable estará en: dist/main.exe
```

---

## 📝 BUENAS PRÁCTICAS

### 1. **Documentación del Código**

```python
def metodo_ejemplo(parametro1, parametro2):
    """
    Descripción breve del método.
    
    Args:
        parametro1 (tipo): Descripción del parámetro 1
        parametro2 (tipo): Descripción del parámetro 2
    
    Returns:
        tipo: Descripción de lo que retorna
    
    Raises:
        TipoError: Cuando ocurre X condición
    """
    # Código aquí
    pass
```

### 2. **Nombres Descriptivos**

```python
# ❌ Malo
def f(x, y):
    return x + y

# ✓ Bueno
def calcular_total_precio(precio_base, impuesto):
    return precio_base + impuesto
```

### 3. **Commits Descriptivos**

```bash
# ❌ Malo
git commit -m "fix"
git commit -m "cambios"

# ✓ Bueno
git commit -m "Fix: Corregir cálculo de total en precios"
git commit -m "Feature: Agregar campo línea a vehículos"
git commit -m "Refactor: Mejorar validación de campos numéricos"
```

### 4. **Manejo de Errores**

```python
# Siempre usar try-except en operaciones que pueden fallar
try:
    resultado = operacion_que_puede_fallar()
    self.show_info("Operación exitosa")
except ValueError as e:
    self.show_error(f"Error de valor: {e}")
except Exception as e:
    self.show_error(f"Error inesperado: {e}")
    # Opcional: logging para debugging
    import logging
    logging.error(f"Error en método_X: {e}", exc_info=True)
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "Module not found"
```bash
# Verificar instalación
pip list | grep nombre-modulo

# Reinstalar
pip install nombre-modulo
```

### Error: "Can't connect to MySQL"
```bash
# Verificar que MySQL esté corriendo
# En Windows: Services → MySQL80 → Start

# Verificar credenciales en db_service.py
```

### Error: "Column doesn't exist"
```bash
# Verificar estructura de tabla
mysql -u root -p
USE registrodb;
DESCRIBE nombre_tabla;

# Si falta columna, ejecutar script ALTER TABLE
```

---

## 📚 RECURSOS ADICIONALES

- **Python Documentation**: https://docs.python.org/3/
- **Tkinter Documentation**: https://docs.python.org/3/library/tkinter.html
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Git Documentation**: https://git-scm.com/doc

---

## ✅ RESUMEN DEL PROCESO

1. **Planificar** el cambio
2. **Hacer backup** (código y BD)
3. **Modificar BD** (si necesario)
4. **Actualizar Modelo** (models/)
5. **Actualizar Controlador** (controllers/)
6. **Actualizar Vista** (views/)
7. **Probar** exhaustivamente
8. **Documentar** el cambio
9. **Commit** a git
10. **Desplegar** si todo funciona

---

**Fecha de creación**: 5 de Noviembre, 2025
**Última actualización**: 5 de Noviembre, 2025
**Versión**: 1.0
