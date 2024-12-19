from api import *
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


if __name__=='__main__':
    app.secret_key='secret'
    app.run()


