from dotenv import load_dotenv
load_dotenv()
import os

my_variable = os.getenv('MY_VARIABLE')
print(my_variable)


from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')
router_v2 = APIRouter(prefix='/api/v2')


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

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    update_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    update_book.title = book['title']
    update_book.author = book['author']
    update_book.year = book['year']
    update_book.is_published = book['is_published']
    db.commit()
    db.refresh(update_book)
    Response.status_code = 200
    return update_book

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(book)
    db.commit()
    response.status_code = 204
    return



# @router_v1.patch('/books/{book_id}')
# async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
#     pass

# @router_v1.delete('/books/{book_id}')
# async def delete_book(book_id: int, db: Session = Depends(get_db)):
#     pass

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newstudent = models.Student(name=student['name'], lastname=student['lastname'], dob=student['dob'], sex=student['sex'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
    update_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    update_student.name = student['name']
    update_student.lastname = student['lastname']
    update_student.dob = student['dob']
    update_student.sex = student['sex']
    db.commit()
    db.refresh(update_student)
    Response.status_code = 200
    return update_student

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, response: Response, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    db.delete(student)
    db.commit()
    response.status_code = 204
    return

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)