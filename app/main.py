from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.dadata_service import DadataService
from app.schemas.address import AddressRequest, AddressResponse

app = FastAPI()
dadata_service: DadataService


@app.on_event("startup")
async def startup():
    """Инициализация сервиса при старте приложения."""
    global dadata_service
    dadata_service = DadataService(api_key="817d7d45d012ac5497cb6ea4d88f47166daec015",
                                   secret_key="b576626f3a04fe8c5c97ed1d3933a0e73186ce19")


@app.on_event("shutdown")
async def shutdown():
    """Закрытие сессии при завершении работы приложения."""
    await dadata_service.close()


@app.post("/standardize", response_model=AddressResponse)
async def standardize_address(address_request: AddressRequest):
    """
    Стандартизация адреса через внешний сервис DaData.
    """
    if len(address_request.raw_address) > 60:
        raise HTTPException(status_code=400, detail="Превышена длина входного запроса")

    standardized_address = await dadata_service.standardize(address_request.raw_address)
    return AddressResponse(standardized_address=standardized_address)