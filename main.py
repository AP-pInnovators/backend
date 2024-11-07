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
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # set token expiration time in minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #generates a dependency that extracts the token from the Authorization header

def make_jwt_token(username: str) -> str:
    to_encode = {
        "sub":username #sub means subject, 
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
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
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
    login_user = db.get_users(user.username)
    if len(login_user) > 1:
        print("Multiple users with the same username " + user.username + " exist")
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Invalid credentials"}
    if len(login_user) < 1:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Invalid credentials"}
    login_user = login_user[0]
    if bcrypt.checkpw(user.password.encode('utf-8'), login_user["password"]):
        jwt_token = make_jwt_token(login_user["username"])
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
    if len(db.get_users(user.username)) > 0:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Username already exists"}
    else:
        db.add_user(user.username, user.email, bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()))
        return {"success":True}











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
            db.add_answer(answer.content, answer.correct, question_id)

        for solution in question.solutions:
            db.add_solution(solution.content, question_id)

        return {"success":True,
                "message":"placeholder"}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Question failed to be added"}
    

@app.get("/api/question/{question_id}")
async def question(question_id: int, current_user: str = Depends(get_username_from_jwt)):
    question = db.get_questions(question_id)
    if len(question) > 1:
        print("Multiple questions with the same id " + str(question_id) + " exist")
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Multiple questions with the same id " + str(question_id) + " exist"}
    if len(question) < 1:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"No question exists under id " + str(question_id)}
    question = question[0]
    # answers = db.get #MAKE A DB INTERACTABLE FUNCTION THAT GETS ANSWERS
    return {"success":True,
            "content":question["content"],
            "answers":"placeholder"}




class QuestionAddJSON(BaseModel):
    content: str
    difficulty: int
    answers: List[AnswerAddJSON]
    solutions: List[SolutionAddJSON]


class AnswerSubmissionJSON(BaseModel):
    answer: str

@app.post("/api/question/{question_id}")
async def question(question_id: int, current_user: str = Depends(get_username_from_jwt)):
    pass


# do a post for the question endpoint for answering the question


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config="log_conf.yaml") #working on it