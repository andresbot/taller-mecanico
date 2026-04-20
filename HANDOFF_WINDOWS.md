# Handoff Para IA De Windows

## Objetivo

1. Generar ejecutable para Windows.
2. Generar instalador con Inno Setup.
3. Validar instalacion real en PC sin USB.
4. Entregar paquete final para usuario no tecnico.

## Estado Actual Del Proyecto (Ya Hecho En Linux)

1. Migracion a SQLite completada.
2. Esquema unificado y autocreacion de BD al iniciar.
3. Backups diarios automaticos.
4. Modo instalado + modo portable USB.
5. Guias de usuario simplificadas.

## Archivos Clave Ya Preparados

1. `services/db_service.py`
2. `database_schema.sql`
3. `main.py`
4. `scripts/build_windows.bat`
5. `installer/TallerMecanico.iss`
6. `README.md`
7. `GUIA_MANTENIMIENTO.md`
8. `GUIA_USUARIO_FINAL.md`
9. `GUIA_USUARIO_IMPRIMIR.html`

## Lo Que Falta Hacer En Windows

### 1) Verificar prerrequisitos

- Python 3 instalado y en PATH.
- Inno Setup instalado.

### 2) Build del ejecutable

Desde la raiz del proyecto, ejecutar:

```bat
scripts\build_windows.bat
```

### 3) Validar outputs de build

Confirmar existencia de:

- `dist/TallerMecanico.exe`
- `dist/portable/TallerMecanicoPortable/ABRIR_TALLER.bat`
- `dist/portable/TallerMecanicoPortable/TallerMecanico.exe`

### 4) Crear instalador Inno Setup

1. Abrir `installer/TallerMecanico.iss`.
2. Compilar.
3. Confirmar salida:
   - `installer/output/TallerMecanico-Setup.exe`

### 5) Prueba funcional minima del .exe (sin instalar)

1. Abrir `dist/TallerMecanico.exe`.
2. Crear 1 cliente, 1 vehiculo, 1 mantenimiento.
3. Cerrar y abrir de nuevo.
4. Verificar persistencia de datos.

### 6) Prueba funcional del instalador

1. Ejecutar `TallerMecanico-Setup.exe`.
2. Instalar.
3. Quitar USB.
4. Abrir desde acceso directo del escritorio.
5. Verificar que abre y persiste datos.

### 7) Prueba del modo portable USB

1. Copiar `TallerMecanicoPortable` a USB.
2. En otro PC, ejecutar `ABRIR_TALLER.bat`.
3. Crear dato de prueba.
4. Cerrar y reabrir.
5. Verificar persistencia.

## Criterios De Aceptacion

1. App abre sin errores en Windows.
2. Datos persisten tras reinicio en modo instalado.
3. Datos persisten en modo portable.
4. Instalador funciona y la app opera sin USB.
5. Guias listas para usuario final:
   - `GUIA_USUARIO_FINAL.md`
   - `GUIA_USUARIO_IMPRIMIR.html`

## Prompt Sugerido Para IA De Windows

```text
Ejecuta scripts\build_windows.bat en la raiz del proyecto.
Compila installer/TallerMecanico.iss con Inno Setup.
Valida funcionamiento de dist/TallerMecanico.exe, instalador y modo portable.
Reporta resultados con:
- archivos generados,
- pruebas hechas,
- errores encontrados (si hay),
- y correcciones aplicadas.
No cambies logica de negocio salvo que falle algo en Windows.
```
