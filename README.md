A scorekeeper app.

To set virtual environment and install deps:
`virtualenv env && . env/bin/activate && pip install -r requirements.txt`

To Run:
Go to folder with `db_create.py`
`./db_create.py`
`gunicorn app:app -b localhost:8000 &`

Config file:
In order for this app to work, need to set up a config file `app/config.py`. Format as below:

`import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

ACCOUNT_SID = "123456"              
AUTH_TOKEN = "123456"                 
ACCOUNT_NUM = "+12405555555"`



Usage: 
* Users text a number hosted by Twilio in a particular format
	* `#` to `NAME` for `REASON`
* App stores their messages and keeps track of totals.
* Texts them back if cannot parse.
* Texts them back fun responses? Fun things to do at party?
* Displays fun message on monitor.


This is a great tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
