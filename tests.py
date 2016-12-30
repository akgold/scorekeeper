#!flask/bin/python
import os
import unittest

from app.config import basedir
from app import app, db, views
from app.models import Person, Award, Text
from datetime import datetime
import json

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ################################
    # Person Class
    ################################
    def test_add_points(self):
        p = Person(name = 'alex', number = '123123', total_points = 0)
        db.session.add(p)
        db.session.commit()

        p.add_points(25)
        assert p.total_points == 25.0

    # Award Class
    def test_give_award(self):
        p = Person(name = 'alex', number = '123123', total_points = 0)
        db.session.add(p)
        db.session.commit()

        a = Award(amount = 25, reason = "Passing tests!", time = datetime.now(), getter = p)
        db.session.add(a)
        db.session.commit()

        assert p.total_points == 0

        a.give_award()

        assert p.total_points == 25

    def test_get_person_from_name_and_number(self):
        p = Person(name = 'alex', number = '123123', total_points = 0)
        db.session.add(p)
        db.session.commit()

        q = Person.get_person_from_name('alex')
        r = Person.get_person_from_number('123123')

        assert p == q
        assert p == r
    ################################
    # Text Class
    ################################
    def test_check_if_first(self):
        text = Text(number = "123123", body = "Farts.", time = datetime.now())
        assert text.check_if_first() == True

        p = Person(name = 'alex', number = '123123', total_points = 0)
        db.session.add(p)
        db.session.commit()
        assert text.check_if_first() == False

    def test_add_new_sender(self):
        text = Text(number = "123123", body = "Farts.", time = datetime.now())
        assert Person.get_person_from_number('123123') == None
        text.add_new_sender()
        assert Person.get_person_from_number('123123') != None

    def test_check_name_Format(self):
        # Check one word test
        text = Text(number = "123123", body = "Farts. Farts.", time = datetime.now())
        with self.assertRaises(ValueError) as exp:
            text.check_name_format()

        assert str(exp.exception) == "Your name can only be one word."

        # Check Length test
        text = Text(number = "123123", body = "jskskshdhdbdjddidjjdjdhdhhd", time = datetime.now())
        with self.assertRaises(ValueError) as exp:
            text.check_name_format()

        assert str(exp.exception) == "Sorry, too long. 15 characters or less!"

        # Check properly assessing whether people in db already
        p = Person(name = 'alex', number = '123123', total_points = 0)
        db.session.add(p)
        db.session.commit()
        text = Text(number = "123123", body = "alex", time = datetime.now())
        with self.assertRaises(ValueError) as exp:
            text.check_name_format()

        assert str(exp.exception) == ("Send me your own damn name?!? " + 
                "Unless you share a name with someone, then a nickname, please!")


    def test_add_name(self):
        # Add new sender
        text = Text(number = "123123", body = "First Text!", time = datetime.now())
        text.add_new_sender()

        # Name text
        text = Text(number = "123123", body = "Farts.!?", time = datetime.now())
        assert text.add_name() == "Farts"
        assert Person.get_person_from_number('123123').name == "Farts"

    def test_check_points_format(self):
        #Check that adheres to format [#] to [NAME] for [REASON]
        # Number at open
        text = Text(number = "123123", body = "First Text!", time = datetime.now()) 
        with self.assertRaises(ValueError) as exp:
            text.check_points_format()

        assert str(exp.exception) == "Give some points! Format as [#] to [NAME] for [REASON]."

        text = Text(number = "123123", body = "Alex gets 100 points for awesome", time = datetime.now()) 
        with self.assertRaises(ValueError) as exp:
            text.check_points_format()

        assert str(exp.exception) == "Your text needs to start with a number."

        # Number at open but wrong format
        text = Text(number = "123123", body = "123 points to gryffindor! Yay!", time = datetime.now()) 
        with self.assertRaises(ValueError) as exp:
            text.check_points_format()

        assert str(exp.exception) == "Please format text as [#] to [NAME] for [REASON]."

        # Proper format but don't have name
        text = Text(number = "123123", body = "123 to alex for coding", time = datetime.now()) 
        with self.assertRaises(ValueError) as exp:
            text.check_points_format()

        assert str(exp.exception) == ("Sorry, I don't have the name alex. Please try again.")

        # Working correctly
        p = Person(name = 'alex', number = '123123', total_points = 0)
        q = Person(name = 'xaq', number = '123321', total_points = 0)
        db.session.add(p)
        db.session.commit()

        text = Text(number = "123123", body = "123 to alex for coding", time = datetime.now()) 
        with self.assertRaises(ValueError) as exp:
            text.check_points_format()

        assert str(exp.exception) == ("You can't give yourself points!")

        text = Text(number = "123321", body = "123 to alex for coding", time = datetime.now())
        assert text.check_points_format() == None

    def test_process_text(self):
        # Processing first text from person one
        text = Text(number = "123123", body = "First Text!", time = datetime.now())
        assert Person.get_person_from_number('123123') == None
        assert text.process_text() == "What's your name? One word only, please!"
        assert Person.get_person_from_number('123123') != None

        # Processing second text from person one
        text = Text(number = "123123", body = "First Text!", time = datetime.now())
        assert text.process_text() == "Your name can only be one word."

        text = Text(number = "123123", body = "asdfasfasdfasdfasdfasaf", time = datetime.now())
        assert text.process_text() == "Sorry, too long. 15 characters or less!"

        text = Text(number = "123123", body = "Xaq", time = datetime.now())
        assert text.process_text() == "Got it, your name's Xaq."

        text = Text(number = "123123", body = "Xaq", time = datetime.now())
        assert text.process_text() == "Give some points! Format as [#] to [NAME] for [REASON]."

        # Texts from person 2
        text = Text(number = "123321", body = "Xaq", time = datetime.now())
        assert text.process_text() == "What's your name? One word only, please!"

        text = Text(number = "123321", body = "Xaq", time = datetime.now())
        assert text.process_text() == ("Send me your own damn name?!? " + 
                "Unless you share a name with someone, then a nickname, please!")
        
        text = Text(number = "123321", body = "Alex", time = datetime.now())
        assert text.process_text() == ("Got it, your name's Alex.")

        # Person 1 sending points
        text = Text(number = "123123", body = "Xaq", time = datetime.now())
        assert text.process_text() == "Give some points! Format as [#] to [NAME] for [REASON]."

        text = Text(number = "123123", body = "First Text!", time = datetime.now())
        assert text.process_text() == "Give some points! Format as [#] to [NAME] for [REASON]."

        text = Text(number = "123123", body = "100 points for gryffindor for awesome", time = datetime.now())
        assert text.process_text() == "Please format text as [#] to [NAME] for [REASON]."

        text = Text(number = "123123", body = "100 to shosh for awesome", time = datetime.now())
        assert text.process_text() == "Sorry, I don't have the name shosh. Please try again."

        text = Text(number = "123123", body = "100 to Xaq for sweet tunes", time = datetime.now())
        assert text.process_text() == "You can't give yourself points!"

        time = datetime.now()
        text = Text(number = "123123", body = "100 to Alex for coding so good", time = time)
        assert text.process_text() == "Thanks Xaq! I'm sure Alex deserved those points!"
        assert Person.get_person_from_name('Alex').total_points == 100
        a = Award.query.all()[0]
        assert a.reason == "coding so good"
        assert a.giver == "Xaq"
        assert a.getter == Person.get_person_from_name('Alex')
        assert a.time == time
        assert a.amount == 100

    ################################
    # Scoreboard
    ################################

    def test_get_scoreboard(self):
        with app.test_request_context():
            p = Person(name = 'alex', number = '123456', total_points = 100)
            q = Person(name = 'xaq', number = '123451', total_points = 120)
            r = Person(name = 'shosh', number = '123452', total_points = 150)
            db.session.add_all((p, q, r))
            db.session.commit()

            assert views.get_scoreboard().get_data() == b'{\n  "alex": 100.0, \n  "shosh": 150.0, \n  "xaq": 120.0\n}\n'

if __name__ == '__main__':
    unittest.main()