from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    test = 'sadfa'
    return '<h1>Your browser is %s %s</h1>' % (user_agent, test)


if __name__  == '__main__':
    app.run(debug=True)
