from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from databases.instance.DB_setup import *



class DB:
    Base = declarative_base() #base class that table schema classes inehrit from

    engine = create_engine('sqlite:///databases/instance/database.db') #connects sqlalchemy engine to database file
    Session = sessionmaker(bind=engine) #binds session to engine
    session = Session() #creates session object



    # user functions below
    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and password:
            new_user = User(username=username, email=email, password=password)
            self.session.add(new_user) #adds user object
            self.session.commit() #commits changes to file
        else:
            print("add_user: Missing username or password, no user added")

    def get_users(self, username: str): #returns a list of dictionaries, one for each user
        #structure = session.query(table object).filter(operation on column object inside table object).all()/.first()

        if username:
            result = self.session.query(User).filter(User.username == username).all()
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
            result = self.session.query(Question).filter(Question.id == id).all()
        else:
            print("get_question: No id passed in")
            return []
        
        question_list = [question.__dict__ for question in result]

        for question_dict in question_list: #remove useless SQLAlchemy metadata from dictionaries
            question_dict.pop('_sa_instance_state',None)

        return question_list #should only return 1 or 0 elements

    def add_question(self, content: str, difficulty: int):
        if content and difficulty != None:
            new_question = Question(content=content, difficulty=difficulty)
            self.session.add(new_question) #adds user object
            self.session.commit()
            return new_question.id
        else:
            print("add_question: Missing question content or difficulty (should be 0 for undefined), no question added")

    #add update_question and really every other table's update function

    def add_answer(self, content: str, correct: bool, question_id: int):
        if content and correct != None and question_id: # correct != None because False is falsey value and false triggers null prevention lol
            new_answer = Answer(content=content, correct=correct, question_id=question_id)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        else:
            print("add_answer: Missing answer content, correct boolean, or question id, no answer added")

    def add_solution(self, content: str, question_id: int):
        if content and question_id:
            new_solution = Solution(content=content, question_id=question_id)
            self.session.add(new_solution)
            self.session.commit()
            return new_solution.id
        else:
            print("add_solution: Missing solution content or question id, no solution added")


        