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
        people = Person.query.all()
        keys = ['name', 'points', 'number']
        ret = []
        for p in people:
                ret.append(dict(zip(keys, [p.name, p.total_points, p.number])))
        return flask.jsonify(*ret)


@app.route('/incoming_text', methods = ['GET', 'POST'])
def incoming_text():
	if request.method == 'POST':
		text = Text(
			number = str(request.form.to_dict()['From']), 
                        body = unicode(request.form.to_dict()['Body']),
			time = datetime.now()
		)

                ACCOUNT_SID = ""
                AUTH_TOKEN = ""
                ACCOUNT_NUM = ""
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 


                process = unicode(text.process_text())
		client.messages.create(
			to=text.number,
			from_=ACCOUNT_NUM,
			body=process
		)

                return(process)
