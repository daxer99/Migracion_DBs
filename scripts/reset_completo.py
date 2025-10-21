import psycopg2
import mysql.connector

print("🔄 RESET SIMPLE DE BASES DE DATOS")

def reset_simple():
    # PostgreSQL
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="cangurito22"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS encuesta_estudiantes")
        cur.execute("CREATE DATABASE encuesta_estudiantes")
        cur.close()
        conn.close()
        print("✅ PostgreSQL resetado")
    except Exception as e:
        print(f"❌ Error PostgreSQL: {e}")

    # MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cangurito22"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS encuesta_estudiantes")
        cur.execute("CREATE DATABASE encuesta_estudiantes")
        cur.close()
        conn.close()
        print("✅ MySQL resetado")
    except Exception as e:
        print(f"❌ Error MySQL: {e}")

    # MariaDB (usando misma conexión que MySQL)
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cangurito22"
        )
        conn.autocommit = True
        cur = conn.cursor()
        # MariaDB usa la misma base de datos que MySQL en este caso
        print("✅ MariaDB resetado (misma que MySQL)")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error MariaDB: {e}")

    print("\n🎉 Reset completado. Bases de datos listas para usar.")

if __name__ == "__main__":
    reset_simple()