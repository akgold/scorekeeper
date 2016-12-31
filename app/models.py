from app import db
import collections
from twilio.rest import TwilioRestClient

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    number = db.Column(db.String(120), unique=True)
    total_points = db.Column(db.Float)

    #given = db.relationship('award', back_populates = 'giver', 
     #   foreign_keys = [given_id])
    gotten = db.relationship('Award', backref = 'getter', lazy = 'dynamic')

    def __repr__(self):
        return '<Person %r>' % (self.name)


    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def add_points(self, amt):
        self.total_points += amt
        db.session.commit()

    @staticmethod
    def get_person_from_name(name):
        return Person.query.filter(Person.name == name).first()

    @staticmethod
    def get_person_from_number(number):
        return Person.query.filter(Person.number == number).first()


class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    reason = db.Column(db.Text)
    time = db.Column(db.DateTime)

    getter_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    giver = db.Column(db.Text)
    #getter_id = db.relationship('Person', backref = 'gotten', lazy = 'dynamic')

    #giver = db.relationship('Person', back_populates = 'given', 
     #   foreign_keys = [giver_id])
    #getter = db.relationship('Person', back_populates = 'gotten', 
     #   foreign_keys = [getter_id])

    def __repr__(self):
        return '<Award %r>' % (self.amount)

    def give_award(self):
        self.getter.add_points(self.amount)

        ACCOUNT_SID = ""
        AUTH_TOKEN = ""
        ACCOUNT_NUM = ""
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
			to=self.getter.number,
			from_=ACCOUNT_NUM,
			body=("Wow wow wow! You just got " + str(self.amount) +
                        " from " + self.giver + " for " + self.reason+ ".")
                )



class Text(object):
    def __init__(self, number, body, time):
        self.number = number
        self.body = body
        self.time = time

    def check_if_first(self):
        return Person.get_person_from_number(self.number) == None

    def add_new_sender(self):
        p = Person(name = self.number, number = self.number, total_points = 0)
        db.session.add(p)
        db.session.commit()

    def check_name_format(self):
        name = self.body.split()
        if(len(name) != 1):
            raise ValueError("Your name can only be one word.")

        if(len(name[0]) >= 15):
            raise ValueError("Sorry, too long. 15 characters or less!")

                # Deal with non-uniqueness
        if(Person.get_person_from_name(name[0].replace(".", "").replace("!", "").replace("?", "")) != None):
            raise ValueError("Send me your own damn name?!? " + 
                "Unless you share a name with someone, then a nickname, please!")


    def add_name(self):
        # Get person from number
        p = Person.get_person_from_number(self.number)

        # Remove any punctuation and assign.
        p.name = self.body.replace(".", "").replace("!", "").replace("?", "")
        db.session.add(p)
        db.session.commit()

        return p.name
        
            

    def process_text(self):
        # Handle first text from person
        if (self.check_if_first() == True):
            self.add_new_sender()
            return "What's your name? One word only, please!"

        # Handle naming text
        p = Person.get_person_from_number(self.number)
        if(self.body == "CHANGE NAME"):
                p.name = self.number
                db.session.add(p)
                db.session.commit()

                return "Ok, what's your name? One word only, please!"

        if(self.body == "MY NAME"):
                return "Your name is " + p.name + "."

        if (p.name == self.number):
            try: 
                self.check_name_format()
            except ValueError as e:
                return str(e)
            return "Got it, your name's " + self.add_name() + "."


        # Handle points assignment
        # Format is [#] to [NAME] for [REASON]
        text = self.body.split()

        try:
            self.check_points_format()
        except ValueError as e:
            return str(e)

        # Allow people to use format [#] points to [NAME] for [REASON]
        add = 0
        if text[1] == "points":
            add = 1

        name = text[2 + add]

        getter = Person.get_person_from_name(name)
        if(getter == None):
            return("Sorry, I don't have " + name + ". Maybe format text right?")
        giver = Person.get_person_from_number(self.number)

        a = Award(amount = text[0], reason = " ".join(text[4:len(text)]), 
            time = self.time, getter = getter, giver = giver.name)
        db.session.add(a)
        db.session.commit()

        a.give_award()

        return ("Thanks " + a.giver + "! I'm sure " + 
        a.getter.name + " deserved those points for "+ a.reason + ".")

    def check_points_format(self):
        # Should really extract points format and return
        text = self.body.split()

        if(len(text) < 5):
            raise ValueError("Give some points! Format as [#] to [NAME] for [REASON].")

        # Parse text
        add = 0
        if text[1] == "points":
            add = 1

        fill1 = text[1 + add]
        fill2 = text[3 + add]
        name = text[2 + add]

        # Check parts
        try:
            amt = float(text[0])
        except ValueError:
            raise ValueError("Your text needs to start with a number.")

        if(amt < -1):
            raise ValueError("So mean! No less than -1!")

        if(amt > 10):
            raise ValueError("Be reasonable. Point values between -1 and 10 only.")
        
        if(fill1 != "to" or fill2 != "for"):
            raise ValueError("Please format text as [#] to [NAME] for [REASON].")

        if(Person.get_person_from_name(name) == None):
            raise ValueError("Sorry, I don't have the name " + 
                name + ". Please try again.") 

        if(Person.get_person_from_name(name) == Person.get_person_from_number(self.number)):
            raise ValueError("You can't give yourself points!")




