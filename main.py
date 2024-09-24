# run file: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/")
async def root():
 return {"greeting":"Hello world"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)