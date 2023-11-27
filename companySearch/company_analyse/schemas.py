from datetime import date as date_
from datetime import datetime

from pydantic import BaseModel


class CreateCity(BaseModel):
    name: str
    company_num: str

class ReadCity(CreateCity):
    id: int
    class Config:
        orm_mode = True

class CreateCompany(BaseModel):
    name: str
    address: str
    Business_Scope: str
    bel_Industry: str
    registered_capital: str

class ReadData(CreateCompany):
    id: int
    City_id: int

    class Config:
        orm_mode = True