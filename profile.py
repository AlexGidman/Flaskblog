from flask import Blueprint, render_template, session, request, redirect, url_for
from decorators import login_required
from contextmanagers import SQL
import sqlite3
import requests

### SQLite3 
conn = sqlite3.connect("site.db", check_same_thread=False,)
db = conn.cursor()

profile = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

BASE = "http://worldtimeapi.org/api/timezone/"
response = requests.get(BASE)
locations = response.json()

@profile.route("/home")
@profile.route("/", methods=["GET", "POST"])
@login_required
def home():
    db.execute("SELECT * FROM profile WHERE user_id=?", (session["id"],))
    user_profile = db.fetchone()
    if request.method == "POST":
        if request.form.get("button") == "edit":
            print(request.form.get("button"))
            return render_template("edit.html", 
                                    user_profile=user_profile,
                                    locations=locations)
        elif request.form.get("button") == "save":
            print(request.form.get("button"))
            user_id = request.form.get("id")
            first = request.form.get("first")
            last = request.form.get("last")
            profession = request.form.get("profession")
            interests = request.form.get("interests")
            location = request.form.get("location")
            if not user_profile:
                db.execute("INSERT INTO profile (user_id, first, last, profession, interests,location) VALUES (?,?,?,?,?,?)",(user_id, first, last, profession, interests,location))
                conn.commit()
            else:
                db.execute("UPDATE profile SET first=?, last=?, profession=?, interests=?,location=? WHERE user_id=?",(first, last, profession, interests,location, user_id))
                conn.commit()
            return redirect(url_for('profile.home'))    
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
    # Get time based on location
    time = ""
    if (user_profile):
        BASE = "http://worldtimeapi.org/api/timezone/"
        response = requests.get(BASE + user_profile[6])
        time = response.json()['datetime']
    return render_template("profile.html", 
                            user_profile=user_profile,
                            time=time[11:19])
