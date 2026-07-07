from flask import Flask, render_template, request

app = Flask(__name__)

#@app.route('/inputpage')
def input_page():
    return render_template('inputpage.html')


@app.route("/statuspage", methods=['GET'])
def status_page():
    # Extracts the text entered from the "textinput" field in the form
    status = request.args.get("textinput")
    return render_template('statuspage.html', status = status)


if __name__ == '__main__':
    app.run(debug=True)