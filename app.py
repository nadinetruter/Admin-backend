from flask import Flask, request, Response
from database.db import initialize_db
import json
from flask_restful import Api

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from resources.errors import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
mail = Mail(app)
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


app.config['MONGODB_SETTINGS'] = { 'host': 'mongodb+srv://nadine:123@cluster0.xznck.mongodb.net/testadmin2?retryWrites=true&w=majority'}


initialize_db(app)
initialize_routes(api)
