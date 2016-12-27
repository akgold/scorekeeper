from twilio.rest import TwilioRestClient
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

from app import models, views


