from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.db.database import Base


class Geography(Base):
    """
    A class mapping to Entry table

    ...
    Attributes
    ----------
    id: int
        product id
    country_id: str
        id of the country
    short_name: str
        short name of the country
    name: str
        complete name of the country
    entry: relationship
        relation of Geography to the Entry table

    Methods
    -------
    __repr__(self)
        Representation of the Geography object as a mapping to the actual record in the table
    """

    __tablename__ = "geography"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(VARCHAR(36))
    short_name = Column(VARCHAR(100))
    name = Column(VARCHAR(255))
    entry = relationship("Entry")

    def __repr__(self):
        return '<Geography %s>' % self.name
