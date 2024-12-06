from flask import Flask

app = Flask(__yuki__)

@app.route('/')

def hello_world():

return 'Yuki2.0 Bot running on Flask'

if __yuki__ == "__main__":

app.run()