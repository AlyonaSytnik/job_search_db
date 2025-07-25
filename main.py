from database.db_creator import DBCreator
from database.db_manager import DBManager
from api.hh_api import HeadHunterAPI
import time


def main():
    print("=== Парсер вакансий с HeadHunter ===")

    # 1. Инициализация базы данных
    print("\nИнициализация базы данных...")
    DBCreator.create_database()
    DBCreator.create_tables()
    time.sleep(1)

    # 2. Загрузка данных
    print("\nЗагрузка данных с HeadHunter...")
    hh_api = HeadHunterAPI()
    db_manager = DBManager()

    employer_ids = [
        "1740", "3529", "78638", "15478", "2748",
        "39305", "3127", "1057", "2180", "87021"
    ]

    # 3. Заполнение базы данных
    for employer_id in employer_ids:
        employer_data = hh_api.get_employer(employer_id)
        if employer_data:
            db_manager.insert_employer(employer_data)
            vacancies = hh_api.get_vacancies(employer_id)

            for vacancy in vacancies:
                db_manager.insert_vacancy(vacancy, employer_id)

            print(f"Загружено {len(vacancies)} вакансий от {employer_data['name']}")
            time.sleep(0.5)

    # 4. Основной цикл взаимодействия
    while True:
        print("\n" + "=" * 40)
        print("Меню:")
        print("1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for company, count in companies:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            print("\nВсе вакансии:")
            for company, title, salary_from, salary_to, url in vacancies:
                salary = f"{salary_from or '?'}-{salary_to or '?'}"
                print(f"{company}: {title} ({salary}) - {url}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата: {avg_salary:.2f} RUB")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vac in vacancies:
                print(f"{vac[2]} (от {vac[3]} RUB)")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nРезультаты по '{keyword}':")
            for vac in vacancies:
                print(f"{vac[2]} ({vac[6]})")

        elif choice == "0":
            print("\nЗавершение работы...")
            break

        input("\nНажмите Enter чтобы продолжить...")

    db_manager.close()
    print("Работа программы завершена.")


if __name__ == "__main__":
    main()