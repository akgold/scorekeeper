from app import app, models
import flask

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/get_scoreboard', methods = ['GET', 'POST'])
def get_scoreboard():
	scoreboard = dict(models.Person.query.with_entities(models.Person.name, models.Person.total_points).all())
	return flask.jsonify(**scoreboard)	