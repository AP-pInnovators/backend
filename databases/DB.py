from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from databases.instance.DB_setup import *



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



    def dictify(self, result):
        dict = [row.__dict__ for row in result] #can handle multiple results, returns a list of dictionaries (each one is a result)

        for row_dict in dict: #remove useless SQLAlchemy metadata from dictionaries
            row_dict.pop('_sa_instance_state',None)

        return dict #should only return 1 or 0 elements



    #add functions
    #get functions
    #update functions


    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and email and password:
            new_user = User(username=username, email=email, password=password)
            self.session.add(new_user)
            self.session.commit() #commits changes to file
            return new_user.id
        else:
            print("add_user: Missing username, email, or password, no user added")
            return None

    def get_user_by_username(self, username: str): #returns a list of dictionaries, one for each user
        #structure = session.query(table object).filter(operation on column object inside table object).all()/.first()
        if username:
            result = self.session.query(User).filter(User.username == username).all()
            if len(result) > 1:
                print("get_user_by_username: Duplicate user id")
                return None
            if len(result) < 1:
                print("get_user_by_username: No users found")
                return None
            return self.dictify(result)[0] #returns all users matching the specified query (ideally 0 or 1, can be more but shouldnt)
        else:
            print("get_user_by_username: No username passed in")
            return None
    
    def get_user_by_id(self, user_id: int):
        if user_id:
            result = self.session.query(User).filter(User.id == user_id).all()
            if len(result) > 1:
                print("get_user_by_id: Duplicate user id")
                return None
            if len(result) < 1:
                print("get_user_by_id: No users found")
                return None
            return self.dictify(result)[0]
        else:
            print("get_user_by_id: No user_id passed in")
            return None
        
    def update_user(self, user_id: int, username: str, email: str, password: str):
        if user_id:
            result = self.session.query(User).filter(User.id == user_id).all()
            if len(result) > 1:
                print("update_user: Duplicate user id")
                return None
            if len(result) < 1:
                print("update_user: No users found")
                return None
            result = result[0]
            if username:
                result.username = username
            if email:
                result.email = email
            if password:
                result.password = password
            self.session.commit() #commits changes to file
            return result.id
        else:
            print("update_user: No user id passed in")
            return None
    


    def add_user_statistics(self, user_id: int):
        if user_id:
            new_user_stats = UserStatistics(user_id=user_id, total_score=0, solved_problems_count=0)
            self.session.add(new_user_stats)
            self.session.commit()
            return new_user_stats.user_id
        else:
            print("add_user_stats: Missing user id, no user stats added")
            return None
        
    def get_user_statistics(self, user_id: int):
        if user_id:
            result = self.session.query(UserStatistics).filter(UserStatistics.user_id == user_id).all()
            if len(result) > 1:
                print("get_user_stats: Duplicate user id")
                return None
            if len(result) < 1:
                print("get_user_stats: No users found")
                return None
            return self.dictify(result)[0]
        else:
            print("get_user_stats: No user_id passed in")
            return None

    def update_user_statistics(self, user_id: int, added_score: int, added_problem_count: int):
        if user_id:
            result = self.session.query(UserStatistics).filter(UserStatistics.user_id == user_id).all()
            if len(result) > 1:
                print("update_user_stats: Duplicate user id")
                return None
            if len(result) < 1:
                print("update_user_stats: No users found")
                return None
            result = result[0]
            if added_score:
                result.total_score += added_score
            if added_problem_count:
                result.solved_problems_count += added_problem_count
            self.session.commit() #commits changes to file
            return result.user_id
        else:
            print("update_user_stats: No user id passed in")
            return None



    def add_question(self, content: str, difficulty: int):
        if content and difficulty != None:
            new_question = Question(content=content, difficulty=difficulty)
            self.session.add(new_question)
            self.session.commit()
            return new_question.id #necessary to link answers and solutions
        else:
            print("add_question: Missing content or difficulty (should be 0 for undefined), no question added")
            return None
        
    def get_question(self, question_id: int):
        if question_id:
            result = self.session.query(Question).filter(Question.id == question_id).all()
            if len(result) > 1:
                print("get_question: Duplicate question id")
                return None
            if len(result) < 1:
                print("get_question: No question found")
                return None
            return self.dictify(result)[0]
        else:
            print("get_question: No question_id passed in")
            return None



    def add_answer(self, question_id: int, content: str, correct: bool):
        if content and correct != None and question_id: # correct != None because False is falsey value and false triggers null prevention lol
            new_answer = Answer(question_id=question_id, content=content, correct=correct)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        else:
            print("add_answer: Missing question id, answer content, or correct boolean, no answer added")
            return None

    def get_answers(self, question_id: int):
        if question_id:
            result = self.session.query(Answer).filter(Answer.question_id == question_id).all()
            return self.dictify(result) #dont need to handle multiple results because multiple results are expected
        else:
            print("get_answers: No question_id passed in")
            return None



    def add_solution(self, question_id: int, content: str):
        if content and question_id:
            new_solution = Solution(question_id=question_id, content=content)
            self.session.add(new_solution)
            self.session.commit()
            return new_solution.id
        else:
            print("add_solution: Missing question id or solution content, no solution added")
            return None

    def get_solutions(self, question_id: int):
        if question_id:
            result = self.session.query(Solution).filter(Solution.question_id == question_id).all()
            return self.dictify(result)
        else:
            print("get_solutions: No question_id passed in")
            return None
        


    def add_user_response(self, user_id: int, question_id: int, answer_id: int, submission_time: int):
        if user_id and question_id and answer_id and submission_time:
            new_response = UserResponse(user_id=user_id, question_id=question_id, answer_id=answer_id, submission_time=submission_time)
            self.session.add(new_response)
            self.session.commit()
            return new_response.id
        else:
            print("add_user_response: Missing user id, question id, answer id, or submission time, no answer added")
            return None

    def get_user_responses(self, user_id: int, question_id: int):
        if user_id and question_id:
            result = self.session.query(UserResponse).filter(UserResponse.user_id == user_id and UserResponse.question_id == question_id).all()
            return self.dictify(result)
        else:
            print("get_user_responses: No user id or question id passed in")
            return None



    def add_user_problem_status(self, user_id: int, question_id: int, viewing_status: bool, correct_status: bool, attempt_count: int, creation_date: int):
        if user_id and question_id and viewing_status != None and correct_status != None and attempt_count != None and creation_date:
            new_user_problem_status = UserProblemStatus(user_id=user_id, question_id=question_id, viewing_status=viewing_status, correct_status=correct_status, attempt_count=attempt_count, creation_date=creation_date)
            self.session.add(new_user_problem_status)
            self.session.commit()
            return new_user_problem_status.id
        else:
            print("add_user_problem_status: Missing user id, question id, viewing_status, correct_status, attempt_count, or creation_date, no user status added")
            return None
        
    def get_user_problem_status(self, user_id: int, question_id: int):
        if user_id and question_id:
            result = self.session.query(UserProblemStatus).filter(UserProblemStatus.user_id == user_id and UserProblemStatus.question_id == question_id).all()
            if len(result) > 1:
                print("get_user_problem_status: Duplicate user id and question id")
                return None
            if len(result) < 1:
                print("get_user_problem_status: No question status found for user id or question id")
                return None
            return self.dictify(result)[0]
        else:
            print("get_user_problem_status: No user_id or question_id passed in") #ideally i should change all these messages to "missing 1 or more arguments"
            return None

    def update_user_problem_status(self, user_id: int, question_id: int, viewing_status: bool, correct_status: bool, attempt_count: int, creation_date: int):
        if user_id and question_id:
            result = self.session.query(UserProblemStatus).filter(UserProblemStatus.user_id == user_id and UserProblemStatus.question_id == question_id).all()
            if len(result) > 1:
                print("get_user_problem_status: Duplicate user id and question id")
                return None
            if len(result) < 1:
                print("get_user_problem_status: No question status found for user id or question id")
                return None
            result = result[0]
            if viewing_status:
                result.viewing_status = viewing_status
            if correct_status:
                result.correct_status = correct_status
            if attempt_count:
                result.attempt_count = attempt_count
            if creation_date:
                result.creation_date = creation_date
            self.session.commit() #commits changes to file
            return result.id
        else:
            print("get_user_problem_status: No user_id or question_id passed in")
            return None