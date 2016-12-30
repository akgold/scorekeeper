from app import app
from app.models import Person, Text
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
			number = str(request.json['From']), 
			body = str(request.json['Body']), 
			time = datetime.now()
			)
		return(str(text.process_text()))
