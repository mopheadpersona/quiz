# Quiz app running on [Flask](https://flask.palletsprojects.com/en/1.1.x/) with [PostreSQL](https://www.postgresql.org)

## To run Quiz online:
	* open [Quiz](https://kvizo-app.herokuapp.com)
	* create new account
	* play existed quizes or create a new one
	* to delete quiz use admin account

## To run Quiz localy:
	* create postgreSQL database localy
	* clone this repo `https://github.com/mopheadpersona/quiz.git`
	* `cd quiz`
	* `pip3 install pipenv`
	* `pipenv shell`
	* change database link on `app.py`
	* change env `ENV = 'dev'`
	* python3 app.py