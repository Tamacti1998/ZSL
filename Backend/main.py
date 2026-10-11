from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import json

file_path = Path("profile.json")

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


@app.post("/learners")
def info(student: profile):
    data = student.model_dump()  # model_dump() converts pydantic model to python dictionary
    students.append(data)
    return data 

    # return {
    #     "message" : "Student added successfully",
        
    #     "students" : {
    #         "id" : student.id,
    #         "name" : student.name,
    #         "major" : student.major,
    #         "grad_year" : student.grad_year 
    #     }      
    # }

class phone(BaseModel):
    id : int
    brand : str
    model : str
    operating_system : str
    price : int
    color : str

@app.post("/post_phones")
def mobile(p_type : phone):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    new_data = p_type.model_dump()
    data.append(new_data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)   

    return {
        "text" : "Phone info saved successfully",
        "data" : new_data
    }

# PUT Request - basically used to update exisiting data/field or replace it with new data.
@app.put("/update_phones/{id}")
def mobile(p_type : phone, id : int):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    updated_data = p_type.model_dump()

    for idx, item in enumerate(data):
        if item["id"] == id:
            data[idx] = updated_data

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent = 4)

            return {
                "text" : "Phone info updated successfully",
                "data" : updated_data
            }
        
    return {
        "text" : "Phone info not found"
    }

#PATCH Request - allows to update specific field of an existing data
@app.patch("/patch_phones/{id}")
def mobile(p_type : phone, id : int):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    updated_data = p_type.model_dump()

    for idx, item in enumerate(data):
        if item["id"] == id:
            data[idx] = updated_data

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent = 4)

            return {
                "text" : "Phone info updated successfully",
                "data" : updated_data
            }
        
    return {
        "text" : "Phone info not found"
    }

@app.delete("/delete_phones/{id}")
def mobile(id : int):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    for idx, item in enumerate(data):
        if item["id"] == id:
            deleted_data = data.pop(idx)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent = 4)

            return {
                "text" : "Phone info deleted successfully",
                "data" : deleted_data
            }
        
    return {
        "text" : "Phone info not found"
    }