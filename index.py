from sys import path
from os import getcwd, system

path.append(f"{getcwd()}/site-packages")
#System removes/resets the installed pip packages every time you login to the computer again, so i installed them to a folder where i can just import them from instead.

system("")
#Enable ANSI/colour in terminal

from Utils.database import database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import *
from random import randint
from datetime import date, datetime
import uvicorn

app = FastAPI()
app.database = database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index(request:Request):
    return FileResponse(f"{request.app.database.cwd}/frontend/index.html")

@app.get("/resource/{resource}")
async def index(request:Request, resource:str):
    return FileResponse(f"{request.app.database.cwd}/frontend/{resource}")

@app.post("/api/login/")
async def login(request:Request):
    return {"success": request.headers.get("Authentication") == request.app.database.password}

@app.post("/api/student/create/")
async def create(request:Request):
    payload = await request.json()

    payload["id"] = randint(111111,999999)

    payload["email"] = f"{payload['id']}@treeschool.com"

    group = payload["group"]
    del payload["group"]

    if group not in request.app.database.data.keys():
        request.app.database.data[group] = [
                payload
            ]
    else:
        request.app.database.data[group].append(payload)
        

    request.app.database.write()

    return {"id": payload["id"]}

@app.get("/api/student/view/")
async def view(request:Request, student:str):
    target = int(student)

    for group in request.app.database.data.keys():
        for student in request.app.database.data[group]:
            if student["id"] == target:
                student["group"] = group
                return student

    raise HTTPException(404, "Student not found")

@app.post("/api/student/delete/")
async def view(request:Request, student:str):
    target = int(student)

    finished = False

    for group in request.app.database.data.keys():
        for student in request.app.database.data[group]:
            if student["id"] == target:
                request.app.database.data[group].remove(student)
                finished = True
                break
        if finished:
            break

    request.app.database.write()

@app.get("/api/student/all/")
async def view(request:Request):
    students = []

    for group in request.app.database.data.keys():
        for student in request.app.database.data[group]:
            student["group"] = group
            students.append(student)

    return {"students":students}

@app.get("/api/reports/{report}")
async def gen_report(request:Request, report:str):
    report = report.lower()

    if report == "age":
        ages = {}
        total = 0
        
        for group in request.app.database.data.keys():
            for student in request.app.database.data[group]:
                age = student["dob"].split("-")
                age = date(int(age[0]), int(age[1]), int(age[2]))
                difference = datetime.now().date() - age
                difference_in_years = int((difference.days + difference.seconds/86400)/365.2425)
                if difference_in_years not in ages.keys():
                    ages[difference_in_years] = 0
                ages[difference_in_years] += 1
                total += 1

        report = []

        for age in ages.keys():
            report.append({"text": f"Age {age}", "ratio": round((ages[age]/total)*100,2), "amount": ages[age]})
                
        return {"report": report}
        
    elif report == "gender":
        genders = {}
        total = 0
        
        for group in request.app.database.data.keys():
            for student in request.app.database.data[group]:
                if student["gender"].lower() not in genders.keys():
                    genders[student["gender"].lower()] = 0
                genders[student["gender"].lower()] += 1
                total += 1

        report = []

        for gender in genders.keys():
            report.append({"text": gender[0].upper()+gender[1:], "ratio": round((genders[gender]/total)*100,2), "amount": genders[gender]})
                
        return {"report": report}
    
    elif report == "tutor":
        groups = {}
        total = 0
        
        for group in request.app.database.data.keys():
            groups[group] = len(request.app.database.data[group])
            total += 1

        report = []

        for group in groups.keys():
            report.append({"text": group, "ratio": round((groups[group]/total)*100,2), "amount": groups[group]})
                
        return {"report": report}
        
if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=80)
    #available from         http://127.0.0.1:8923/
    
