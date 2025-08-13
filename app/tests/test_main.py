from fastapi.testclient import TestClient
from app.main import app

# Создаём клиент для тестирования
client = TestClient(app)

def test_standardize_valid_address():
    # Тестовый запрос
    response = client.post(
        "/standardize",
        json={"raw_address": "мск сухонска 11/-89"}
    )

    # Проверка ответа
    assert response.status_code == 200
    assert "г Москва, ул Сухонская, д 11, кв 89" in response.json()["standardized_address"]

def test_standardize_too_long_address():
    # Тестовый запрос с длинным адресом
    long_address = "рос федерация сам обл смоленский район ул. пушкина дом колотушкина квартира 55"
    response = client.post(
        "/standardize",
        json={"raw_address": long_address}
    )

    # Проверка ответа
    assert response.status_code == 400
    assert response.json()["detail"] == "Превышена длина входного запроса"