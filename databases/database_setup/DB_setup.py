from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
import os


Base = declarative_base() #base class that table schema classes inehrit from

os.makedirs(os.path.dirname('sqlite:///backend/databases/instance/app.db'.split('///')[1]), exist_ok=True)
engine = create_engine('sqlite:///backend/databases/instance/app.db') #connects sqlalchemy engine to database file

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
    difficulty = Column(Integer)  # difficulty level

class Answer(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('Questions.id'))

class Solution(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Solutions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    question_id = Column(Integer, ForeignKey('Questions.id'))

class UserResponses(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'UserResponses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    question_id = Column(Integer, ForeignKey('Questions.id'))
    answer_id = Column(Integer, ForeignKey('Answers.id'))
    submission_time = Column(Integer) #in seconds or milliseconds ideally
    answer_time = Column(Integer) #same as above, this should be how long it took them
    attempts = Column(Integer, default=1)  # Tracks submission attempts

class UserProblems(Base):
    __tablename__ = 'UserProblems'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    question_id = Column(Integer, ForeignKey('Questions.id'))
    status = Column(String)  # "current" or "solved"
    max_attempts = Column(Integer)  # Based on difficulty

class UserStats(Base):
    __tablename__ = 'UserStats'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    total_score = Column(Integer, default=0)  # cumulative score for solved problems !
    solved_problems_count = Column(Integer, default=0)  # number of problems solved all time


Base.metadata.create_all(engine) #creates all tables defined under the base object in the database if it doesn't exist (running the script again wont overwrite it)