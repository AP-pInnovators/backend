from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database



Base = declarative_base() #base class that table schema classes inehrit from

engine = create_engine('sqlite:///databases/instance/users.db') #connects sqlalchemy engine to database file

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine) #binds session to engine
session = Session() #creates session object

class User(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


Base.metadata.create_all(engine) #creates all tables defined under the base object in the database if it doesn't exist (running the script again wont overwrite it)