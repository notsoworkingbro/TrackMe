from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from .models import User 
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email')  # could be email OR username
        password = request.form.get('password')

        user = User.query.filter(or_(User.email == identifier, User.username == identifier)).first()

        if user:
            if check_password_hash(user.password, password):

                login_user(user, remember=True)

                flash('logged in succesful', category='success')
                print(f'Succes')

                return redirect(url_for('views.home'))  # ✅ go to home route
            else:
                flash('Incorrect Password , try again', category='error')

        else:
            flash('user does not exist')


    return render_template("login.html", show_navbar=False)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Just simple validation (you can expand later)

        user = User.query.filter_by(email=email).first()
        if  user:

            login_user(user, remember=True)

            flash('Email already exist', category='error')
            return redirect(url_for('views.home'))

        elif password != confirm:
            flash('Passwords do not match!', category='error')

        else:
            flash('Account created successfully!', category='success')

            # Create new user
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully!', category='success')

            return redirect(url_for('views.home'))

    return render_template('sign_up.html', show_navbar=False)