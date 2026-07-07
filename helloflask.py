from flask import Flask, render_template

app = Flask(__name__)

@app.route('/pageone')
def first_page():
    return render_template('firstpage.html')

@app.route('/pagetwo')
def second_page():
    return render_template('secondpage.html')

if __name__ == '__main__':
    app.run(debug=True)