from sqlalchemy import Column, Integer, VARCHAR, CHAR
from sqlalchemy.orm import relationship
from src.database import Base


class Geography(Base):
    __tablename__ = "geography"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(CHAR(36))
    short_name = Column(VARCHAR(100))
    name = Column(VARCHAR(255))
    entries = relationship("Entry")

    def __repr__(self):
        return '<Geography %s>' % self.name
