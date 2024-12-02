from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
import os


#DONT FORGET TO RUN THIS IN THE ROOT DIRECTORY OF THE PROJECT (where main.py is located) OR NONE OF THIS WILL WORK

reset_database = False #if you wanna reset your database completely (remove all existing entries) then turn this to true
if reset_database and os.path.exists("databases\\instance\\database.db"):
    os.remove("databases\\instance\\database.db")


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

class UserStatistics(Base):
    __tablename__ = 'UserStatistics'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    total_score = Column(Integer, default=0)  # cumulative score for solved problems (sum of difficlty of all solved problems)
    solved_problems_count = Column(Integer, default=0)  # number of problems solved all time

class Question(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    difficulty = Column(Integer)

class Answer(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('Questions.id'))
    content = Column(String)
    correct = Column(Boolean)
    
class Solution(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'Solutions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('Questions.id'))
    content = Column(String)
    
class UserResponse(Base): #inherits from declarative_base object to define how a table is structured
    __tablename__ = 'UserResponses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    question_id = Column(Integer, ForeignKey('Questions.id'))
    answer_id = Column(Integer, ForeignKey('Answers.id'))
    submission_time = Column(Integer) #in seconds or milliseconds ideally

class UserProblemStatus(Base):
    __tablename__ = 'UserProblemStatuses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    question_id = Column(Integer, ForeignKey('Questions.id'))
    viewing_status = Column(Boolean) # whether the user is currently viewing the question or not (only one question will be like this at a time per user)
    correct_status = Column(Boolean)  # true if the question has been correctly answered, false if not
    attempt_count = Column(Integer)  # how many attempts a user has spent on a question (will affect score based on answer count too)
    creation_date = Column(Integer) # the first time the user looks at a question a row for the user and question will be created and the creation date will be the first viewed time




Base.metadata.create_all(engine) #creates all tables defined under the base object in the database if it doesn't exist (running the script again wont overwrite it)