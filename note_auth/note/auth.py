from flask import Blueprint, render_template, request, redirect, url_for, flash   # flash for sending messages 
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST", "GET"])
def login():

    if request.method == "POST":
        # data = request.form returns immutableMultiDict([('email','laouali@gmail'), ('password','1234')])
        email = request.form.get("email")
        password = request.form.get("password")

        # to filter through User table for the user email
        user_log = User.query.filter_by(email=email).first()

        if user_log:
            # checking if the password is the same
            if check_password_hash(user_log.password, password):
                flash('Logged in successfully', category='success')
                
                # act like a session
                login_user(user_log, remember=True)

                # redirect to home
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exit.', category='error')
        
    users = User.query.all()
    notes = Note.query.all()
    print(users)
    print(notes)
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required  # must always have a login_required so that mean the user can't access this page without being login
def logout():
    # this is enough to logout the user and clean the session
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',  methods=["POST", "GET"])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            # the flash function takes a message and a category which can be error, success, info if using boostrap or anything else
            # they do not need return
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # creating a a new user
            # hashing method = generate_password_hash(password1, method='sha256')
            hash_password = generate_password_hash(password1, method='pbkdf2')
            new_user = User(email=email, password=hash_password, firstName=firstName)

            db.session.add(new_user)
            db.session.commit()

            # act like a session but not advice in the sign up
            login_user(user, remember=True)

            flash('Account created', category='success')

            return redirect(url_for('views.home'))
        
       

    return render_template('sign_up.html', user=current_user)