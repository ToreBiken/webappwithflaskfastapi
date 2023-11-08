from sqlalchemy.orm import Session
from .models import User, db, Work

def add_user(user:User)->None:
    db.session.add(user)
    db.session.commit()
    
def delete_user(user:User)->None:
    db.session.delete(user)
    db.session.commit()
    
def add_work(work:Work)->None:
    db.session.add(work)
    db.session.commit()
    
def get_all_users()->db.Query:
    return User.query.all()