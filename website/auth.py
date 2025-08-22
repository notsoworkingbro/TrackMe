from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p> Login </p>"

@auth.route('/logout')
def logout():
    return render_template("login.html", show_navbar=False)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Just simple validation (you can expand later)
        if password != confirm:
            flash('Passwords do not match!', category='error')
        else:
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', show_navbar=False)