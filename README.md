# 🗃️ Actividad de Migración de Bases de Datos

Este proyecto educativo muestra la migración de datos entre diferentes motores de bases de datos (PostgreSQL, MySQL y MariaDB), partiendo de datos recolectados mediante Google Forms.

## 🎯 Objetivos de Aprendizaje

- **Diseño de bases de datos relacionales** 
- **Migración de datos** entre diferentes motores de SQL
- **Procesamiento ETL** (Extract, Transform, Load) desde CSV
- **Manejo de conexiones** a múltiples sistemas de bases de datos
- **Uso de DBeaver** como herramienta universal de administración
- **Diferencias entre motores** SQL y sus particularidades

## 📁 Estructura del Proyecto
```bash
Migracion_DBs/
│
├── data/
│ └── respuestas_encuesta.csv    # Datos de ejemplo de la encuesta
│
├── scripts/
│ ├── migracion.py               #Carga datos CSV a PostgreSQL
│ ├── migrar_mysql.py            # Migra de PostgreSQL a MySQL
│ ├── migrar_mariadb.py          # Migra de PostgreSQL a MariaDB
│ ├── reset_completo.py          # Resetea todas las bases de datos
│ └── verificacion_consultas.sql # Consultas de verificación
│
├── schemas/
│ ├── esquema_postgres.sql 
│ └── esquema_mysql.sql 
│
└── README.md
```




## 🚀 Instalación y Configuración

### 1. 📥 Descargar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/daxer99/Migracion_DBs.git
cd Migracion_DBs

# O descargar como ZIP desde GitHub y extraer
```

### 2. 🛠️ Descargar e Instalar el Software Requerido
🔹 DBeaver: https://dbeaver.io/download/

🔹 PostgreSQL: https://www.postgresql.org/download/  

🔹 MySQL: https://dev.mysql.com/downloads/mysql/

🔹 MariaDB: https://mariadb.org/download/

### 3. 📦 Instalar Dependencias Python 

```bash
# Navegar al directorio del proyecto
cd Migracion_DBs/scripts

# Instalar dependencias requeridas
pip install psycopg2-binary pandas mysql-connector-python

# Si hay problemas de permisos en Linux/macOS:
pip install --user psycopg2-binary pandas mysql-connector-python
```
### 4. ⚙️ Configurar Conexiones en DBeaver
```bash
1. Abrir DBeaver
2. Clic en "Nueva conexión de base de datos" (icono de enchufe)
3. Configurar cada motor:

PostgreSQL:
Tipo: PostgreSQL
Host: localhost
Puerto: 5432
Database: all
Username: postgres
Password: la configurada en el motor

MySQL:
Tipo: MySQL
Host: localhost
Puerto: 3306
Username: root
Password: la configurada en el motor

MariaDB:
Tipo: MySQL (es compatible)
Host: localhost
Puerto: 3306
Username: root
Password: la configurada en el motor
```
## Uso

```bash
cd scripts
python migracion.py

python migrar_mysql.py

python migrar_mariadb.py

python reset_completo.py
```


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
## Authors

- [@rprealta](https://github.com/daxer99)

