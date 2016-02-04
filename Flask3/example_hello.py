#!/usr/bin/env python
from flask import Flask # import flask
app = Flask(__name__) # just variable

@app.route('/') # root URI connect hello_world()
def hello_world():
    return '<strong>Hello World!</strong>'

if __name__ == '__main__': # is this file main?
    app.run(host='0', debug=True)		   # run WAS
