from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.database import Base


class Indicator(Base):
    __tablename__ = "indicator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(VARCHAR(100))
    category = Column(VARCHAR(100))
    indicator = Column(VARCHAR(100))
    unit = Column(VARCHAR(45))
    impact = relationship("Impact")

    def __repr__(self):
        return '<Indicator %s>' % self.indicator
