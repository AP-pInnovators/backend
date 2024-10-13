# run file: uvicorn main:app --reload

from fastapi import FastAPI, Request

from pydantic import BaseModel #handles how incoming json should be formatted and recieved/passed into endpoints
from typing import List #works with above

from databases.DB import DB #class made to handle all database interaction (2 methods, add_user and find_user)

import time

app = FastAPI()
db = DB()



#below is the file writing/logging function (just for abstraction)
def log(endpoint, ip, message):
    with open("logFile.txt", "at") as logFile: #'at' stands for "append text file"
        logFile.write(str(endpoint) + " (" + str(ip) +") - " + time.strftime("%m/%d/%Y") + "@" + time.strftime("%H:%M:%S", time.localtime()) + " | " + str(message) + "\n")

#log server startup
log("api/", "server", "Server Started")

'''
https://gist.github.com/liviaerxin/d320e33cbcddcc5df76dd92948e5be3b
use this for logging, not the function above
also refer below if needed to get ip/port from request

'''


@app.get("/api/test")
async def test(request: Request):
    log("api/test", str(request.client), "Success")
    print(request.client)
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
                "error_message":"Multiple users with the same username " + user.username + " exist"}
    if len(login_user) < 1:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"No user exists"}
    login_user = login_user[0]
    if login_user["password"] == user.password:
        return {"success":True,
                "session_token":"placeholder"}
    else:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Incorrect password"} #refer to todo (make sure messages are different due to cybersecurity reasons)


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
        db.add_user(user.username, user.email, user.password)
        return {"success":True,
                "session_token":"placeholder"}



class AnswerAddJSON(BaseModel):
    content: str
    correct: bool

class SolutionAddJSON(BaseModel):
    content: str

class QuestionAddJSON(BaseModel):
    question: str
    answers: List[AnswerAddJSON]
    solutions: List[SolutionAddJSON]



@app.post("/api/add_question/")
async def add_question(question: QuestionAddJSON):
    answers = []
    for answer in question.answers: #turns all answer json into dict
        answers.append(answer.__dict__)
    solutions = []
    for solution in question.solutions: #turns all solution json into dict
        solutions.append(solution.__dict__)
    try:
        db.add_question_answers_solutions(question.question, answers, solutions)
        return {"success":True,
                "message":"placeholder"}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Question failed to be added"}
    

@app.get("/api/question/{question_id}")
async def question(question_id: int):
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
    return {"success":True,
            "content":question["content"]}

# do a post for the question endpoint for answering the question


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)