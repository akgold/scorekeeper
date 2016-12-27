from twilio.rest import TwilioRestClient
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import datetime
import os

app = Flask(__name__)
Bootstrap(app)
CONFIG_LOC = '/Users/agold/Documents/scorekeeper/app/config.py'
app.config.from_envvar('CONFIG_LOC')
db = SQLAlchemy(app)

from app import models, views


