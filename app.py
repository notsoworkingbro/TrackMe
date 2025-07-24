import os
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/projects')
def projects():
    project_folder = os.path.join(app.static_folder, 'images/projects')
    images = [
        filename for filename in os.listdir(project_folder)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
    ]
    return render_template('projects.html', project_images=images)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/forum')
def forum():
    return render_template("forum.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # You can handle the data here (save to file, send email, etc.)
        flash('Thank you for reaching out!', 'success')
        return redirect('/contact')

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
    