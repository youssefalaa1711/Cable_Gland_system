from sqlalchemy import Column, Integer, Float, String
from database import Base

class Gland(Base):
    __tablename__ = "glands"

    id = Column(Integer, primary_key=True, index=True)
    min_size = Column(Float, nullable=False)
    max_size = Column(Float, nullable=False)
    gland_size = Column(String, nullable=False)
