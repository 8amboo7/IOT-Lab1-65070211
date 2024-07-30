from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends, Response, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# นำเข้าโมเดล
from database import SessionLocal, engine
import models

load_dotenv()

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

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    try:
        return db.query(models.Book).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    try:
        newbook = models.Book(
            title=book['title'], 
            author=book['author'], 
            year=book['year'], 
            is_published=book['is_published'], 
            detail=book['detail'], 
            description=book['description']
        )
        db.add(newbook)
        db.commit()
        db.refresh(newbook)
        response.status_code = 201
        return newbook
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    try:
        update_book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not update_book:
            raise HTTPException(status_code=404, detail="Book not found")
        update_book.title = book['title']
        update_book.author = book['author']
        update_book.year = book['year']
        update_book.detail = book['detail']
        update_book.description = book['description']
        update_book.is_published = book['is_published']
        db.commit()
        db.refresh(update_book)
        Response.status_code = 200
        return update_book
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(book)
        db.commit()
        response.status_code = 204
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    try:
        return db.query(models.Student).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    try:
        newstudent = models.Student(
            name=student['name'], 
            lastname=student['lastname'], 
            dob=student['dob'], 
            sex=student['sex']
        )
        db.add(newstudent)
        db.commit()
        db.refresh(newstudent)
        response.status_code = 201
        return newstudent
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
    try:
        update_student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if not update_student:
            raise HTTPException(status_code=404, detail="Student not found")
        update_student.name = student['name']
        update_student.lastname = student['lastname']
        update_student.dob = student['dob']
        update_student.sex = student['sex']
        db.commit()
        db.refresh(update_student)
        Response.status_code = 200
        return update_student
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student)
        db.commit()
        response.status_code = 204
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
