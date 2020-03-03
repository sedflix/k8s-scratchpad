from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hi, I'm " + str(os.uname()[1])

if __name__ == "__main__":
    app.run(host='0.0.0.0')