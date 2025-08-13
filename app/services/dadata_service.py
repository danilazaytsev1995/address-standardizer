import aiohttp
import os


class DadataService:
    BASE_URL = "https://cleaner.dadata.ru/api/v1/clean/address"

    def __init__(self):
        # Получение значений переменных окружения
        self.api_key = os.getenv("DADATA_API_KEY")
        self.secret_key = os.getenv("DADATA_SECRET_KEY")
        self.session = aiohttp.ClientSession()  # Инициализация сессии

    async def close(self):
        """Закрытие сессии."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def standardize(self, raw_address: str) -> str:
        """
        Асинхронная стандартизация адреса через DaData API.
        """
        headers = {
            "Authorization": f"Token {self.api_key}",
            "X-Secret": self.secret_key,
            "Content-Type": "application/json",
        }
        data = [raw_address]

        async with self.session.post(self.BASE_URL, json=data, headers=headers) as response:
            if response.status != 200:
                error_message = await response.text()
                raise Exception(f"Ошибка при запросе к DaData: {response.status}, {error_message}")
            result = await response.json()
            return result[0]["result"]