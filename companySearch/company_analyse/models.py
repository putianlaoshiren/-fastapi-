from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, comment='省的名字')
    company_num=Column(BigInteger, nullable=False, comment='公司数量')

    companies = relationship('Company', back_populates='city')

    __mapper_args__ = {"order_by": company_num}

class Company(Base):
    __tablename__ = 'Company'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment='公司名字')
    address=Column(String(100), nullable=False, comment='地址')
    Business_Scope = Column(String(100), nullable=False, comment='经营范围')
    bel_Industry = Column(String(100), nullable=False, comment='所处行业')
    registered_capital=Column(String(100), nullable=False, comment='注册资本')

    City_id=Column(Integer, ForeignKey('city.id'),comment='城市id')

    city = relationship('City', back_populates='companies')
