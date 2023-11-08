

from sqlalchemy.orm import Session
import models, schemas

def get_user_by_login(db: Session, user_login: str)->Session.query:
    return db.query(models.User).filter(models.User.login == user_login).first()

def get_user_by_email(db:Session, user_email: str)-> Session.query:
    return db.query(models.User).filter(models.User.email == user_email).all()

def get_all_users(db: Session, skip: int = 0, limit: int = 100)-> Session.query:
    return db.query(models.User).offset(skip).limit(limit).all()

def get_work_by_id(db: Session, work_id: int)->Session.query:
    return db.query(models.Work).filter(models.Work.work_id == work_id).first()

def get_user_works(db:Session,user_id: int)->Session.query:
    return db.query(models.Work).filter(models.Work.work_owner == user_id).all()

def get_all_works(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.Work).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate)->models.User:
    new_user = models.User(login=user.login,
                           email=user.email,
                           password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_work(db: Session, work: schemas.WorkCreate)->models.Work:
    new_work = models.Work(work_title = work.work_title,
                         work_description = work.work_description,
                         work_owner = work.work_owner)
    db.add(new_work)
    db.commit()
    db.refresh(new_work)
    return new_work
