# run file: uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel #handles how incoming json should be formatted and recieved/passed into endpoints
from typing import List #works with above

from databases.DB import DB #class made to handle all database interaction (2 methods, add_user and find_user)

import bcrypt

import jwt

import logging

import time

from datetime import datetime, timedelta, timezone

import os




SECRET_KEY = os.environ.get("PATH", "pathpathpathlol")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5259492  # set token expiration time in minutes (1 year right now)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #generates a dependency that extracts the token from the Authorization header

def make_jwt_token(username: str, user_id: int) -> str:
    to_encode = {
        "sub":username, #sub means subject
        "user_id":user_id
    }
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #time to expire, adds an amount of time to the current utc time
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Depends(oauth2_scheme) in get_username_from_jwt retrieves the token from the Authorization header (in Bearer format) without needing additional code in the endpoint
def get_username_from_jwt(token: str = Depends(oauth2_scheme)): #given a 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, "username": username}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )



app = FastAPI()
db = DB()
# logger = logging.getLogger(__name__) #still working on getting it to log to a file



'''
https://gist.github.com/liviaerxin/d320e33cbcddcc5df76dd92948e5be3b
use this for logging in the
also refer to test endpoint if needed to get ip/port from request
'''








@app.get("/api/test")
async def test():
    return {"greeting":"Hello world"}



class UserLoginJSON(BaseModel): #creates a pydantic class that models the expected incoming json for logging in/signing up
    username: str
    password: str

@app.post("/api/login")
async def login(user: UserLoginJSON):
    login_user = db.get_user_by_username(user.username)
    if login_user:
        if bcrypt.checkpw(user.password.encode('utf-8'), login_user["password"]):
            jwt_token = make_jwt_token(login_user["username"], login_user["id"])
            return {"success":True,
                    "access_token":jwt_token,
                    "token-type":"bearer"}
    else:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Invalid credentials"} #refer to todo (make sure messages are different due to cybersecurity reasons)



class UserSignUpJSON(BaseModel): #creates a pydantic class that models the expected incoming json for logging in/signing up
    username: str
    email: str
    password: str

@app.post("/api/signup")
async def signup(user: UserSignUpJSON):
    if not db.get_user_by_username(user.username):
        user_id = db.add_user(user.username, user.email, bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()))
        db.add_user_statistics(user_id)
        return {"success":True}
    else:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Username already exists"}



class AnswerAddJSON(BaseModel):
    content: str
    correct: bool

class SolutionAddJSON(BaseModel):
    content: str

class QuestionAddJSON(BaseModel):
    content: str
    difficulty: int
    answers: List[AnswerAddJSON]
    solutions: List[SolutionAddJSON]

@app.post("/api/add_question/")
async def add_question(question: QuestionAddJSON, current_user: str = Depends(get_username_from_jwt)):
    answers = []
    for answer in question.answers: #turns all answer json into dict
        answers.append(answer.__dict__)
    solutions = []
    for solution in question.solutions: #turns all solution json into dict
        solutions.append(solution.__dict__)
    try:
        question_id = db.add_question(question.content, difficulty=question.difficulty)
        for answer in question.answers:
            db.add_answer(question_id, answer.content, answer.correct)

        for solution in question.solutions:
            db.add_solution(question_id, solution.content)

        return {"success":True,
                "message":"placeholder"}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Question failed to be added"}
    


@app.get("/api/question/{question_id}")
async def get_question(question_id: int, current_user: str = Depends(get_username_from_jwt)):
    question = db.get_question(question_id)
    answers = db.get_answers(question_id)
    for answer in answers: #need to remove database id stuff as well as the answer bool (no cheating...)
        del answer["question_id"]
        del answer["correct"]
    if question and answers:
        return {"success":True,
                "content":question["content"],
                "answers":answers}
    else:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Question does not exist or a question's answers are missing"}



class AnswerSubmissionJSON(BaseModel):
    content: str

@app.post("/api/question/{question_id}")
async def submit_answer(question_id: int, answer: AnswerSubmissionJSON, current_user: str = Depends(get_username_from_jwt)):
    try:
        problem_status = db.get_user_problem_status(current_user["user_id"], question_id)
        if (problem_status == None):
            db.add_user_problem_status(current_user["user_id"], question_id, True, False, 5, datetime.now(timezone.utc))
            problem_status = db.get_user_problem_status(current_user["user_id"], question_id)
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Failed to get user problem status from database"}
    if not problem_status["viewing_status"]:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"User must be viewing question first to submit answer"}
    try:
        db.add_user_response(current_user["user_id"], question_id, answer.content, datetime.now(timezone.utc))
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Failed to add user response to database"}
    try:
        correct = False
        for answer_result in db.get_answers(question_id):
            if answer_result["correct"] == True and answer_result["content"] == answer.content:
                correct = True
                continue
        try:
            new_attempt_count = problem_status["attempt_count"] - int(not correct)
            if (new_attempt_count >= 0):         
                db.update_user_problem_status(current_user["user_id"], question_id, None, correct, new_attempt_count, None)
        except:
            return {"success":False,
                "error_code":"placeholder",
                "error_message":"User question status failed to be updated"}
        if not correct:
            return {"success":True,
                    "correct":correct,
                    "attempts":new_attempt_count,
                    "score":0}
        else:
            try:
                user_stats = db.get_user_statistics(current_user["user_id"])
                if (user_stats == None):
                    db.add_user_statistics(current_user["user_id"])
                    user_stats = db.get_user_statistics(current_user["user_id"])
                    
                db.update_user_statistics(current_user["user_id"], new_attempt_count*100, 1)
                print(user_stats["total_score"])
                
                return {"success":True,
                        "correct":correct,
                        "attempts":new_attempt_count,
                        "score":new_attempt_count*100}
            except:
                return {"success":False,
                        "error_code":"placeholder",
                        "error_message":"User stats failed to be updated"}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Answer failed to be checked"}
        
@app.get("/api/recommendation")
async def recommend_question(current_user: str = Depends(get_username_from_jwt)):
    try:
        question = db.get_new_question(current_user["user_id"])
        return {"success":True,
                "id":question["id"]}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Failed to recommend question"}

@app.get("/api/stats")
async def get_stats(current_user: str = Depends(get_username_from_jwt)):
    try:
        stats = db.get_user_statistics(current_user["user_id"])
        return {"success":True,
                "score":stats["total_score"]}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Failed to get stats"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config="log_conf.yaml") #working on it