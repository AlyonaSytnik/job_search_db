from api.hh_api import HeadHunterAPI
from database.db_creator import DBCreator
from database.db_manager import DBManager
from utils.config import DB_CONFIG, EMPLOYERS_IDS


def main():
    # 1. Создание БД и таблиц
    db_creator = DBCreator()
    db_creator.create_tables()
    db_creator.close()

    # 2. Заполнение данными
    hh_api = HeadHunterAPI()
    db_manager = DBManager()

    for employer_id in EMPLOYERS_IDS:
        employer = hh_api.get_employer(employer_id)
        vacancies = hh_api.get_vacancies(employer_id)
        # Запись в БД (код опущен для краткости)

    # 3. Взаимодействие с пользователем
    while True:
        print("\n1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print(db_manager.get_companies_and_vacancies_count())
        elif choice == "2":
            print(db_manager.get_all_vacancies())
        elif choice == "3":
            print(f"Средняя зарплата: {db_manager.get_avg_salary():.2f}")
        elif choice == "4":
            print(db_manager.get_vacancies_with_higher_salary())
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif choice == "0":
            break

    db_manager.close()


if __name__ == "__main__":
    main()