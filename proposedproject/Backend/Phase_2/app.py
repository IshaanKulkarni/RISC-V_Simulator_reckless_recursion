from flask import Flask, render_template, request
from flask_cors import CORS
from pipeline1 import controller

app = Flask(__name__)
CORS(app)


@app.route("/", methods = ['POST', 'GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/postcode", methods = ['POST'])
def uploader():
    if request.method == 'POST':
        code = request.form["code"]
        f = open("test1.asm", 'w')
        f.write(code)
        f.close()
        controller()
        return "done"

    return "done"





if __name__ == "__main__":
    app.run(debug= True)