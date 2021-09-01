from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, Float
from src.database import Base


class Impact(Base):
    """
    A class mapping to Impact table

    ...
    Attributes
    ----------
    id: int
        product id
    indicator_id: int
        indicator id
    entry_id: int
        entry id
    coefficient: int
        impact coefficient

    Methods
    -------
    __repr__(self)
        Representation of the Impact object as a mapping to the actual record in the table
    """

    __tablename__ = "impact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('indicator.id'))
    entry_id = Column(Integer, ForeignKey('entry.id'))
    coefficient = Column(Float)

    def __repr__(self):
        return '<Impact %s>' % self.coefficient
