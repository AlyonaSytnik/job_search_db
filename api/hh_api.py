import requests
from typing import Dict, List, Optional


class HeadHunterAPI:
    """Класс для взаимодействия с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_employer(self, employer_id: str) -> Optional[Dict]:
        """Получить данные о работодателе по ID."""
        url = f"{self.base_url}/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_vacancies(self, employer_id: str) -> Optional[List[Dict]]:
        """Получить вакансии работодателя по ID."""
        url = f"{self.base_url}/vacancies?employer_id={employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("items", [])
        return None