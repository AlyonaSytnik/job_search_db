import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils.config import DB_CONFIG, DEFAULT_DB_CONFIG


class DBCreator:
    """Управляет созданием БД и таблиц с изолированными соединениями"""

    @staticmethod
    def create_database():
        """Создает БД если она не существует"""
        try:
            conn = psycopg2.connect(**DEFAULT_DB_CONFIG)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                # Проверяем существование БД
                cur.execute(
                    sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
                    .format(sql.Literal(DB_CONFIG["database"])))

                if not cur.fetchone():
                    cur.execute(
                        sql.SQL("CREATE DATABASE {}")
                        .format(sql.Identifier(DB_CONFIG["database"])))
                    print(f"БД {DB_CONFIG['database']} создана")
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def create_tables():
        """Создает таблицы в целевой БД"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        employer_id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        url VARCHAR(100),
                        open_vacancies INT
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        employer_id INT REFERENCES employers(employer_id),
                        title VARCHAR(100) NOT NULL,
                        salary_from INT,
                        salary_to INT,
                        currency VARCHAR(10),
                        url VARCHAR(100)
                    )
                """)
                conn.commit()
                print("Таблицы созданы/проверены")
        finally:
            if 'conn' in locals():
                conn.close()