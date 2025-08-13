import os
from fastapi import FastAPI, HTTPException, Depends
from app.services.dadata_service import DadataService
from app.schemas.address import AddressRequest, AddressResponse
from dotenv import load_dotenv

app = FastAPI()
# Загрузка переменных окружения из файла .env
load_dotenv()
service_name = os.getenv("SERVICE_NAME")

async def get_dadata_service():
    """Зависимость для создания и закрытия DadataService."""
    service = DadataService()
    yield service
    await service.close()

def get_service(name: str):
    match name:
        case 'dadata':
            return get_dadata_service
        case _:
            raise Exception('Неизвестный сервис')

@app.post("/standardize", response_model=AddressResponse)
async def standardize_address(
    address_request: AddressRequest, service = Depends(get_service(service_name))):
    """
    Стандартизация адреса через внешний сервис.
    """
    if len(address_request.raw_address) > 60:
        raise HTTPException(status_code=400, detail="Превышена длина входного запроса")

    try:
        standardized_address = await service.standardize(address_request.raw_address)
        return AddressResponse(standardized_address=standardized_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))