from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Yuki2.0 running'


if __name__ == "__main__":
    app.run()