from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.database import Base


class Indicator(Base):
    """
    A class mapping to Entry table

    ...
    Attributes
    ----------
    id: int
        primary key
    method: str
        method name
    category: str
        category name
    indicator: str
        indicator name
    impact: relationship
        relation of Indicator to the Impact table

    Methods
    -------
    __repr__(self)
        Representation of the Indicator object as a mapping to the actual record in the table

    """
    __tablename__ = "indicator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(VARCHAR(100))
    category = Column(VARCHAR(100))
    indicator = Column(VARCHAR(100))
    unit = Column(VARCHAR(45))
    impact = relationship("Impact")

    def __repr__(self):
        return '<Indicator %s>' % self.indicator
