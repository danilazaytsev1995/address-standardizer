from pydantic import BaseModel

class AddressRequest(BaseModel):
    raw_address: str


class AddressResponse(BaseModel):
    standardized_address: str