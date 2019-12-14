from flask import Flask

# App
app = Flask(__name__)
app.config["HOST"] = "localhost"
app.config["PORT"] = 5000
app.config["DEBUG"] = True


# JWT
from flask_jwt_extended import JWTManager
import secrets

app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)


# Database
from models import db, DB_NAME, DB_HOST, DB_PORT
from flask_mongoengine import MongoEngineSessionInterface

app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = DB_PORT
app.config["MONGODB_HOST"] = DB_HOST

db.init_app(app)
app.session_interface = MongoEngineSessionInterface(db)


from flask_graphql import GraphQLView
from api import schema

app.add_url_rule('/api', view_func=GraphQLView.as_view('api', schema=schema, graphiql=True))

