from app_flask import *
from flask import render_template
from flask import request, session, redirect, url_for
from werkzeug.utils import secure_filename
import requests

# from ..models import User, db, Work
# from .. import crud
# from ..models import User, Work
# from app_flask import db

from database.models import User, Work
from database.crud import add_user, add_work

# from .. import crud
# import importlib.util
# import os
# module_path = 'D:\\projects\\fastapi_crud\\crud.py'
# module_name = os.path.splitext(os.path.basename(module_path))[0]
# spec = importlib.util.spec_from_file_location(module_name, module_path)
# module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)
# from module import create_user

# import os
# import sys
# module_directory = 'D:\\projects\\fastapi_crud'
# sys.path.append(module_directory)
# from crud import create_user

@app.route('/home')
@app.route("/")
def home():
    is_authenticated = session.get('authenticated', False)
    return render_template("index.html", is_authenticated=is_authenticated)

@app.route("/register", methods=["GET", "POST"])
def register(context=None):
    if session.get('authenticated'):
        return redirect(url_for('home'))
    
    # if request.method == "POST":
    #     login = request.form['login']
    #     email = request.form['email']
    #     pass1 = request.form['password']
    #     pass2 = request.form['password_conf']
        
    #     data = db.session.query(User).filter_by(login=request.form['login']).first()
    #     if data:
    #         return redirect(url_for("register", error="Login exists"))
    #     elif pass1 != pass2:
    #         return redirect(url_for("register", error="password does not match"))
    #     else:
    #         add_user(User(login=login,
    #                       email=email,
    #                       password=pass2))
            
    #         return redirect(url_for("login", context="Succesfully registered!"))
    if request.method == "POST":
        data = {
            'login': request.form['login'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        response = requests.post('http://localhost:8000/users/create/', json=data)
        if response:
            return redirect(url_for('login'))
        else:
            return f'User creation failed: {response.text}'
    return render_template("register.html", context=context)
    
    # if request.method == "POST":
    #     login = request.form['login']
    #     email = request.form['email']
    #     pass1 = request.form['password']
    #     pass2 = request.form['password_conf']
    #     data = db.session.query(User).filter_by(login=request.form['login']).first()
    #     add_user(User(login=login,
    #                      email=email,
    #                      password=pass1))
    #     return redirect(url_for('home'), contect="nice")
    # return render_template("register.html", context=context)
        

@app.route("/login", methods=["GET", "POST"])
def login(context=None):
    if session.get('authenticated'):
        return redirect(url_for('home'))
    
    if request.method == "POST":
        user = db.session.query(User).filter_by(login=request.form['login'], password=request.form['password']).first()
        if user:
            session['authenticated'] = True
            session['uid'] = user.user_id
            session['login'] = user.login
            return redirect(url_for("home"))
        else:
            return render_template("login.html", context="try again, something went wrong")
    return render_template("login.html", context=context)

@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('login', None)
    return redirect(url_for('home'))

@app.route('/upload', methods=["GET", "POST"])
def upload(context=None):
    if not session.get('authenticated'):
        return render_template("warning.html")
    
    user = db.session.query(User).get(session['uid'])
    if request.method == "POST":
        work_title = request.form['work_title']
        work_description = request.form['work_description']
        work_owner = session['uid']
        # data = db.session.query(Work).filter_by(work_title=work_title, work_description=work_description)
        data = {
            'work_title': work_title,
            'work_description': work_description,
            'work_owner': work_owner
        }
        response = requests.post('http://localhost:8000/works/create/', json=data)
        if response:
            return redirect(url_for('works'))
        else:
            return f'Work creation failed: {response.text}'
        # add_work(Work(work_title=work_title,
        #               work_description=work_description,
        #               work_owner=work_owner))
        # return redirect(url_for('works', context="Succesfully added"))
        
    return render_template('upload.html', context=context, user=user)
        
@app.route('/works')
def works():
    # if session.get('authenticated'):
    response = requests.get('http://localhost:8000/works/')
    if response:
        data = response.json()
        # user = session['login']
        return render_template("works.html", data=data)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)