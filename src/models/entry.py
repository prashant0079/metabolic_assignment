from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from src.database import Base


class Entry(Base):
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(VARCHAR(255))
    unit = Column(VARCHAR(45))
    geography_id = Column(Integer, ForeignKey('geography.id'))
    impact = relationship("Impact")

    def __repr__(self):
        return '<Entry %s>' % self.product_name
