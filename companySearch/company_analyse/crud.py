from sqlalchemy.orm import Session

from company_analyse import models, schemas

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CreateCity):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(models.Company).join(models.Company.city).filter(models.City.name == city)  # 外键关联查询，这里不是像Django ORM那样Data.city.province
    return db.query(models.Company).offset(skip).limit(limit).all()

def get_company_by_name(db: Session, company_name: str = None):
    return db.query(models.Company).filter(models.Company.name == company_name).all()

def get_industry_by_name(db: Session, industry_name: str = None):
    return db.query(models.Company).filter(models.Company.bel_Industry==industry_name).all()

def create_city_data(db: Session, data: schemas.CreateCompany ,city_id: int):
    db_data = models.Company(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
