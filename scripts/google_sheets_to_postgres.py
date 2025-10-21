import psycopg2
import pandas as pd
import csv
from datetime import datetime


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


def crear_esquema_postgres(conn):
    """Crear el esquema de base de datos en PostgreSQL"""
    try:
        cur = conn.cursor()

        # Leer y ejecutar el script de esquema
        with open('schemas/esquema_postgres.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Ejecutar cada sentencia por separado
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cur.execute(statement)

        conn.commit()
        print("Esquema de PostgreSQL creado exitosamente")
        cur.close()

    except Exception as e:
        print(f"Error creando esquema: {e}")
        conn.rollback()


def mapear_carrera(carrera_str):
    """Mapear el string de carrera al ID correspondiente"""
    carreras_map = {
        'ing software': 1, 'ingenieria software': 1, 'software': 1,
        'ciencias computacion': 2, 'ciencias de la computacion': 2, 'computer science': 2,
        'sistemas informacion': 3, 'sistemas de informacion': 3,
        'tecnologias informacion': 4, 'ti': 4, 'tecnologías de la información': 4,
        'ingenieria computacion': 5, 'ingeniería en computación': 5,
        'otra': 6, 'otro': 6
    }

    carrera_lower = carrera_str.lower().strip()
    return carreras_map.get(carrera_lower, 6)  # Default a "Otra"


def mapear_lenguajes(lenguajes_str):
    """Mapear string de lenguajes a IDs (opción múltiple)"""
    lenguajes_map = {
        'python': 1, 'java': 2, 'c++': 3, 'php': 4, 'javascript': 5,
        'r': 6, 'perl': 7, 'sql': 8, 'rust': 9, 'go': 10
    }

    lenguajes_ids = []
    if pd.isna(lenguajes_str) or lenguajes_str == '':
        return lenguajes_ids

    # Separar por comas, punto y coma, o saltos de línea
    import re
    lenguajes_list = re.split(r'[,;\n]', str(lenguajes_str))

    for lenguaje in lenguajes_list:
        lenguaje_clean = lenguaje.strip().lower()
        if lenguaje_clean in lenguajes_map:
            lenguajes_ids.append(lenguajes_map[lenguaje_clean])

    return lenguajes_ids


def mapear_sistemas_operativos(so_str):
    """Mapear string de sistemas operativos a IDs (opción múltiple)"""
    so_map = {
        'windows 7': 1, 'win7': 1,
        'windows 10': 2, 'win10': 2,
        'windows 11': 3, 'win11': 3,
        'linux mint': 4, 'mint': 4,
        'ubuntu': 5,
        'debian': 6,
        'opensuse': 7, 'open suse': 7,
        'fedora': 8,
        'macos': 9, 'mac os': 9, 'os x': 9,
        'chrome os': 10, 'chromebook': 10
    }

    so_ids = []
    if pd.isna(so_str) or so_str == '':
        return so_ids

    # Separar por comas, punto y coma, o saltos de línea
    import re
    so_list = re.split(r'[,;\n]', str(so_str))

    for so in so_list:
        so_clean = so.strip().lower()
        if so_clean in so_map:
            so_ids.append(so_map[so_clean])

    return so_ids


def validar_edad(edad):
    """Validar y convertir edad"""
    try:
        edad_int = int(edad)
        if 16 <= edad_int <= 60:
            return edad_int
        else:
            print(f"Edad fuera de rango: {edad_int}")
            return None
    except (ValueError, TypeError):
        print(f"Edad inválida: {edad}")
        return None


def validar_experiencia(exp):
    """Validar y convertir años de experiencia"""
    try:
        exp_int = int(exp)
        if exp_int >= 0:
            return exp_int
        else:
            return 0
    except (ValueError, TypeError):
        return 0


def procesar_csv_y_cargar(conn, csv_file_path):
    """Procesar el archivo CSV y cargar datos a PostgreSQL"""
    try:
        # Leer el CSV
        df = pd.read_csv(csv_file_path)
        print(f"CSV leído exitosamente. {len(df)} filas encontradas.")

        cur = conn.cursor()
        estudiantes_procesados = 0

        for index, fila in df.iterrows():
            try:
                # Validar y procesar datos básicos
                nombre = str(fila.iloc[0]).strip() if pd.notna(fila.iloc[0]) else None
                edad = validar_edad(fila.iloc[1]) if pd.notna(fila.iloc[1]) else None
                carrera_str = str(fila.iloc[2]) if pd.notna(fila.iloc[2]) else 'Otra'
                experiencia = validar_experiencia(fila.iloc[5]) if len(fila) > 5 else 0
                proyecto = str(fila.iloc[6]) if len(fila) > 6 and pd.notna(fila.iloc[6]) else "No especificado"

                # Validaciones básicas
                if not nombre or not edad:
                    print(f"Fila {index + 1}: Datos requeridos faltantes. Saltando...")
                    continue

                # Mapear datos
                carrera_id = mapear_carrera(carrera_str)
                lenguajes_ids = mapear_lenguajes(fila.iloc[3]) if len(fila) > 3 else []
                so_ids = mapear_sistemas_operativos(fila.iloc[4]) if len(fila) > 4 else []

                # Insertar estudiante
                cur.execute("""
                    INSERT INTO estudiantes (nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (nombre, edad, carrera_id, experiencia, proyecto))

                estudiante_id = cur.fetchone()[0]

                # Insertar lenguajes de programación (relación muchos a muchos)
                for lenguaje_id in lenguajes_ids:
                    try:
                        cur.execute("""
                            INSERT INTO estudiante_lenguajes (estudiante_id, lenguaje_id)
                            VALUES (%s, %s)
                        """, (estudiante_id, lenguaje_id))
                    except Exception as e:
                        print(f"Error insertando lenguaje {lenguaje_id} para estudiante {estudiante_id}: {e}")
                        conn.rollback()
                        continue

                # Insertar sistemas operativos (relación muchos a muchos)
                for so_id in so_ids:
                    try:
                        cur.execute("""
                            INSERT INTO estudiante_sistemas_operativos (estudiante_id, so_id)
                            VALUES (%s, %s)
                        """, (estudiante_id, so_id))
                    except Exception as e:
                        print(f"Error insertando SO {so_id} para estudiante {estudiante_id}: {e}")
                        conn.rollback()
                        continue

                estudiantes_procesados += 1
                print(f"Estudiante {estudiantes_procesados} procesado: {nombre}")

            except Exception as e:
                print(f"Error procesando fila {index + 1}: {e}")
                conn.rollback()
                continue

        conn.commit()
        print(f"\nProcesamiento completado. {estudiantes_procesados} estudiantes cargados exitosamente.")

        # Estadísticas finales
        cur.execute("SELECT COUNT(*) FROM estudiantes")
        total_estudiantes = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(DISTINCT estudiante_id) 
            FROM estudiante_lenguajes
        """)
        estudiantes_con_lenguajes = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(DISTINCT estudiante_id) 
            FROM estudiante_sistemas_operativos
        """)
        estudiantes_con_so = cur.fetchone()[0]

        print(f"\n--- ESTADÍSTICAS FINALES ---")
        print(f"Total estudiantes en BD: {total_estudiantes}")
        print(f"Estudiantes con lenguajes asignados: {estudiantes_con_lenguajes}")
        print(f"Estudiantes con SO asignados: {estudiantes_con_so}")

        cur.close()

    except Exception as e:
        print(f"Error procesando CSV: {e}")
        conn.rollback()


def main():
    """Función principal"""
    print("=== CARGA DE DATOS DESDE CSV A POSTGRESQL ===")

    # Conectar a PostgreSQL
    conn = conectar_postgres()
    if not conn:
        return

    try:
        # Crear esquema
        crear_esquema_postgres(conn)

        # Procesar y cargar datos
        csv_file = "data/respuestas_encuesta.csv"
        procesar_csv_y_cargar(conn, csv_file)

    finally:
        conn.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    main()