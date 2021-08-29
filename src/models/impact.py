from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, Float
from src.database import Base


class Impact(Base):
    __tablename__ = "impact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(Integer, ForeignKey('indicator.id'))
    entry_id = Column(Integer, ForeignKey('entry.id'))
    coefficient = Column(Float)

    def __repr__(self):
        return '<Impact %s>' % self.coefficient
