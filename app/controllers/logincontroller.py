from flask import render_template,redirect,url_for,request,flash
from flask_login import login_user,logout_user
from app import app,db
from app.models.tables import User

@app.route("/login", methods =['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        pwd = request.form['password']
        
        userExist = User.query.filter_by(username=user).first()
        if not userExist or not userExist.verify_password(pwd):
            flash('Incorrect username or password', 'error')
            return redirect(url_for('login'))
        
        login_user(userExist)  
        return redirect(url_for('index'))
    
    return render_template('Login.html')


@app.route("/register", methods =['GET','POST'])
def register ():
    if request.method == 'POST':
        name = request.form['name']
        user = request.form['user']
        pwd = request.form['password']

        usercad = User(user,pwd,name)
        db.session.add(usercad)
        db.session.commit()
    
    return render_template('register.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))