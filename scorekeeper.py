# An app to get texts and keep score.

from twilio.rest import TwilioRestClient
from flask import Flask, request
import os
import datetime

app = Flask(__name__)

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

    def add(self):
        '''
        Add person to db.
        '''

    def add_points(amt, name):
        '''
        Add amt points to person.
        '''

    def get_points(number):
        '''
        Get total points person has.
        '''

    def get_name(number):
        '''
        Given a number, get the name.
        '''

    def get_number(name):
        '''
        Given a name, get the number
        '''

    def exists(name):
        '''
        Given a name, check if exists.
        '''



if __name__ == "__main__":
	app.run(debug=True)