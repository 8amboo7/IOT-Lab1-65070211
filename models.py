from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    detail = Column(String, index=True)
    story = Column(String, index=True)
    classification = Column(String, index=True)
    is_published = Column(Boolean, index=True)

class Menu(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    detail = Column(String, index=True)
    ingredient = Column(String, index=True)
    is_published = Column(Boolean, index=True)
    
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    total = Column(Integer, index=True)
    note = Column(String, index=True)
    
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    dob = Column(String, index=True)
    sex = Column(String, index=True)