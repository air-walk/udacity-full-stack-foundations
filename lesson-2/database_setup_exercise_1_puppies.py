import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
  __tablename__ = 'shelter'

  id      = Column(Integer, primary_key = True)
  name    = Column(String(80), nullable = False)
  address = Column(String(250))
  city    = Column(String(100))
  state   = Column(String(100))
  zipCode = Column(String(10))
  website = Column(String(150))


class Puppy(Base):
  __tablename__ = 'puppy'

  id            = Column(Integer, primary_key = True)
  name          = Column(String(80), nullable = False)
  date_of_birth = Column(Date)
  gender        = Column(String(10))
  weight        = Column(Numeric(10))
  shelter_id    = Column(Integer, ForeignKey('shelter.id'))

  shelter       = relationship(Shelter)

  picture       = Column(String(250))

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)