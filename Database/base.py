# This module connects to the database using database credentials
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://root:dhansu123@localhost:3306/mysql')
Session = sessionmaker(bind=engine)

Base = declarative_base()
