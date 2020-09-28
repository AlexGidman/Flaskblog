from flask import Flask, render_template, url_for, redirect, flash, request

app = Flask(__name__)

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
            
        # If registration success, log user in and redirect to homepage
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")