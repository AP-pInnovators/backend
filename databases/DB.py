from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import random

class DB:
    Base = declarative_base() #base class that table schema classes inehrit from

    def __init__(self, db_url='sqlite:///backend/databases/instance/app.db'):
        os.makedirs(os.path.dirname(db_url.split('///')[1]), exist_ok=True)

        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.create_tables()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

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

    # user functions below
    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and password:
            new_user = self.User(username=username, email=email, password=password)
            self.session.add(new_user) #adds user object
            self.session.commit() #commits changes to file
        else:
            print("add_user: Missing username or password, no user added")

    def add_user_problem(self, user_id: int, question_id: int, status: str = "current"):
        user_problem = self.UserProblems(user_id=user_id, question_id=question_id, status=status, seen=True)
        self.session.add(user_problem)
        self.session.commit()

    def update_user_stats(self, user_id: int, score: int):
        user_stat = self.session.query(self.UserStats).filter_by(user_id=user_id).first()
        if user_stat:
            user_stat.total_score += score
            user_stat.solved_problems_count += 1
        else:
            user_stat = self.UserStats(user_id=user_id, total_score=score, solved_problems_count=1)
            self.session.add(user_stat)
        self.session.commit()

    def update_user_score(self, user_id: int, question_id: int, attempts_taken: int, max_attempts: int):
        score = 100*(1 - ((attempts_taken - 1.0)/(max_attempts)))
        self.add_user_problem(user_id, question_id, status="solved")
        self.update_user_stats(user_id, score)

    def get_users(self, username: str): #returns a list of dictionaries, one for each user
        #structure = session.query(table object).filter(operation on column object inside table object).all()/.first()

        if username:
            result = self.session.query(self.User).filter(self.User.username == username).all()
        else:
            print("find_user: No username passed in")
            return []

        user_list = [user.__dict__ for user in result] #converts all returned user objects to dictionary

        for user_dict in user_list: #remove useless SQLAlchemy metadata from dictionaries
            user_dict.pop('_sa_instance_state',None)

        return user_list #returns all users matching the specified query (ideally 0 or 1, can be more but shouldnt)
    
    # question functions below
    def get_questions(self, id: int): #returns a list of dictionaries, one for each question (should only be 1 or 0)
        if id:
            result = self.session.query(self.Question).filter(self.Question.id == id).all()
        else:
            print("get_question: No id passed in")
            return []
        
        question_list = [question.__dict__ for question in result]

        for question_dict in question_list: #remove useless SQLAlchemy metadata from dictionaries
            question_dict.pop('_sa_instance_state',None)

        return question_list #should only return 1 or 0 elements
    
    def get_new_question(self, user_id: int):
        # get all questions that the user has seen
        seen_question_ids = self.session.query(self.UserProblems.question_id).filter(self.UserProblems.user_id == user_id).subquery()

        # query within the complement of those already seen questions
        unseen_questions = self.session.query(self.Question).filter(~self.Question.id.in_(seen_question_ids)).all()

        if not unseen_questions:
            print("No unseen questions available for this user.")
            return []

        # Select a random question from unseen questions
        random_question = random.choice(unseen_questions)

        # convert question to dictionary and remove the nonsense SQLAlchemy metadata
        question_dict = random_question.__dict__
        question_dict.pop('_sa_instance_state', None)

        return [question_dict]

    def add_question_answers_solutions(self, question: str, difficulty: int, answers: list, solutions: list):
        if question and answers:
            new_question = self.Question(content=question, difficulty=difficulty)
            self.session.add(new_question)
            self.session.commit()
            question_id = new_question.id
            for answer in answers:
                new_answer = self.Answer(content=answer["content"], correct=answer["correct"], question_id=question_id)
                self.session.add(new_answer)
            for solution in solutions:
                new_solution = self.Solution(content=solution["content"], question_id=question_id)
                self.session.add(new_solution)
            self.session.commit()
        else:
            print("add_question_answers_solutions: Missing question content or answers, no question added")

    def add_scraped(self, problem_text: str, correct_answer: str, difficulty: int):
        new_question = self.Question(content=problem_text, difficulty=difficulty)
        self.session.add(new_question)
        self.session.commit()
        
        answer = {
            "content": correct_answer,
            "correct": True,
            "question_id": new_question.id  # link to new question id
        }
        
        new_answer = self.Answer(**answer) # pointers!
        self.session.add(new_answer)
        self.session.commit()
        