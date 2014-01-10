__author__ = 'Roman Arkharov'

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'HaWaii!!!<img src="/blocks.png">'

if __name__ == '__main__':
    app.run()
