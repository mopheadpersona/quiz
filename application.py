from flask import Flask, abort, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

from uuid import uuid4

from data import test_quiz, test_humans, test_quizes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://deemaneken:star@localhost/quiz_db'
db = SQLAlchemy(app)

class Quiz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	json_column = db.Column(JSON)


def insert(json):
	data = Quiz(json_column=json)
	db.session.add(data)
	db.session.commit()


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
	correct_id = uuid4()

	for key in query:
		if key.startswith('questions[question]'):
			counter += 1

	questions = []
	for i in range(1, counter + 1):
		question = {}
		question['question'] = query[f'questions[question][{i}]']
		question['correct_answer_id'] = str(correct_id)
		answers = []
		for j in range(1, 5):
			answer = {}
			answer['answer'] = query[f'answers[question][{i}][answer][{j}]']
			if query[f'correct_answer{i}'] == f'answers[question][{i}][answer][{j}]':
				answer['id'] = str(correct_id) 
			else:
				answer['id'] = str(uuid4())
			answers.append(answer)
		question['answers'] = answers
		questions.append(question)

	data['name'] = query['name']
	data['description'] = query['description']
	data['length'] = str(counter)
	data['questions'] = questions

	insert(data)
	return redirect('/')

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
