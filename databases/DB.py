from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base



class DB:
    Base = declarative_base() #base class that table schema classes inehrit from

    engine = create_engine('sqlite:///databases/instance/database.db') #connects sqlalchemy engine to database file
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



    # user functions below
    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and password:
            new_user = self.User(username=username, email=email, password=password)
            self.session.add(new_user) #adds user object
            self.session.commit() #commits changes to file
        else:
            print("add_user: Missing username or password, no user added")

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

    
    def add_question_answers_solutions(self, question: str, answers: list, solutions: list):
        if question and answers:
            new_question = self.Question(content=question)
            self.session.add(new_question) #adds user object
            self.session.commit()
            question_id = new_question.id
            for answer in answers: #adds all answers referencing the question id
                new_answer = self.Answer(content=answer["content"], correct=answer["correct"], question_id=question_id)
                self.session.add(new_answer)
            for solution in solutions: #adds all solutions referencing the question id
                new_solution = self.Solution(content=solution["content"], question_id=question_id)
                self.session.add(new_solution)
            self.session.commit()
        else:
            print("add_question_answers_solutions: Missing question content or answers, no question added")
        