from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/asd')
def hello_world_asd():
    return 'Hello World asd!'


if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')

