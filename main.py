from database.db_creator import DBCreator
from database.db_manager import DBManager
from utils.config import DB_CONFIG


def main():
    # 1. Создаем объект для работы с БД
    db_creator = DBCreator()

    try:
        # 2. Создаем новую БД (если не существует)
        db_creator.create_database(DB_CONFIG["database"])

        # 3. Создаем таблицы в новой БД
        db_creator.create_tables()

        # 4. Теперь работаем с созданной БД через DBManager
        db_manager = DBManager()

        # ... остальная логика приложения

    finally:
        db_creator.close()
        if 'db_manager' in locals():
            db_manager.close()


if __name__ == "__main__":
    main()