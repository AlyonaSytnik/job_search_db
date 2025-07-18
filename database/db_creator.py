import psycopg2
from psycopg2 import sql
from typing import Dict, List
from utils.config import DB_CONFIG


class DBCreator:
    """Создает БД и таблицы в PostgreSQL."""

    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True

    def create_database(self, db_name: str) -> None:
        """Создает новую базу данных."""
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

    def create_tables(self) -> None:
        """Создает таблицы employers и vacancies."""
        with self.conn.cursor() as cur:
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
        self.conn.commit()

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()