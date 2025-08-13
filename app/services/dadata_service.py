import aiohttp
from typing import Optional

class DadataService:
    BASE_URL = "https://cleaner.dadata.ru/api/v1/clean/address"

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = aiohttp.ClientSession()  # Автоматическая инициализация

    async def close(self):
        """Закрывает сессию."""
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
                raise Exception(f"Ошибка при запросе к DaData: {response.status}")
            result = await response.json()
            return result[0]["result"]