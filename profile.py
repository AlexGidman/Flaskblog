from flask import Blueprint, render_template, session, request
from decorators import login_required
from contextmanagers import SQL
import sqlite3

### SQLite3 
conn = sqlite3.connect("site.db", check_same_thread=False,)
db = conn.cursor()

profile = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

@profile.route("/home")
@profile.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        print(request.form.get("button"))
    db.execute("SELECT * FROM profile WHERE user_id=?", (session["id"],))
    user_profile = db.fetchone()
    return render_template("profile.html", user_profile=user_profile)