import os
from dotenv import load_dotenv

load_dotenv()

# Параметры для подключения к дефолтной БД (postgres)
DEFAULT_DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": "postgres",  # Стандартная БД
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "port": os.getenv("DB_PORT", "5432")
}

# Параметры для нашей БД (будет создана)
DB_CONFIG = {
    **DEFAULT_DB_CONFIG,
    "database": os.getenv("DB_NAME", "hh_vacancies")  # Наша БД
}