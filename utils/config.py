import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "hh_vacancies"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "12345"),
    "port": os.getenv("DB_PORT", "5432")
}

EMPLOYERS_IDS = [
    "1740",   # Яндекс (https://hh.ru/employer/1740)
    "3529",   # Сбер (https://hh.ru/employer/3529)
    "78638",  # Тинькофф (https://hh.ru/employer/78638)
    "15478",  # VK (https://hh.ru/employer/15478)
    "2748",   # Ростелеком (https://hh.ru/employer/2748)
    "39305",  # Газпром (https://hh.ru/employer/39305)
    "3127",   # Магнит (https://hh.ru/employer/3127)
    "1057",   # Лаборатория Касперского (https://hh.ru/employer/1057)
    "2180",   # Ozon (https://hh.ru/employer/2180)
    "87021",  # Wildberries (https://hh.ru/employer/87021)
]