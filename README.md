# Sistema de Gestión de Mantenimiento Vehicular

Sistema de escritorio para la gestión integral de talleres mecánicos. Permite administrar clientes, vehículos y diferentes tipos de mantenimientos de forma eficiente.

## 🚗 Características Principales

- **Gestión de Clientes**: Registro completo de clientes con cédula, nombre, teléfono y fecha de registro
- **Control de Vehículos**: Administración de vehículos con placa, marca, modelo, línea y kilometraje asociados a clientes
- **Mantenimientos Especializados**:
  - Cambio de aceite y filtros
  - Mantenimiento de frenos
  - Mantenimiento general
  - Mantenimiento correctivo
- **Gestión de Precios**: Control de precios para los diferentes servicios
- **Reportes**: Generación de reportes en Excel con historial de mantenimientos

## 🛠️ Tecnologías

- **Python 3.x**
- **Tkinter**: Interfaz gráfica de usuario
- **SQLite**: Base de datos local embebida
- **pandas**: Procesamiento de datos
- **openpyxl**: Generación de reportes en Excel

## 📋 Requisitos

```
et_xmlfile==2.0.0
numpy==2.3.4
openpyxl==3.1.5
pandas==2.3.3
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
```

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/andresbot/taller-mecanico.git
cd taller-mecanico
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python main.py
```

La base de datos SQLite se crea automaticamente en el primer inicio.

## 💾 Guardado De Datos (Simple)

No necesitas configurar nada.

La aplicacion:

- Guarda los datos automaticamente en el equipo local.
- Crea respaldos automaticos.
- Funciona sin internet.

## 🪟 Build E Instalador Windows

### 1) Generar el .exe

En Windows, desde la raiz del proyecto:

```bat
scripts\build_windows.bat
```

Resultado:

- `dist/TallerMecanico.exe`

### 2) Crear instalador

1. Instalar Inno Setup en el equipo de build.
2. Abrir `installer/TallerMecanico.iss`.
3. Compilar el script.

Resultado:

- `installer/output/TallerMecanico-Setup.exe`

### 3) Distribucion en USB

Copiar a la USB el instalador generado `TallerMecanico-Setup.exe`.
Por seguridad de Windows, no es posible auto-ejecutar apps al conectar USB en equipos modernos.
La forma recomendada es abrir el instalador manualmente (doble clic) una sola vez.

## 🔌 Modo Portable (USB Sin Instalar)

Al ejecutar `scripts\build_windows.bat`, tambien se crea una carpeta portable:

- `dist/portable/TallerMecanicoPortable/`

Contenido principal:

- `TallerMecanico.exe`
- `ABRIR_TALLER.bat`
- `data/` (se crea vacia para la base local)

Uso:

1. Copiar `dist/portable/TallerMecanicoPortable` a la USB.
2. En el equipo Windows destino, abrir `ABRIR_TALLER.bat`.
3. Trabajar normalmente en la aplicacion.

Backups en modo portable:

- Se realizan automaticamente.

## 🧾 Guía Para Imprimir

Para entregar al usuario final en una sola hoja:

- [GUIA_USUARIO_IMPRIMIR.html](GUIA_USUARIO_IMPRIMIR.html)

## ⚙️ Detalle Técnico (Opcional)

Solo si necesitas soporte tecnico o migracion manual:

- Windows instalado: `%LOCALAPPDATA%/TallerMecanico/data/registrodb.sqlite3`
- Linux instalado: `~/.local/share/taller-mecanico/data/registrodb.sqlite3`
- Portable USB: `data/registrodb.sqlite3` en la carpeta portable

Respaldos:

- Instalado Windows: `%LOCALAPPDATA%/TallerMecanico/data/backups/`
- Instalado Linux: `~/.local/share/taller-mecanico/data/backups/`
- Portable USB: `data/backups/`

## 📁 Estructura del Proyecto

```
taller-mecanico/
├── controllers/      # Lógica de negocio
├── models/          # Modelos de datos
├── views/           # Interfaces de usuario
├── services/        # Servicios (conexión BD)
├── utils/           # Utilidades (estilos)
├── sql/             # Scripts SQL
├── main.py          # Punto de entrada
└── requirements.txt # Dependencias
```

## 📖 Arquitectura

El proyecto sigue el patrón **MVC (Model-View-Controller)**:
- **Models**: Manejo de datos y base de datos
- **Views**: Interfaces gráficas con Tkinter
- **Controllers**: Lógica de negocio entre modelos y vistas

## 📝 Licencia

Este proyecto está en fase de desarrollo.

## 👨‍💻 Autor

andresbot
