from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# enables communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text:str

class TextOut(BaseModel):
    result:str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/test")
async def test(data: TextIn):
    modified = data.text + "test"
    return {"result": modified}