A scorekeeper app.

To set virtual environment and install deps:
`virtualenv env && . env/bin/activate && pip install -r requirements.txt`

To Run:
`gunicorn app:app -b localhost:8000 &`

Usage: 
* Users text a number hosted by Twilio in a particular format
	* `#` to `NAME` for `REASON`
* App stores their messages and keeps track of totals.
* Texts them back if cannot parse.
* Texts them back fun responses? Fun things to do at party?
* Displays fun message on monitor.


This is a great tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
