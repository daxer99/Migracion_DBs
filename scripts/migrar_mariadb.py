import mysql.connector  # Usar el conector de MySQL para MariaDB
import psycopg2


def conectar_postgres():
    """Conectar a PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="encuesta_estudiantes",
            user="postgres",
            password="cangurito22",
            port="5432"
        )
        print("✅ Conexión a PostgreSQL exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None


def conectar_mariadb():
    """Conectar a MariaDB usando MySQL connector (compatible)"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cangurito22",
            port="3306"
        )
        print("✅ Conexión a MariaDB exitosa (usando MySQL connector)")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a MariaDB: {e}")
        print("💡 Verifica que:")
        print("   1. MariaDB/MySQL esté ejecutándose")
        print("   2. Las credenciales sean correctas")
        print("   3. El puerto 3306 esté disponible")
        return None


def crear_esquema_mariadb(conn_mariadb):
    """Crear esquema en MariaDB"""
    try:
        cur = conn_mariadb.cursor()

        # Crear base de datos
        print("🗃️ Creando base de datos...")
        cur.execute("CREATE DATABASE IF NOT EXISTS encuesta_estudiantes")
        cur.execute("USE encuesta_estudiantes")
        print("✅ Base de datos creada/seleccionada")

        # Crear esquema manualmente
        print("📋 Creando tablas en MariaDB...")

        # Tablas de referencia
        tablas_sql = [
            # Carreras
            """
            CREATE TABLE IF NOT EXISTS carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_carrera VARCHAR(50) UNIQUE NOT NULL
            )
            """,

            # Lenguajes
            """
            CREATE TABLE IF NOT EXISTS lenguajes_programacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_lenguaje VARCHAR(30) UNIQUE NOT NULL
            )
            """,

            # Sistemas operativos
            """
            CREATE TABLE IF NOT EXISTS sistemas_operativos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_so VARCHAR(50) UNIQUE NOT NULL
            )
            """,

            # Estudiantes
            """
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_completo VARCHAR(100) NOT NULL,
                edad INT,
                carrera_id INT,
                anos_experiencia INT DEFAULT 0,
                proyecto_favorito TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id),
                CHECK (edad >= 16 AND edad <= 60)
            )
            """,

            # Relación estudiantes-lenguajes
            """
            CREATE TABLE IF NOT EXISTS estudiante_lenguajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT,
                lenguaje_id INT,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
                FOREIGN KEY (lenguaje_id) REFERENCES lenguajes_programacion(id) ON DELETE CASCADE,
                UNIQUE(estudiante_id, lenguaje_id)
            )
            """,

            # Relación estudiantes-SO
            """
            CREATE TABLE IF NOT EXISTS estudiante_sistemas_operativos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT,
                so_id INT,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
                FOREIGN KEY (so_id) REFERENCES sistemas_operativos(id) ON DELETE CASCADE,
                UNIQUE(estudiante_id, so_id)
            )
            """
        ]

        # Ejecutar creación de tablas
        for i, sql in enumerate(tablas_sql):
            try:
                cur.execute(sql)
                print(f"   ✅ Tabla {i + 1} creada")
            except Exception as e:
                print(f"   ⚠️ Error creando tabla {i + 1}: {e}")

        # Insertar datos de referencia
        print("📝 Insertando datos de referencia...")

        # Lenguajes
        lenguajes = ['Python', 'Java', 'C++', 'PHP', 'JavaScript', 'R', 'Perl', 'SQL', 'Rust', 'Go']
        for lenguaje in lenguajes:
            try:
                cur.execute(
                    "INSERT IGNORE INTO lenguajes_programacion (nombre_lenguaje) VALUES (%s)",
                    (lenguaje,)
                )
            except Exception as e:
                print(f"   ⚠️ Error insertando lenguaje {lenguaje}: {e}")

        # Sistemas operativos
        sistemas_ops = [
            'Windows 7', 'Windows 10', 'Windows 11',
            'Linux Mint', 'Ubuntu', 'Debian', 'OpenSUSE', 'Fedora',
            'macOS', 'Chrome OS'
        ]
        for so in sistemas_ops:
            try:
                cur.execute(
                    "INSERT IGNORE INTO sistemas_operativos (nombre_so) VALUES (%s)",
                    (so,)
                )
            except Exception as e:
                print(f"   ⚠️ Error insertando SO {so}: {e}")

        # Carreras
        carreras = [
            'Ingenieria de Software',
            'Ciencias de la Computacion',
            'Sistemas de Informacion',
            'Tecnologias de la Informacion',
            'Ingenieria en Computacion',
            'Otra'
        ]
        for carrera in carreras:
            try:
                cur.execute(
                    "INSERT IGNORE INTO carreras (nombre_carrera) VALUES (%s)",
                    (carrera,)
                )
            except Exception as e:
                print(f"   ⚠️ Error insertando carrera {carrera}: {e}")

        conn_mariadb.commit()
        print("✅ Esquema de MariaDB creado exitosamente")

    except Exception as e:
        print(f"❌ Error creando esquema MariaDB: {e}")
        conn_mariadb.rollback()


