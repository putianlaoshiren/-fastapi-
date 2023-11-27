from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from company_analyse import crud, schemas
from company_analyse.database import engine, Base, SessionLocal

conapplication = APIRouter()

templates = Jinja2Templates(directory='./company_analyse/templates')

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@conapplication.post("/create_city", response_model=schemas.ReadCity)
def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)


@conapplication.get("/get_city/{city}", response_model=schemas.ReadCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@conapplication.get("/get_cities", response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@conapplication.post("/create_data", response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateCompany, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data

@conapplication.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return data

@conapplication.get("/city")
def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
    })

@conapplication.get("/company")
def get_company_by_name(request: Request, Companyname: str = None, db: Session = Depends(get_db)):
    data = crud.get_company_by_name(db, company_name=Companyname)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
    })

@conapplication.get("/Industry")
def get_company_by_name(request: Request, Indestryname: str = None, db: Session = Depends(get_db)):
    data = crud.get_industry_by_name(db, industry_name=Indestryname)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
    })