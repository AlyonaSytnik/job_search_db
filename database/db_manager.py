import psycopg2
from typing import List, Dict, Optional
from utils.config import DB_CONFIG


class DBManager:
    """Управляет данными в PostgreSQL."""

    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Возвращает список компаний и количество их вакансий."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id) 
                FROM employers e 
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id 
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Dict]:
        """Возвращает все вакансии с указанием компании, зарплаты и ссылки."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                FROM vacancies v 
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Возвращает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Возвращает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies 
                WHERE (salary_from + salary_to) / 2 > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Возвращает вакансии, содержащие ключевое слово в названии."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies 
                WHERE title ILIKE %s
            """, (f"%{keyword}%",))
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()