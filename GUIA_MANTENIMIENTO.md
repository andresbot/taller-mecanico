# GUIA DE MANTENIMIENTO DEL CODIGO

## 1. INTRODUCCION

Esta guia describe como mantener, actualizar y desplegar el sistema de gestion del taller mecanico en su estado actual.

Estado actual del proyecto:

- Base de datos local con SQLite.
- Creacion automatica de base de datos al iniciar la app.
- Respaldos diarios automaticos.
- Opcion de instalacion en Windows.
- Opcion portable en USB (sin instalar).

---

## 2. ARQUITECTURA ACTUAL

Estructura principal:

- `models/`: acceso a datos y entidades del negocio.
- `controllers/`: logica de negocio.
- `views/`: interfaz Tkinter.
- `services/db_service.py`: conexion SQLite, inicializacion y backup.
- `database_schema.sql`: esquema unificado de base de datos.
- `main.py`: arranque de la aplicacion.

Base de datos:

- Motor: SQLite.
- Archivo principal: `registrodb.sqlite3`.
- Se crea automaticamente con `database_schema.sql` en el primer inicio.

---

## 3. MANTENIMIENTO PREVENTIVO

### 3.1 Control de versiones (Git)

```bash
git checkout -b feature/nueva-funcionalidad
# ... cambios ...
git add .
git commit -m "Feature: descripcion clara"
git checkout main
git merge feature/nueva-funcionalidad
```

### 3.2 Respaldos

La app ya realiza respaldo diario automatico.

Adicionalmente, para respaldo manual rapido, copia el archivo de base de datos (`registrodb.sqlite3`) a una carpeta externa.

Recomendado antes de cambios grandes:

- Cambios en `database_schema.sql`.
- Cambios en modelos/controladores.
- Nueva version para usuarios.

### 3.3 Dependencias

```bash
pip install -r requirements.txt
```

Si actualizas paquetes, prueba toda la app antes de publicar una nueva version.

---

## 4. MANTENIMIENTO CORRECTIVO (ERRORES)

Proceso sugerido:

1. Reproducir el error.
2. Revisar traceback completo.
3. Corregir en capa correcta:
   - `models/`: errores de datos/consultas.
   - `controllers/`: reglas de negocio.
   - `views/`: formularios/interfaz.
   - `services/`: conexion/infraestructura.
4. Probar que el error desaparece.
5. Verificar que no se rompan otras funcionalidades.

Debug rapido:

```python
try:
    # codigo
    pass
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## 5. MANTENIMIENTO EVOLUTIVO (NUEVAS FUNCIONES)

Cuando agregues una nueva funcion:

1. Actualiza `database_schema.sql` (si requiere datos nuevos).
2. Actualiza `models/`.
3. Actualiza `controllers/`.
4. Actualiza `views/`.
5. Prueba flujos de crear/editar/eliminar/consultar.
6. Actualiza esta guia y `README.md` si cambia despliegue o uso.

Notas para SQLite:

- Placeholder de consultas: la app soporta `%s` de forma transparente desde `DatabaseService`.
- Si agregas columnas/tablas, usa SQL compatible con SQLite.

---

## 6. DESPLIEGUE EN WINDOWS (EJECUTABLE)

### 6.1 Requisitos en PC de build

- Windows 10/11.
- Python 3 instalado y agregado al PATH.
- Proyecto descargado.

### 6.2 Generar ejecutable

Desde la raiz del proyecto, ejecutar:

```bat
scripts\build_windows.bat
```

Este script hace:

1. Instala dependencias.
2. Construye `dist/TallerMecanico.exe`.
3. Crea paquete portable en `dist/portable/TallerMecanicoPortable/`.

### 6.3 Crear instalador (opcional recomendado)

1. Instalar Inno Setup.
2. Abrir `installer/TallerMecanico.iss`.
3. Compilar.

Salida esperada:

- `installer/output/TallerMecanico-Setup.exe`.

---

## 7. MODOS DE ENTREGA AL USUARIO

### 7.1 Modo instalado (recomendado para uso diario)

Entregar:

- `TallerMecanico-Setup.exe`.

Usuario final:

1. Doble clic en instalador.
2. Siguiente, siguiente, finalizar.
3. Abrir desde acceso directo `TallerMecanico`.

### 7.2 Modo USB portable (sin instalar)

Entregar carpeta:

- `dist/portable/TallerMecanicoPortable/`

Usuario final:

1. Abrir carpeta en USB.
2. Doble clic en `ABRIR_TALLER.bat`.
3. Usar normalmente.

Importante:

- En Windows moderno no se permite auto-ejecucion al conectar USB.
- Siempre se debe abrir manualmente con doble clic.

---

## 8. LISTA DE VERIFICACION ANTES DE PUBLICAR

- [ ] `database_schema.sql` actualizado.
- [ ] Sin errores en editor.
- [ ] Flujo clientes/vehiculos/mantenimientos probado.
- [ ] Exportes y reportes probados.
- [ ] Build `scripts\\build_windows.bat` exitoso.
- [ ] Instalador compilado (si aplica).
- [ ] Guia usuario actualizada (`GUIA_USUARIO_FINAL.md`).
- [ ] Guia imprimible actualizada (`GUIA_USUARIO_IMPRIMIR.html`).

---

## 9. SOLUCION DE PROBLEMAS FRECUENTES

### 9.1 El ejecutable no abre

- Ejecutar desde terminal para ver error.
- Verificar antivirus/SmartScreen.
- Regenerar con `scripts\\build_windows.bat`.

### 9.2 Error de base de datos

- Verificar que existe `database_schema.sql` en el proyecto/bundle.
- Revisar permisos de escritura en el equipo o USB.
- Probar reiniciar app (genera estructura automaticamente).

### 9.3 Usuario reporta perdida de datos

- Revisar respaldos automaticos del dia.
- Restaurar copiando respaldo sobre la base actual con la app cerrada.

---

## 10. REFERENCIAS

- Python: https://docs.python.org/3/
- Tkinter: https://docs.python.org/3/library/tkinter.html
- SQLite: https://www.sqlite.org/docs.html
- PyInstaller: https://pyinstaller.org/
- Inno Setup: https://jrsoftware.org/isinfo.php

---

Ultima actualizacion: 2026-04-20
Version de la guia: 2.0
