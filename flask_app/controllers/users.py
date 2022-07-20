from flask import render_template, request, redirect, session, flash 
from flask_app import app,bcrypt 

from flask_app.models.user import User

# Create 1 to display form 

@app.route('/')
@app.route('/users')
def index():
    return render_template('index.html' )

# one for post after the form has been filled out will take me to /dashboard
@app.route('/users/register', methods= ['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # dictionary changes password value to the hash created above
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['first_name'],
        "email": request.form['email'],
        "password":pw_hash
    }
# Save to database
# User.save(data) will return my user id
    user_id = User.save(data)

    # to log in 
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    # if my static method (validate) inside my user class method (save) is NOT true then redirect them to my home page ELSE redirect them to my dashboard
    return redirect('/dashboard')

@app.route('/users/login' ,methods = ["post"])
def login():
    print(request.form)
    user = User.get_one_by_email(request.form)
    print(user)
    return render_template('/dashboard')