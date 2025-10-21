import mariadb
import psycopg2
import sys


def conectar_postgres():
    """Conectar a PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="encuesta_estudiantes",
            user="postgres",
            password="password",
            port="5432"
        )
        print("Conexión a PostgreSQL exitosa")
        return conn
    except Exception as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None


def conectar_mariadb():
    """Conectar a MariaDB"""
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="password",
            port="3306"
        )
        print("Conexión a MariaDB exitosa")
        return conn
    except Exception as e:
        print(f"Error conectando a MariaDB: {e}")
        return None


def crear_esquema_mariadb(conn_mariadb):
    """Crear esquema en MariaDB (similar a MySQL)"""
    try:
        cur = conn_mariadb.cursor()

        # Crear base de datos
        cur.execute("CREATE DATABASE IF NOT EXISTS encuesta_estudiantes")
        cur.execute("USE encuesta_estudiantes")

        # Leer y ejecutar script de esquema (usamos el mismo de MySQL)
        with open('schemas/esquema_mysql.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cur.execute(statement)
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"Error en statement MariaDB: {e}")

        conn_mariadb.commit()
        print("Esquema de MariaDB creado exitosamente")

    except Exception as e:
        print(f"Error creando esquema MariaDB: {e}")


def migrar_datos_postgres_mariadb():
    """Migrar datos desde PostgreSQL a MariaDB"""
    print("=== MIGRACIÓN POSTGRESQL → MARIADB ===")

    # Conectar a las bases de datos
    conn_pg = conectar_postgres()
    conn_mariadb = conectar_mariadb()

    if not conn_pg or not conn_mariadb:
        print("Error en conexiones. Abortando migración.")
        return

    try:
        # Crear esquema en MariaDB
        crear_esquema_mariadb(conn_mariadb)

        cur_mariadb = conn_mariadb.cursor()
        cur_pg = conn_pg.cursor()

        # Configurar uso de base de datos
        cur_mariadb.execute("USE encuesta_estudiantes")

        # Migrar tablas de referencia
        tablas_referencia = ['carreras', 'lenguajes_programacion', 'sistemas_operativos']

        for tabla in tablas_referencia:
            print(f"Migrando tabla de referencia: {tabla}")

            cur_pg.execute(f"SELECT * FROM {tabla}")
            datos = cur_pg.fetchall()

            for fila in datos:
                try:
                    placeholders = ', '.join(['%s'] * len(fila))
                    cur_mariadb.execute(f"INSERT IGNORE INTO {tabla} VALUES ({placeholders})", fila)
                except Exception as e:
                    print(f"Error insertando en {tabla}: {e}")

        # Migrar estudiantes
        print("Migrando estudiantes...")
        cur_pg.execute(
            "SELECT id, nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito, fecha_registro FROM estudiantes")
        estudiantes = cur_pg.fetchall()

        for estudiante in estudiantes:
            try:
                cur_mariadb.execute("""
                    INSERT INTO estudiantes (id, nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, estudiante)
            except Exception as e:
                print(f"Error insertando estudiante {estudiante[0]}: {e}")

        # Migrar relaciones muchos a muchos
        print("Migrando relaciones estudiantes-lenguajes...")
        cur_pg.execute("SELECT estudiante_id, lenguaje_id FROM estudiante_lenguajes")
        relaciones_lenguajes = cur_pg.fetchall()

        for rel in relaciones_lenguajes:
            try:
                cur_mariadb.execute("""
                    INSERT IGNORE INTO estudiante_lenguajes (estudiante_id, lenguaje_id)
                    VALUES (?, ?)
                """, rel)
            except Exception as e:
                print(f"Error insertando relación lenguaje {rel}: {e}")

        print("Migrando relaciones estudiantes-SO...")
        cur_pg.execute("SELECT estudiante_id, so_id FROM estudiante_sistemas_operativos")
        relaciones_so = cur_pg.fetchall()

        for rel in relaciones_so:
            try:
                cur_mariadb.execute("""
                    INSERT IGNORE INTO estudiante_sistemas_operativos (estudiante_id, so_id)
                    VALUES (?, ?)
                """, rel)
            except Exception as e:
                print(f"Error insertando relación SO {rel}: {e}")

        conn_mariadb.commit()
        print("Migración a MariaDB completada exitosamente!")

        # Verificación
        print("\n--- VERIFICACIÓN MARIADB ---")
        cur_mariadb.execute("SELECT COUNT(*) FROM estudiantes")
        print(f"Estudiantes migrados: {cur_mariadb.fetchone()[0]}")

        cur_mariadb.execute("SELECT COUNT(*) FROM estudiante_lenguajes")
        print(f"Relaciones lenguajes migradas: {cur_mariadb.fetchone()[0]}")

        cur_mariadb.execute("SELECT COUNT(*) FROM estudiante_sistemas_operativos")
        print(f"Relaciones SO migradas: {cur_mariadb.fetchone()[0]}")

        cur_mariadb.close()
        cur_pg.close()

    except Exception as e:
        print(f"Error durante migración: {e}")
        conn_mariadb.rollback()
    finally:
        conn_pg.close()
        conn_mariadb.close()


if __name__ == "__main__":
    migrar_datos_postgres_mariadb()