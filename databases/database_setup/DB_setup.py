from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database



Base = declarative_base() #base class that table schema classes inehrit from

engine = create_engine('sqlite:///databases/instance/database.db') #connects sqlalchemy engine to database file

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine) #binds session to engine
session = Session() #creates session object

class User(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

class Question(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)

class Answer(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    correct = Column(Boolean)
    question_id = Column(Integer)

class Solution(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Solutions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    question_id = Column(Integer)

class UserResponses(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'UserResponses'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    question_id = Column(Integer)
    answer_id = Column(Integer)
    submission_time = Column(Integer) #in seconds or milliseconds ideally
    answer_time = Column(Integer) #same as above, this should be how long it took them


Base.metadata.create_all(engine) #creates all tables defined under the base object in the database if it doesn't exist (running the script again wont overwrite it)