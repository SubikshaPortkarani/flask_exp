from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "feedback.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_feedback_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        year TEXT,
        college TEXT,
        dob TEXT,
        gender TEXT,
        email_id TEXT UNIQUE,
        address TEXT,
        rating INTEGER,
        remark TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_college_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS college(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_id TEXT UNIQUE,
        college_name TEXT,
        city TEXT,
        email_id TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()


create_feedback_table()
create_college_table()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def check_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid Username or Password"
    )


@app.route("/dashboard")
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM feedback")
    total = cur.fetchone()[0]

    ratings = {}

    for i in range(1, 6):
        cur.execute(
            "SELECT COUNT(*) FROM feedback WHERE rating=?",
            (i,)
        )
        ratings[i] = cur.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        one=ratings[1],
        two=ratings[2],
        three=ratings[3],
        four=ratings[4],
        five=ratings[5]
    )
      cur.execute("SELECT COUNT(*) FROM college")
    total_colleges = cur.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total=total_feedback,
        colleges=total_colleges
    )

@app.route("/logout")
def logout():
    return redirect(url_for("login"))


@app.route("/feedback", methods=["GET","POST"])
def feedback():

    if request.method=="POST":

        conn=get_db()
        cur=conn.cursor()

        cur.execute("""
        INSERT INTO feedback
        (student_name,year,college,dob,gender,email_id,address,rating,remark)
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(
            request.form["student_name"],
            request.form["year"],
            request.form["college"],
            request.form["dob"],
            request.form["gender"],
            request.form["email_id"],
            request.form["address"],
            request.form["rating"],
            request.form["remark"]
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("view_feedback"))

    return render_template("feedback.html")

@app.route("/view_feedback")
def view_feedback():

    conn=get_db()
    conn.row_factory=sqlite3.Row

    cur=conn.cursor()

    cur.execute("SELECT * FROM feedback")

    data=cur.fetchall()

    conn.close()

    return render_template(
        "view_feedback.html",
        data=data
    )
@app.route("/api/create", methods=["POST"])
def api_create():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    try:

        cur.execute("""
        INSERT INTO feedback
        (
            student_name,
            year,
            college,
            dob,
            gender,
            email_id,
            address,
            rating,
            remark
        )
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            data["student_name"],
            data["year"],
            data["college"],
            data["dob"],
            data["gender"],
            data["email_id"],
            data["address"],
            data["rating"],
            data["remark"]
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Feedback Added Successfully"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

    finally:
        conn.close()


@app.route("/api/select", methods=["GET"])
def api_select():

    email = request.args.get("email_id")

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM feedback WHERE email_id=?",
        (email,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return jsonify(dict(row))

    return jsonify({
        "message": "Record Not Found"
    })


@app.route("/api/update", methods=["POST"])
def api_update():

    data = request.get_json()

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
    UPDATE feedback
    SET
        student_name=?,
        year=?,
        college=?,
        dob=?,
        gender=?,
        email_id=?,
        address=?,
        rating=?,
        remark=?
    WHERE id=?
    """,
    (
        data["student_name"],
        data["year"],
        data["college"],
        data["dob"],
        data["gender"],
        data["email_id"],
        data["address"],
        data["rating"],
        data["remark"],
        data["id"]
    ))

    conn.commit()

    if cur.rowcount == 0:

        conn.close()

        return jsonify({
            "message": "Record Not Found"
        })

    conn.close()

    return jsonify({
        "message": "Feedback Updated Successfully"
    })



@app.route("/api/delete", methods=["POST"])
def api_delete():

    data = request.get_json()

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM feedback WHERE id=?",
        (data["id"],)
    )

    conn.commit()

    if cur.rowcount == 0:

        conn.close()

        return jsonify({
            "message": "Record Not Found"
        })

    conn.close()

    return jsonify({
        "message": "Feedback Deleted Successfully"
    })

@app.route("/collegeform",methods=["GET","POST"])
def collegeform():

    if request.method=="POST":

        conn=get_db()
        cur=conn.cursor()

        cur.execute("""
        INSERT INTO college
        (college_id,college_name,city,email_id,phone)
        VALUES(?,?,?,?,?)
        """,(
            request.form["college_id"],
            request.form["college_name"],
            request.form["city"],
            request.form["email_id"],
            request.form["phone"]
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("collegeview"))

    return render_template("collegeform.html")

@app.route("/collegeview")
def collegeview():

    conn=get_db()

    conn.row_factory=sqlite3.Row

    cur=conn.cursor()

    cur.execute("SELECT * FROM college")

    colleges=cur.fetchall()

    conn.close()

    return render_template(
        "collegeview.html",
        colleges=colleges
    )


@app.route("/college/create", methods=["POST"])
def create_college():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    try:

        cur.execute("""
        INSERT INTO college
        (
            college_id,
            college_name,
            city,
            email_id,
            phone
        )
        VALUES (?,?,?,?,?)
        """,
        (
            data["college_id"],
            data["college_name"],
            data["city"],
            data["email_id"],
            data["phone"]
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "College Added Successfully"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

    finally:
        conn.close()


@app.route("/college/select", methods=["GET"])
def select_college():

    college_id = request.args.get("college_id")

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM college WHERE college_id=?",
        (college_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return jsonify(dict(row))

    return jsonify({
        "message": "College Not Found"
    })


@app.route("/college/update", methods=["POST"])
def update_college():

    data = request.get_json()

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
    UPDATE college
    SET
        college_name=?,
        city=?,
        email_id=?,
        phone=?
    WHERE college_id=?
    """,
    (
        data["college_name"],
        data["city"],
        data["email_id"],
        data["phone"],
        data["college_id"]
    ))

    conn.commit()

    if cur.rowcount == 0:

        conn.close()

        return jsonify({
            "message": "College Not Found"
        })

    conn.close()

    return jsonify({
        "message": "College Updated Successfully"
    })

@app.route("/college/delete", methods=["POST"])
def delete_college():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM college WHERE college_id=?",
        (data["college_id"],)
    )

    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        return jsonify({"message": "College Not Found"})

    conn.close()

    return jsonify({"message": "College Deleted Successfully"})
  
if __name__ == "__main__":

 
    app.run(
        debug=True,)

