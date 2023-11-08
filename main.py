from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Замените это на домен и порт вашего Flask-приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/users/create/", response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_login(db, user_login=user.login)
    
    if new_user:
        raise HTTPException(status_code=400, detail="Login is already taken by another user.")
    return crud.create_user(db=db, user=user)

@app.post("/works/create/", response_model=schemas.Work)
def create_work(work: schemas.WorkCreate, db: Session=Depends(get_db)):
    return crud.create_work(db, work=work)

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users

@app.get("/users/{login}", response_model=schemas.User)
def get_certain_user(login, db: Session = Depends(get_db)):
    return crud.get_user_by_login(db, login)

@app.get("/works/", response_model=list[schemas.Work])
def get_all_works(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_works(db)

@app.get("/user/works/{user_id}", response_model=list[schemas.Work])
def get_user_works(user_id, db: Session = Depends(get_db)):
    return crud.get_user_works(db, user_id)

@app.get("/work/{work_id}/", response_model=schemas.Work)
def get_work(work_id:int, db: Session = Depends(get_db)):
    return crud.get_work_by_id(db, work_id)