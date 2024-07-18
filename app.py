from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    student_id: str
    birthdate: str
    gender: str

class StudentUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    student_id: str = None
    birthdate: str = None
    gender: str = None

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router_v1.post('/students')
async def create_student(student: StudentCreate, response: Response, db: Session = Depends(get_db)):
    new_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        student_id=student.student_id,
        birthdate=student.birthdate,
        gender=student.gender
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    response.status_code = 201
    return new_student

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student.dict(exclude_unset=True).items():
        setattr(existing_student, key, value)
    
    db.commit()
    db.refresh(existing_student)
    return existing_student

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(existing_student)
    db.commit()
    return Response(status_code=204)

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
#bam