from flask import Blueprint, render_template, session, request, redirect, url_for
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
    db.execute("SELECT * FROM profile WHERE user_id=?", (session["id"],))
    user_profile = db.fetchone()
    if request.method == "POST":
        if request.form.get("button") == "edit":
            print(request.form.get("button"))
            return render_template("edit.html", user_profile=user_profile)
        elif request.form.get("button") == "deleteposts":
            print(request.form.get("button"))
            db.execute("DELETE FROM posts WHERE user_id=?", (session["id"],))
            conn.commit()
            return redirect(url_for("profile.home"))
        elif request.form.get("button") == "deleteprofile":
            print(request.form.get("button"))
            db.execute("DELETE FROM user WHERE id=?", (session["id"],))
            db.execute("DELETE FROM profile WHERE user_id=?", (session["id"],))
            conn.commit()
            return redirect(url_for("logout")) 
        else:
            flash("Unsuccessful")
    return render_template("profile.html", user_profile=user_profile)