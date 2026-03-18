from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)         
    best_lap_time = Column(Float)             
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)