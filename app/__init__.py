from twilio.rest import TwilioRestClient
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
CONFIG_LOC = '/Users/agold/Documents/scorekeeper/app/config.py'
app.config.from_envvar('CONFIG_LOC')
db = SQLAlchemy(app)

from app import models, views


