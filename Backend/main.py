from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from pathlib import Path
import json
from DB import get_db
from models import Movies


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

class user_phone(BaseModel):
    id : int | None = None
    brand : str | None = None
    model : str | None = None
    operating_system : str | None = None
    price : int | None = None
    color : str | None = None

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
def mobile(p_type : user_phone, id : int):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    updated_data = p_type.model_dump(exclude_unset=True)

    for idx, item in enumerate(data):
        if item["id"] == id:
            data[idx].update(updated_data)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent = 4)

            return {
                "text" : "Phone info updated successfully",
                "data" : data[idx]
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

class watchlist(BaseModel):
    title : str
    genre : str
    rating : float
    views : float
    release_year : str

@app.post("/post_movies")
def movie_added(m : watchlist, db = Depends(get_db)):
    c_data_j = m.model_dump()
    sql_data = Movies(**c_data_j)

    db.add(sql_data)
    db.commit()
    db.refresh(sql_data)
    
    # Here you can add logic to save the movie_data to the database or perform any other operations
    return {
        "text" : "Movie info saved successfully",
        "data" : sql_data
    }

# This to retrieve single data from the database using id
@app.get("/retrieve_movies/{id}")
def movie_retrieve(id : int, db = Depends(get_db)):
    movie_data = db.query(Movies).filter(Movies.id == id).first()

    if movie_data:
        return {
            "text" : "Movie info retrieved successfully",
            "data" : movie_data
        }
    else:
        return {
            "text" : "Movie info not found"
        }

# This retrieve all the data from the database
@app.get("/get_movies")
def get_movies(db = Depends(get_db)):
    movies = db.query(Movies).all()
    return {
        "text" : "Movies retrieved successfully",
        "data" : movies
    }

# This update the entire/section data of a movie in the database using id
@app.put("/update_movies/{id}")
def movie_update(id : int, m : watchlist, db = Depends(get_db)):
    movie_data = db.query(Movies).filter(Movies.id == id).first()

    if movie_data:
        update_data = m.model_dump()
        for key, value in update_data.items():
            setattr(movie_data, key, value)

        db.commit()
        db.refresh(movie_data)

        return {
            "text" : "Movie info updated successfully",
            "data" : movie_data
        }
    else:
        return {
            "text" : "Movie info not found"
        }


class movie_checklist(BaseModel):
    title : str | None = None
    genre : str | None = None
    rating : float | None = None
    views : float | None = None
    release_year : str | None = None

# This update specific field of a movie in the database using id
@app.patch("/patch_movies/{id}")
def movie_repair(id : int, m : movie_checklist, db = Depends(get_db)):
    movie_data = db.query(Movies).filter(Movies.id == id).first()

    if movie_data:
        update_data = m.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(movie_data, key, value)

        db.commit()
        db.refresh(movie_data)

        return {
            "text" : "Movie info updated successfully",
            "data" : movie_data
        }
    else:
        return {
            "text" : "Movie info not found"
        }