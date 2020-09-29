from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash 
from functools import wraps
import sqlite3

# DECORATORS 
def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

 # CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
conn = sqlite3.connect("site.db", check_same_thread=False,)
db = conn.cursor()

# ROUTES

## HOME
@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("index.html")

## ABOUT
@app.route("/about")
@login_required
def about():
    return render_template("about.html")

## REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Error Check
        check = db.execute("SELECT username FROM user WHERE username = ?;", [username])
        if (check.fetchall()):
            flash("Username already exists!")
            return render_template("register.html")
        if (len(password) < 10):
            flash("Password must be 10 characters or more!")
            return render_template("register.html")
        
        # Store into database 
        pwhash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, pwhash))
        conn.commit()

        # Log user in and redirect to homepage
        db.execute("SELECT id FROM user WHERE username=?", [username])
        session["id"] = db.fetchone()[0]
        return redirect(url_for("home"))
    else: 
        return render_template("register.html")

## LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide a username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide a password")
            return render_template("login.html")
        
        username = request.form.get("username")
        db.execute("SELECT * FROM user WHERE username=?", [username])
        user = db.fetchone()

        if not user:
            flash("Invalid username or password")
            return render_template("login.html")
        
        if not check_password_hash(user[2], request.form.get("password")):
            flash("Invalid username or password")
            return render_template("login.html")

        session["id"] = user[0]
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


## LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))