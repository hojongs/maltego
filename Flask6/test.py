#!/usr/bin/env python
from flask import Flask
appsym = Flask(__name__)
  
@appsym.route('/')
def hello_world():
    return 'Hello World!'
if __name__ == '__main__':
    appsym.run(host='0.0.0.0')
