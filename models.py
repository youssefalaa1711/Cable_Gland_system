from sqlalchemy import Column, Integer, Float, String
from database import Base


class Gland(Base):
    __tablename__ = "glands"

    id = Column(Integer, primary_key=True, index=True)
    min_size = Column(Float, nullable=False)
    max_size = Column(Float, nullable=False)
    gland_size = Column(String, nullable=False)


class ArmouredGland(Base):
    __tablename__ = "armoured_glands"

    id = Column(Integer, primary_key=True, index=True)

    # Subtype groups: C1W, E1SW, C1X
    gland_type = Column(String, nullable=False, index=True)

    # Exact size such as: 20S, 20SS, 25S
    gland_size = Column(String, nullable=False)

    # Only used for E1SW (can be NULL for others)
    inner_min = Column(Float, nullable=True)
    inner_max = Column(Float, nullable=True)

    # Used for all types
    outer_min = Column(Float, nullable=False)
    outer_max = Column(Float, nullable=False)
