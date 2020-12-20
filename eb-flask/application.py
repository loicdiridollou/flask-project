from flask import Flask

application = Flask(__name__)

@application.route('/')
def hello():
    return 'Hello world!'


@application.route('/cars')
def cars():
    return {'number': 5}



if __name__ == '__main__':
    application.run(debug=True, port=5000)