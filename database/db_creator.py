import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils.config import DB_CONFIG, DEFAULT_DB_CONFIG


class DBCreator:
    """Создает БД и таблицы в PostgreSQL"""

    def __init__(self):
        # Подключаемся к дефолтной БД для создания новой
        self.default_conn = psycopg2.connect(**DEFAULT_DB_CONFIG)
        self.default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Подключение к целевой БД (будет установлено после создания)
        self.target_conn = None

    def create_database(self, db_name: str) -> None:
        """Создает новую базу данных если её не существует"""
        with self.default_conn.cursor() as cur:
            # Проверяем существование БД
            cur.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
                .format(sql.Literal(db_name))

            if not cur.fetchone():
                cur.execute(
                    sql.SQL("CREATE DATABASE {}")
                    .format(sql.Identifier(db_name)))
            print(f"База данных {db_name} создана")
            else:
            print(f"База данных {db_name} уже существует")

    def create_tables(self) -> None:
        """Создает таблицы в целевой БД"""
        if not self.target_conn:
            self.target_conn = psycopg2.connect(**DB_CONFIG)

        with self.target_conn.cursor() as cur:
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
            self.target_conn.commit()

    def close(self) -> None:
        """Закрывает все соединения"""
        if self.default_conn:
            self.default_conn.close()
        if self.target_conn:
            self.target_conn.close()