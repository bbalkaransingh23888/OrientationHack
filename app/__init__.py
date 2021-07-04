import os
from flask import Flask, render_template, request
#Response, send_from_directory, redirect
#from dotenv import load_dotenv
#from . import db
from werkzeug.security import generate_password_hash, check_password_hash
#from app.db import get_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
   return render_template('aboutPage.html', title="John Smith", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('aboutPage.html', title="John Smith", url=os.getenv("URL"))

@app.route('/blog')
def blog():
    return render_template('blogPage.html', title="John Smith", url=os.getenv("URL"))

@app.route('/projects')
def projects():
    return render_template('projectsPage.html', title="John Smith", url=os.getenv("URL"))

@app.route('/health')
def healthy():
    return render_template('base.html'), 201
    app_status = flask.Response(status=201)
    return app_status


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200 
        else:
            return error, 418
    
    ## TODO: Return a login page
    #return "Login page not yet implemented", 501
    return render_template('login.html', title="John Smith", url=os.getenv("URL")), 200


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    ## TODO: Return a restister page
    # return "Register Page not yet implemented", 501
    return render_template('register.html', title="John Smith", url=os.getenv("URL")), 200

