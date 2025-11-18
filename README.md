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
- **MySQL**: Base de datos
- **mysql-connector-python**: Conexión a base de datos
- **pandas**: Procesamiento de datos
- **openpyxl**: Generación de reportes en Excel

## 📋 Requisitos

```
et_xmlfile==2.0.0
mysql-connector-python==9.5.0
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

3. Configurar base de datos MySQL:
```bash
mysql -u root -p < database_schema.sql
```

4. Ejecutar la aplicación:
```bash
python main.py
```

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

## 🔧 Configuración de Base de Datos

La aplicación se conecta a MySQL con las siguientes credenciales por defecto:
- Host: `127.0.0.1`
- Usuario: `root`
- Contraseña: `root`
- Base de datos: `registrodb`
- Puerto: `3306`

## 📝 Licencia

Este proyecto está en fase de desarrollo.

## 👨‍💻 Autor

andresbot
