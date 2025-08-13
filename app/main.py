from fastapi import FastAPI, HTTPException, Depends
from app.services.dadata_service import DadataService
from app.schemas.address import AddressRequest, AddressResponse
from dotenv import load_dotenv
import os

app = FastAPI()

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных окружения
DADATA_API_KEY = os.getenv("DADATA_API_KEY")
DADATA_SECRET_KEY = os.getenv("DADATA_SECRET_KEY")

async def get_dadata_service():
    """Зависимость для создания и закрытия DadataService."""
    dadata_service = DadataService(api_key=DADATA_API_KEY,
                                   secret_key=DADATA_SECRET_KEY)
    yield dadata_service
    await dadata_service.close()


@app.post("/standardize", response_model=AddressResponse)
async def standardize_address(
    address_request: AddressRequest, dadata_service: DadataService = Depends(get_dadata_service)
):
    """
    Стандартизация адреса через внешний сервис DaData.
    """
    if len(address_request.raw_address) > 60:
        raise HTTPException(status_code=400, detail="Превышена длина входного запроса")

    try:
        standardized_address = await dadata_service.standardize(address_request.raw_address)
        return AddressResponse(standardized_address=standardized_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))