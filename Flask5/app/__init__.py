from flask import Flask

appsym = Flask(__name__)
appsym.config.from_object('config')

from app import views
