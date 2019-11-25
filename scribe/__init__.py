import os

import yaml
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))

app.config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY']
app.config['TEMPLATES_AUTO_RELOAD']

db = SQLAlchemy(app)

# we import all our blueprint routes here
from scribe.main.routes import main

# Here we register the various blue_prints of our app
app.register_blueprint(main)
