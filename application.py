from flask import Flask, abort, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.dialects.postgresql import JSON

from data import test_quiz, test_humans, test_quizes


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://deemaneken:star@localhost/quiz_db'
#db = SQLAlchemy(app)
#
#class Quiz(db.Model):
#	id = db.Column(db.Integer, primary_key=True)
#	json_column = db.Column(JSON)
#
#db.create_all()


@app.route('/')
def index(): 
	return render_template('home.html', quizes=test_quizes)

@app.route('/quiz')
def quiz():
	# return test_quiz
	return render_template('quiz.html', quiz=test_quiz)

@app.route('/create-quiz')
def add_quiz():
	return render_template('create.html')

@app.route('/submit-new-quiz', methods=['POST'])
def create_quiz():
	data = {}
	query = request.form
	counter = 0

	for key in query:
		if key.startswith('questions[question]'):
			counter += 1

	questions = []
	for i in range(1, counter + 1):
		question = {}
		question['question'] = query[f'questions[question][{i}]']
		question['correct_answer_id'] = 'the_id'
		answers = []
		for j in range(1, 5):
			answer = {}
			answer['answer'] = query[f'answers[question][{i}][answer][{j}]']
			if query.get(f'correct[question][{i}][answer][{j}]'):
				answer['id'] = 'the_id'
			else:
				answer['id'] = 'just_id'
			answers.append(answer)
		question['answers'] = answers
		questions.append(question)

	data['name'] = query['name']
	data['description'] = query['description']
	data['length'] = str(counter)
	data['questions'] = questions

	return data

@app.route('/submit-quiz', methods=['POST'])
def process_quiz():
	results = request.form
	points = 0

	for question in test_quiz['questions']:
		if results[question['id']] == question['correct_answer_id']:
			points += 1

	return str(points)

@app.route('/leader-board')
def leader_board():
	return render_template('leaderboard.html', humans=test_humans)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404
