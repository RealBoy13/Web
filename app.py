import os
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, abort
from werkzeug.utils import secure_filename
import logging

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Logging setup
logging.basicConfig(level=logging.INFO)

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route redirects to the welcome page
@app.route('/')
def index():
    app.logger.info('Index route accessed.')
    return render_template('index.html')

# Welcome page that shows basic information and session data
@app.route('/welcome')
def welcome():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('welcome.html', visits=session['visits'])

# Dynamic route to greet users by name
@app.route('/user/<username>')
def greet_user(username):
    app.logger.info(f'Greeted user: {username}')
    return render_template('user.html', username=username)

# Form route to handle user input
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash('Username is required!', 'error')
            return redirect(url_for('form'))
        return render_template('user.html', username=username)
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'File successfully uploaded: {filename}')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')

# Return a JSON response for an API-like endpoint
@app.route('/api/visits', methods=['GET'])
def api_visits():
    visits = session.get('visits', 0)
    return jsonify({'visits': visits})

# Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning('404 error occurred.')
    return "<h1>404 - Page not found</h1>", 404

# Run the Flask app
if __name__ == '__app__':
    app.run(host='0.0.0.0', port=81)
