from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from environs import Env

env = Env()
env.read_env()


engine = create_engine(f'postgresql://{env("DB_USER")}:{env("DB_PASSWORD")}@{env("DB_HOST")}:{env("DB_PORT")}/{env("DB_NAME")}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Adds(Base):
    __tablename__ = 'adds'

    id = Column(Integer, primary_key=True)
    img_url = Column(String)
    date_posted = Column(String)
    currency = Column(String)
    
    

