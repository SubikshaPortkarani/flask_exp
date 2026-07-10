from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER ,
        student_name TEXT,
        year TEXT,
        college TEXT,
        dob TEXT,
        gender TEXT,
        address TEXT,
        rating INTEGER,
        remark TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM feedback")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating=5")
    five = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating=4")
    four = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating=3")
    three = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating=2")
    two = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating=1")
    one = cur.fetchone()[0]

    cur.execute("""
        SELECT id,
               student_name,
               year,
               college,
               rating,
               remark
        FROM feedback
    """)

    data = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        five=five,
        four=four,
        three=three,
        two=two,
        one=one,
        data=data
    )
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        student = request.form["student"]
        year = request.form["year"]
        college = request.form["college"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        address = request.form["address"]
        rating = request.form["rating"]
        remark = request.form["remark"]

        conn = sqlite3.connect("feedback.db")
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO feedback 
            (student_name, year, college, dob, gender, address, rating, remark) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student, year, college, dob, gender, address, rating, remark))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for("dashboard"))

    return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)