def verificar_tablas_mariadb(conn_mariadb):
    """Verificar que las tablas existen en MariaDB"""
    try:
        cur = conn_mariadb.cursor()
        cur.execute("USE encuesta_estudiantes")
        cur.execute("SHOW TABLES")
        tablas = [tabla[0] for tabla in cur.fetchall()]

        print("📊 Tablas en MariaDB:", tablas)

        tablas_esperadas = ['carreras', 'lenguajes_programacion', 'sistemas_operativos',
                            'estudiantes', 'estudiante_lenguajes', 'estudiante_sistemas_operativos']

        for tabla in tablas_esperadas:
            if tabla in tablas:
                print(f"   ✅ {tabla} - EXISTE")
            else:
                print(f"   ❌ {tabla} - FALTANTE")

        return all(tabla in tablas for tabla in tablas_esperadas)

    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False


def migrar_datos_postgres_mariadb():
    """Migrar datos desde PostgreSQL a MariaDB"""
    print("=== MIGRACIÓN POSTGRESQL → MARIADB ===")
    print("🔌 Usando MySQL connector para MariaDB")

    # Conectar a las bases de datos
    conn_pg = conectar_postgres()
    if not conn_pg:
        print("❌ No se puede continuar sin PostgreSQL")
        return

    conn_mariadb = conectar_mariadb()
    if not conn_mariadb:
        print("❌ No se puede continuar sin MariaDB")
        conn_pg.close()
        return

    try:
        # Paso 1: Crear esquema en MariaDB
        print("\n" + "=" * 50)
        print("PASO 1: CREANDO ESQUEMA EN MARIADB")
        print("=" * 50)
        crear_esquema_mariadb(conn_mariadb)

        # Verificar que las tablas se crearon
        print("\n🔍 Verificando tablas...")
        if not verificar_tablas_mariadb(conn_mariadb):
            print("❌ Faltan tablas en MariaDB. Abortando migración.")
            return

        cur_mariadb = conn_mariadb.cursor()
        cur_pg = conn_pg.cursor()

        # Configurar uso de base de datos
        cur_mariadb.execute("USE encuesta_estudiantes")

        # Paso 2: Migrar datos
        print("\n" + "=" * 50)
        print("PASO 2: MIGRANDO DATOS")
        print("=" * 50)

        # Migrar tablas de referencia
        tablas_referencia = ['carreras', 'lenguajes_programacion', 'sistemas_operativos']
        total_referencias = 0

        for tabla in tablas_referencia:
            print(f"📤 Migrando: {tabla}")

            cur_pg.execute(f"SELECT * FROM {tabla}")
            datos = cur_pg.fetchall()

            migrados_tabla = 0
            for fila in datos:
                try:
                    placeholders = ', '.join(['%s'] * len(fila))
                    cur_mariadb.execute(f"INSERT IGNORE INTO {tabla} VALUES ({placeholders})", fila)
                    migrados_tabla += 1
                    total_referencias += 1
                except Exception as e:
                    print(f"   ⚠️ Error en {tabla}: {e}")

            print(f"   ✅ {migrados_tabla} registros migrados")

        # Migrar estudiantes
        print("👥 Migrando estudiantes...")
        cur_pg.execute(
            "SELECT id, nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito, fecha_registro FROM estudiantes"
        )
        estudiantes = cur_pg.fetchall()

        estudiantes_migrados = 0
        for estudiante in estudiantes:
            try:
                cur_mariadb.execute("""
                    INSERT IGNORE INTO estudiantes 
                    (id, nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito, fecha_registro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, estudiante)
                estudiantes_migrados += 1
            except Exception as e:
                print(f"   ⚠️ Error en estudiante {estudiante[0]}: {e}")

        print(f"✅ Estudiantes migrados: {estudiantes_migrados}")

        # Migrar relaciones muchos a muchos - Lenguajes
        print("💻 Migrando relaciones estudiantes-lenguajes...")
        cur_pg.execute("SELECT estudiante_id, lenguaje_id FROM estudiante_lenguajes")
        relaciones_lenguajes = cur_pg.fetchall()

        relaciones_leng_migradas = 0
        for rel in relaciones_lenguajes:
            try:
                cur_mariadb.execute("""
                    INSERT IGNORE INTO estudiante_lenguajes (estudiante_id, lenguaje_id)
                    VALUES (%s, %s)
                """, rel)
                relaciones_leng_migradas += 1
            except Exception as e:
                print(f"   ⚠️ Error en relación lenguaje {rel}: {e}")

        print(f"✅ Relaciones lenguajes migradas: {relaciones_leng_migradas}")

        # Migrar relaciones muchos a muchos - Sistemas Operativos
        print("🖥️ Migrando relaciones estudiantes-SO...")
        cur_pg.execute("SELECT estudiante_id, so_id FROM estudiante_sistemas_operativos")
        relaciones_so = cur_pg.fetchall()

        relaciones_so_migradas = 0
        for rel in relaciones_so:
            try:
                cur_mariadb.execute("""
                    INSERT IGNORE INTO estudiante_sistemas_operativos (estudiante_id, so_id)
                    VALUES (%s, %s)
                """, rel)
                relaciones_so_migradas += 1
            except Exception as e:
                print(f"   ⚠️ Error en relación SO {rel}: {e}")

        print(f"✅ Relaciones SO migradas: {relaciones_so_migradas}")

        conn_mariadb.commit()

        print("\n🎉 MIGRACIÓN A MARIADB COMPLETADA EXITOSAMENTE!")

        # Verificación final
        print("\n" + "=" * 50)
        print("VERIFICACIÓN FINAL")
        print("=" * 50)

        # Conteos MariaDB
        cur_mariadb.execute("SELECT COUNT(*) as total FROM estudiantes")
        mariadb_estudiantes = cur_mariadb.fetchone()[0]

        cur_mariadb.execute("SELECT COUNT(*) as total FROM estudiante_lenguajes")
        mariadb_lenguajes = cur_mariadb.fetchone()[0]

        cur_mariadb.execute("SELECT COUNT(*) as total FROM estudiante_sistemas_operativos")
        mariadb_so = cur_mariadb.fetchone()[0]

        # Conteos PostgreSQL
        cur_pg.execute("SELECT COUNT(*) FROM estudiantes")
        pg_estudiantes = cur_pg.fetchone()[0]

        cur_pg.execute("SELECT COUNT(*) FROM estudiante_lenguajes")
        pg_lenguajes = cur_pg.fetchone()[0]

        cur_pg.execute("SELECT COUNT(*) FROM estudiante_sistemas_operativos")
        pg_so = cur_pg.fetchone()[0]

        print(f"📊 COMPARACIÓN:")
        print(
            f"   Estudiantes:  PostgreSQL={pg_estudiantes} | MariaDB={mariadb_estudiantes} | ✅={pg_estudiantes == mariadb_estudiantes}")
        print(
            f"   Lenguajes:    PostgreSQL={pg_lenguajes} | MariaDB={mariadb_lenguajes} | ✅={pg_lenguajes == mariadb_lenguajes}")
        print(f"   SO:           PostgreSQL={pg_so} | MariaDB={mariadb_so} | ✅={pg_so == mariadb_so}")

        cur_mariadb.close()
        cur_pg.close()

    except Exception as e:
        print(f"❌ Error durante migración: {e}")
        conn_mariadb.rollback()
    finally:
        conn_pg.close()
        conn_mariadb.close()
        print("\n🔌 Conexiones cerradas")


if __name__ == "__main__":
    migrar_datos_postgres_mariadb()