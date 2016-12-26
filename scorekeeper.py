# An app to get texts and keep score.

from twilio.rest import TwilioRestClient
from flask import Flask, request
import os
import datetime

app = Flask(__name__)
@app.route("/")

def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)



class Award(object):
    def __init__(self):
        (to, giver, amount, reason) = parse_incoming_text()
        self.to = to
        self.giver = giver
        self.amount = amount
        self.reason = reason
        self.time = str(datetime.datetime.now())

    def store(self):
        '''
        Store in db.
        '''


class Person(object):
    def __init__(self):
        (name, number) = intro_text()
        self.name = name
        self.number = number
        self.id = assign_id(name, number)

    def assign_id(name, number):
        '''
        Add person to db and return id.
        '''

    def add_points(amt, id):
        '''
        Add amt points to person.
        '''

    def get_points(id):
        '''
        Get total points person has.
        '''

    def get_name(id):
        '''
        Given a number, get the name.
        '''

    def get_number(id):
        '''
        Given a name, get the number
        '''

    def get_id_from_name(name):
        '''
        Given a name, return id.
        '''

    def get_id_from_num(number):
        '''
        Given a number, return id.
        '''



if __name__ == "__main__":
	app.run(debug=True)