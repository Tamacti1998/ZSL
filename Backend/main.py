from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = []

@app.get("/")
def root():
    return "Hello World!"

@app.get("/students")
def initial():
    students = [
        {
            "id" : "027400",
            "name" : "Tamacti Jun",
            "major" : "Computer Science",
            "grad_year" : "2030" 
        },

        {
            "id" : "339800",
            "name" : "Baba Voss",
            "major" : "Biology",
            "grad_year" : "2035"
        }
    ]
    return students

class profile(BaseModel):
    id : str
    name : str
    major : str
    grad_year : str

@app.post("/students")
def info(student: profile):
    students.append(student.model_dump())

    return {
        "message" : "Student added successfully",
        
        "students" : {
            "id" : student.id,
            "name" : student.name,
            "major" : student.major,
            "grad_year" : student.grad_year 
        }      
    }
