from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from src.database import Base


class Entry(Base):
    """
    A class mapping to Entry table

    ...
    Attributes
    ----------
    id: int
        product id
    product_name: str
        the name of the product
    unit: str
        unit of the product(kgs)
    geography_id: int
        geography_id in which the product is based in
    impact: relationship
        impact of the product on environment based on various indicators

    Methods
    -------
    __repr__(self)
        Representation of the Entry object as a mapping to the actual record in the table
    """
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(VARCHAR(255))
    unit = Column(VARCHAR(45))
    geography_id = Column(Integer, ForeignKey('geography.id'))
    impact = relationship("Impact")

    def __repr__(self):
        return '<Entry %s>' % self.product_name
