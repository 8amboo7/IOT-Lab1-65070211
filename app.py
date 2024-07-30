from dotenv import load_dotenv
load_dotenv()

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
#---------------------------------Book---------------------------------

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], detail=book['detail'], story=book['story'], classification=book['classification'])
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
    update_book.detail = book['detail']
    update_book.story = book['story']
    update_book.classification = book['classification']
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



#---------------------------------Menu---------------------------------
@router_v1.get('/menus')
async def get_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.get('/menus/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

@router_v1.post('/menus')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    newmenu = models.Menu(name=menu['name'], price=menu['price'], is_published=menu['is_published'], detail=menu['detail'], ingredient=menu['ingredient'])
    db.add(newmenu)
    db.commit()
    db.refresh(newmenu)
    response.status_code = 201
    return newmenu

@router_v1.patch('/menus/{menu_id}')
async def update_menu(menu_id: int, menu: dict, db: Session = Depends(get_db)):
    update_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    update_menu.name = menu['name']
    update_menu.price = menu['price']
    update_menu.is_published = menu['is_published']
    update_menu.detail = menu['detail']
    update_menu.ingredient = menu['ingredient']
    db.commit()
    db.refresh(update_menu)
    Response.status_code = 200
    return update_menu

@router_v1.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, response: Response, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(menu)
    db.commit()
    response.status_code = 204
    return

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    neworder = models.Order(name=order['name'], price=order['price'], total=order['total'], note=order['note'])
    db.add(neworder)
    db.commit()
    db.refresh(neworder)
    response.status_code = 201
    return neworder

#---------------------------------Staff----------------------------------
@router_v1.get('/staffs')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/staffs/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.delete('/staffs/{order_id}')
async def delete_order(order_id: int, response: Response, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db.delete(order)
    db.commit()
    response.status_code = 204
    return

#---------------------------------Student--------------------------------
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