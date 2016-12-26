from app import db

class Award(object):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    reason = db.Column(db.Text)
    time = db.Column(db.DateTime)

    to_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    from_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __init__(self):
        (to, giver, amount, reason) = parse_incoming_text()
        self.to_id = to
        self.from_id = 
        self.amount = amount
        self.reason = reason
        self.time = str(datetime.datetime.now())

    def store(self):
        '''
        Store in db.
        '''