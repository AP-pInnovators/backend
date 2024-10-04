# run file: uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel #handles how incoming json should be formatted and recieved/passed into endpoints
from databases.UserDB import UserDB

app = FastAPI()
userdb = UserDB()

@app.get("/api/test")
async def test():
    return {"greeting":"Hello world"}



class UserLoginJSON(BaseModel): #creates a pydantic class that models the expected incoming json for logging in/signing up
    username: str
    password: str

@app.post("/api/login")
async def login(user: UserLoginJSON):
    login_user = userdb.find_users(user.username)
    if len(login_user) > 1:
        print("Multiple users with the same username " + user.username + " exist")
        return {"success":"false",
                "error_code":"placeholder",
                "error_message":"Multiple users with the same username " + user.username + " exist"}
    if len(login_user) < 1:
        return {"success":"false",
                "error_code":"placeholder",
                "error_message":"No user exists"}
    login_user = login_user[0]
    if login_user["password"] == user.password:
        return {"success":"true",
                "session_token":"placeholder"}
    else:
        return {"success":"false",
                "error_code":"placeholder",
                "error_message":"Incorrect password"} #should 


class UserSignUpJSON(BaseModel): #creates a pydantic class that models the expected incoming json for logging in/signing up
    username: str
    email: str
    password: str

@app.post("/api/signup")
async def login(user: UserSignUpJSON):
    if len(userdb.find_users(user.username)) > 0:
        return {"success":"false",
                "error_code":"placeholder",
                "error_message":"Username already exists"}
    else:
        userdb.add_user(user.username, user.email, user.password)
        return {"success":"true",
                "session_token":"placeholder"}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)