from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqllite:///demo.db")

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    
Base.metadata.create_all(engine)