from app import app
from app.models import Person, Text
from twilio.rest import TwilioRestClient 
import flask
import json
from flask import request, render_template
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get_scoreboard', methods = ['GET', 'POST'])
def get_scoreboard():
	scoreboard = dict(Person.query.with_entities(Person.name, Person.total_points).all())
	return flask.jsonify(**scoreboard)	


@app.route('/incoming_text', methods = ['GET', 'POST'])
def incoming_text():
	if request.method == 'POST':
		text = Text(
			number = str(request.form.to_dict()['From']), 
			body = str(request.form.to_dict()['Body']), 
			time = datetime.now()
		)

		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

		client.messages.create(
    		to=text.number, 
    		from_=ACCOUNT_NUM, 
    		body=str(text.process_text())
		)

		return(str(text.process_text()))
