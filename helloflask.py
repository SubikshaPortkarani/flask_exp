from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/inputpage")
def inputpage():
    return render_template("inputpage.html")


@app.route("/statuspage")
def statuspage():
    inputvalue = request.args.get("textinput")
    return render_template("statuspage.html", inputvalue=inputvalue)


if __name__ == "__main__":
    app.run(debug=True)