from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
# Create engine
engine = create_engine("sqlite:///data.sqlite3")
# Create session
Session = sessionmaker(bind=engine)
session = Session()
# Create Base
Base = declarative_base()
#Create product
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    expiry = Column(Date, nullable=False)
    expired = Column(Boolean, default=False)        
    def __str__(self):
        return f"Product: {self.name}, price: {self.price}, expiry: {self.expiry}"
    def is_expired(self):
        return datetime.today().date() > self.expiry
Base.metadata.create_all(engine)