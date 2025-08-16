import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy  # Database ORM
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)  # User authentication management
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------
# FLASK APP CONFIGURATION
# -------------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used for session encryption

# -------------------------
# DATABASE CONFIGURATION
# -------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # SQLite database file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # Initialize database connection

# -------------------------
# LOGIN MANAGER CONFIGURATION
# -------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect here if @login_required fails

# -------------------------
# USER MODEL
# -------------------------
class User(UserMixin, db.Model):
    """
    This table stores user accounts.
    UserMixin provides Flask-Login functionality like is_authenticated.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(150), unique=True, nullable=False)  # Must be unique
    email = db.Column(db.String(150), unique=True, nullable=False)  # Must be unique
    password_hash = db.Column(db.String(200), nullable=False)  # Stores hashed password

    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks a plain password against the stored hash."""
        return check_password_hash(self.password_hash, password)

# -------------------------
# USER LOADER
# -------------------------
@login_manager.user_loader
def load_user(user_id):
    """
    This function is called by Flask-Login to load a user by ID.
    """
    return User.query.get(int(user_id))

# -------------------------
# SIGN UP ROUTE
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if username or email is already taken
    if User.query.filter_by(username=username).first():
        flash("Username already exists!")
        return redirect(url_for("home"))
    if User.query.filter_by(email=email).first():
        flash("Email already exists!")
        return redirect(url_for("home"))

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Save to database
    db.session.add(new_user)
    db.session.commit()

    flash("Account created! Please log in.")
    return redirect(url_for("home"))

# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    # Check credentials
    if user and user.check_password(password):
        login_user(user)
        flash("Logged in successfully!")
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid username or password")
        return redirect(url_for("home"))

# -------------------------
# LOGOUT ROUTE
# -------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))

# -------------------------
# DASHBOARD (PROTECTED)
# -------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    # Shows a personalized greeting to the logged-in user
    return f"Welcome, {current_user.username}!"

# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    """
    Main page of the site — loads index.html.
    This should include the login/signup modals inside base.html.
    """
    return render_template("index.html")

# -------------------------
# PROJECTS PAGE
# -------------------------
@app.route("/projects")
def projects():
    """
    Dynamically loads all project images from static/images/projects.
    """
    project_folder = os.path.join(app.static_folder, 'images/projects')

    # Get only valid image files
    images = [
        filename for filename in os.listdir(project_folder)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
    ]
    return render_template('projects.html', project_images=images)

# -------------------------
# ABOUT PAGE
# -------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------
# FORUM PAGE
# -------------------------
@app.route("/forum")
def forum():
    return render_template("forum.html")

# -------------------------
# CONTACT PAGE
# -------------------------
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """
    Contact form page.
    Handles form submission and shows a thank-you message.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Here you could store in DB or send email
        flash('Thank you for reaching out!', 'success')
        return redirect('/contact')

    return render_template('contact.html')

# -------------------------
# MAIN APP ENTRY
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)  # Runs the app in debug mode
