from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from databases.instance.DB_setup import *



class DB:
    Base = declarative_base() #base class that table schema classes inehrit from

    engine = create_engine('sqlite:///databases/instance/database.db') #connects sqlalchemy engine to database file
    Session = sessionmaker(bind=engine) #binds session to engine
    session = Session() #creates session object



    def dictify(self, result):
        dict = [row.__dict__ for row in result]

        for row_dict in dict: #remove useless SQLAlchemy metadata from dictionaries
            row_dict.pop('_sa_instance_state',None)

        return dict #should only return 1 or 0 elements

    #add update_question and really every other table's update function



    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and email and password:
            new_user = User(username=username, email=email, password=password)
            self.session.add(new_user)
            self.session.commit() #commits changes to file
            return new_user.id
        else:
            print("add_user: Missing username, email, or password, no user added")
            return None

    def get_users(self, username: str): #returns a list of dictionaries, one for each user
        #structure = session.query(table object).filter(operation on column object inside table object).all()/.first()
        if username:
            result = self.session.query(User).filter(User.username == username).all()
            if len(result) > 1:
                print("get_users: More than one user with username " + username + " exists, this shouldn't happen")
                return None
            if len(result) < 1:
                print("get_users: No users exist with user id")
                return None
            return self.dictify(result) #returns all users matching the specified query (ideally 0 or 1, can be more but shouldnt)
        else:
            print("get_users: No username passed in")
            return None
    


    def add_user_stats(self, user_id: str):
        if user_id:
            new_user_stats = UserStatistics(user_id=user_id, total_score=0, solved_problems_count=0)
            self.session.add(new_user_stats) #adds user object
            self.session.commit() #commits changes to file
            return new_user_stats.id
        else:
            print("add_user_stats: Missing user id, no user stats added")
            return None
        
    def get_user_stats(self, user_id: str): #returns a list of dictionaries, one for each user
        if user_id:
            result = self.session.query(UserStatistics).filter(UserStatistics.user_id == user_id).all()
            return self.dictify(result) #returns all user statistics matching the specified query (ideally 0 or 1, can be more but shouldnt)
        else:
            print("get_user_stats: No user id passed in")
            return None

    def update_user_stats(self, user_id, added_score, added_problem_count):
        if user_id and added_score != None and added_problem_count != None:
            user_stats = self.session.query(UserStatistics).filter(UserStatistics.user_id == user_id).all()
            if len(user_stats) > 1:
                print("update_user_stats: More than one user stats exist, this shouldn't happen; nothing updated")
                return None
            if len(user_stats) < 1:
                print("update_user_stats: No user stats exist for that user id; nothing updated")
                return None
            user_stats = user_stats[0]
            user_stats.total_score += added_score
            user_stats.solved_problems_count += added_problem_count
            self.session.commit() #commits changes to file
            return user_stats.id
        else:
            print("update_user_stats: User id, added score, or added_problem_count not passed in; nothing updated")
            return None

    

    def get_questions(self, id: int): #returns a list of dictionaries, one for each question (should only be 1 or 0)
        if id:
            result = self.session.query(Question).filter(Question.id == id).all()
        else:
            print("get_question: No id passed in")
            return []
        
        return self.dictify(result) #should only return 1 or 0 elements

    def add_question(self, content: str, difficulty: int):
        if content and difficulty != None:
            new_question = Question(content=content, difficulty=difficulty)
            self.session.add(new_question) #adds user object
            self.session.commit()
            return new_question.id #necessary to link answers and solutions
        else:
            print("add_question: Missing question content or difficulty (should be 0 for undefined), no question added")



    def add_answer(self, content: str, correct: bool, question_id: int):
        if content and correct != None and question_id: # correct != None because False is falsey value and false triggers null prevention lol
            new_answer = Answer(content=content, correct=correct, question_id=question_id)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        else:
            print("add_answer: Missing answer content, correct boolean, or question id, no answer added")

    def get_answers(self, question_id: int):
        if question_id:
            result = self.session.query(Answer).filter(Answer.question_id == question_id).all()
        else:
            print("get_answer: No question_id passed in")
            return []
        
        return self.dictify(result)



    def add_solution(self, content: str, question_id: int):
        if content and question_id:
            new_solution = Solution(content=content, question_id=question_id)
            self.session.add(new_solution)
            self.session.commit()
            return new_solution.id
        else:
            print("add_solution: Missing solution content or question id, no solution added")

    def get_solutions(self, question_id: int):
        if question_id:
            result = self.session.query(Solution).filter(Solution.question_id == question_id).all()
        else:
            print("get_solution: No question_id passed in")
            return []
        
        return self.dictify(result)



    def add_user_response(self, user_id: str, question_id: int, answer_id: int, submission_time: int):
        if user_id and question_id and answer_id and submission_time:
            new_answer = UserResponse(user_id=user_id, question_id=question_id, answer_id=answer_id, submission_time=submission_time)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        else:
            print("add_user_response: Missing user id, question id, answer id, or submission time, no answer added")

    def get_user_responses(self, user_id: int, question_id: int):
        if user_id and question_id:
            result = self.session.query(UserResponse).filter(UserResponse.user_id == user_id and UserResponse.question_id == question_id).all()
        else:
            print("get_user_responses: No user id or question id passed in")
            return []
        
        return self.dictify(result)
    


    def add_user_response(self, user_id: str, question_id: int, answer_id: int, submission_time: int):
        if user_id and question_id and answer_id and submission_time:
            new_answer = UserResponse(user_id=user_id, question_id=question_id, answer_id=answer_id, submission_time=submission_time)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        else:
            print("add_user_response: Missing user id, question id, answer id, or submission time, no answer added")

    def get_user_responses(self, user_id: int, question_id: int):
        if user_id and question_id:
            result = self.session.query(UserResponse).filter(UserResponse.user_id == user_id and UserResponse.question_id == question_id).all()
        else:
            print("get_user_responses: No user id or question id passed in")
            return []
        
        return self.dictify(result) #should only return 1 or 0 elements