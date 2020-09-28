from flask import Flask, render_template, url_for, redirect, flash, request
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
conn = sqlite3.connect("site.db", check_same_thread=False,)
db = conn.cursor()
#CREATE TABLES...

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
        pwhash = generate_password_hash(password)
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, pwhash))
        conn.commit()
        
        # Log user in and redirect to homepage
        # Session Id...
        return redirect(url_for("home"))
    else: 
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    #(check_password_hash(pwdhash, password)
    return render_template("login.html")