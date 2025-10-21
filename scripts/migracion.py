import psycopg2
import pandas as pd
import os

print("=== MIGRACIÓN - SIN ARCHIVOS EXTERNOS ===")


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


def crear_esquema_completo(conn):
    """Crear todo el esquema directamente en código"""
    try:
        cur = conn.cursor()

        print("🗃️ Creando tablas...")

        # 1. Tablas de referencia
        cur.execute("""
            CREATE TABLE IF NOT EXISTS carreras (
                id SERIAL PRIMARY KEY,
                nombre_carrera VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS lenguajes_programacion (
                id SERIAL PRIMARY KEY,
                nombre_lenguaje VARCHAR(30) UNIQUE NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sistemas_operativos (
                id SERIAL PRIMARY KEY,
                nombre_so VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        # 2. Tabla principal
        cur.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id SERIAL PRIMARY KEY,
                nombre_completo VARCHAR(100) NOT NULL,
                edad INTEGER CHECK (edad >= 16 AND edad <= 60),
                carrera_id INTEGER REFERENCES carreras(id),
                anos_experiencia INTEGER DEFAULT 0,
                proyecto_favorito TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. Tablas de relación
        cur.execute("""
            CREATE TABLE IF NOT EXISTS estudiante_lenguajes (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                lenguaje_id INTEGER REFERENCES lenguajes_programacion(id) ON DELETE CASCADE,
                UNIQUE(estudiante_id, lenguaje_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS estudiante_sistemas_operativos (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                so_id INTEGER REFERENCES sistemas_operativos(id) ON DELETE CASCADE,
                UNIQUE(estudiante_id, so_id)
            )
        """)

        print("✅ Tablas creadas")

        # Insertar datos de referencia
        print("📝 Insertando datos de referencia...")

        # Lenguajes
        lenguajes = ['Python', 'Java', 'C++', 'PHP', 'JavaScript', 'R', 'Perl', 'SQL', 'Rust', 'Go']
        for lenguaje in lenguajes:
            cur.execute(
                "INSERT INTO lenguajes_programacion (nombre_lenguaje) VALUES (%s) ON CONFLICT (nombre_lenguaje) DO NOTHING",
                (lenguaje,)
            )

        # Sistemas operativos
        sistemas_ops = [
            'Windows 7', 'Windows 10', 'Windows 11',
            'Linux Mint', 'Ubuntu', 'Debian', 'OpenSUSE', 'Fedora',
            'macOS', 'Chrome OS'
        ]
        for so in sistemas_ops:
            cur.execute(
                "INSERT INTO sistemas_operativos (nombre_so) VALUES (%s) ON CONFLICT (nombre_so) DO NOTHING",
                (so,)
            )

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
            cur.execute(
                "INSERT INTO carreras (nombre_carrera) VALUES (%s) ON CONFLICT (nombre_carrera) DO NOTHING",
                (carrera,)
            )

        conn.commit()
        print("✅ Datos de referencia insertados")
        cur.close()
        return True

    except Exception as e:
        print(f"❌ Error creando esquema: {e}")
        conn.rollback()
        return False


def cargar_datos_desde_csv(conn):
    """Cargar datos desde el archivo CSV"""
    try:
        csv_file = "../data/respuestas_encuesta.csv"

        if not os.path.exists(csv_file):
            print(f"❌ Archivo CSV no encontrado: {csv_file}")
            return False

        print(f"📂 Leyendo archivo CSV: {csv_file}")

        # Leer CSV con diferentes encodings
        try:
            df = pd.read_csv(csv_file)
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(csv_file, encoding='latin1')
                print("✅ CSV leído con encoding latin1")
            except:
                df = pd.read_csv(csv_file, encoding='iso-8859-1')
                print("✅ CSV leído con encoding iso-8859-1")

        print(f"📊 Filas encontradas: {len(df)}")
        print(f"📋 Columnas: {list(df.columns)}")

        cur = conn.cursor()
        estudiantes_procesados = 0

        # Mapeos
        carreras_map = {
            'ing software': 1, 'ingenieria software': 1, 'software': 1,
            'ciencias computacion': 2, 'ciencias de la computacion': 2,
            'sistemas informacion': 3, 'sistemas de informacion': 3,
            'tecnologias informacion': 4, 'ti': 4,
            'ingenieria computacion': 5,
            'otra': 6, 'otro': 6
        }

        lenguajes_map = {
            'python': 1, 'java': 2, 'c++': 3, 'php': 4, 'javascript': 5,
            'r': 6, 'perl': 7, 'sql': 8, 'rust': 9, 'go': 10
        }

        so_map = {
            'windows 7': 1, 'win7': 1,
            'windows 10': 2, 'win10': 2,
            'windows 11': 3, 'win11': 3,
            'linux mint': 4, 'mint': 4,
            'ubuntu': 5,
            'debian': 6,
            'opensuse': 7, 'open suse': 7,
            'fedora': 8,
            'macos': 9, 'mac os': 9,
            'chrome os': 10, 'chromebook': 10
        }

        for index, fila in df.iterrows():
            try:
                # Extraer datos básicos
                nombre = str(fila.iloc[0]).strip()
                edad = int(fila.iloc[1]) if pd.notna(fila.iloc[1]) else None
                carrera_str = str(fila.iloc[2]).lower() if len(fila) > 2 and pd.notna(fila.iloc[2]) else 'otra'
                experiencia = int(fila.iloc[5]) if len(fila) > 5 and pd.notna(fila.iloc[5]) else 0
                proyecto = str(fila.iloc[6]) if len(fila) > 6 and pd.notna(fila.iloc[6]) else "No especificado"

                # Validar
                if not nombre or not edad:
                    continue

                # Mapear carrera
                carrera_id = 6  # default
                for key, value in carreras_map.items():
                    if key in carrera_str:
                        carrera_id = value
                        break

                # Mapear lenguajes (múltiples)
                lenguajes_ids = []
                if len(fila) > 3 and pd.notna(fila.iloc[3]):
                    lenguajes_str = str(fila.iloc[3]).lower()
                    for lenguaje_key, lenguaje_id in lenguajes_map.items():
                        if lenguaje_key in lenguajes_str:
                            lenguajes_ids.append(lenguaje_id)
                lenguajes_ids = list(set(lenguajes_ids))  # eliminar duplicados

                # Mapear sistemas operativos (múltiples)
                so_ids = []
                if len(fila) > 4 and pd.notna(fila.iloc[4]):
                    so_str = str(fila.iloc[4]).lower()
                    for so_key, so_id in so_map.items():
                        if so_key in so_str:
                            so_ids.append(so_id)
                so_ids = list(set(so_ids))  # eliminar duplicados

                # Insertar estudiante
                cur.execute("""
                    INSERT INTO estudiantes (nombre_completo, edad, carrera_id, anos_experiencia, proyecto_favorito)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (nombre, edad, carrera_id, experiencia, proyecto))

                estudiante_id = cur.fetchone()[0]

                # Insertar lenguajes
                for lenguaje_id in lenguajes_ids:
                    cur.execute("""
                        INSERT INTO estudiante_lenguajes (estudiante_id, lenguaje_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (estudiante_id, lenguaje_id))

                # Insertar sistemas operativos
                for so_id in so_ids:
                    cur.execute("""
                        INSERT INTO estudiante_sistemas_operativos (estudiante_id, so_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (estudiante_id, so_id))

                estudiantes_procesados += 1

                if estudiantes_procesados % 5 == 0:
                    print(f"✅ Procesados {estudiantes_procesados} estudiantes...")

            except Exception as e:
                print(f"⚠️ Error en fila {index + 1}: {e}")
                continue

        conn.commit()

        # Estadísticas finales
        cur.execute("SELECT COUNT(*) FROM estudiantes")
        total_estudiantes = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM estudiante_lenguajes")
        total_lenguajes = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM estudiante_sistemas_operativos")
        total_so = cur.fetchone()[0]

        print(f"\n🎉 CARGA COMPLETADA")
        print(f"📊 Estudiantes: {total_estudiantes}")
        print(f"💻 Relaciones lenguajes: {total_lenguajes}")
        print(f"🖥️ Relaciones SO: {total_so}")

        cur.close()
        return True

    except Exception as e:
        print(f"❌ Error cargando datos CSV: {e}")
        conn.rollback()
        return False


def main():
    """Función principal"""
    print("🚀 INICIANDO MIGRACIÓN COMPLETA")

    # Conectar a PostgreSQL
    conn = conectar_postgres()
    if not conn:
        print("❌ No se puede continuar sin conexión a PostgreSQL")
        return

    try:
        # Paso 1: Crear esquema
        print("\n" + "=" * 50)
        print("PASO 1: CREANDO ESQUEMA DE BASE DE DATOS")
        print("=" * 50)
        if not crear_esquema_completo(conn):
            return

        # Paso 2: Cargar datos
        print("\n" + "=" * 50)
        print("PASO 2: CARGANDO DATOS DESDE CSV")
        print("=" * 50)
        if not cargar_datos_desde_csv(conn):
            return

        print("\n🎊 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")

    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        conn.close()
        print("🔌 Conexión cerrada")


if __name__ == "__main__":
    main()