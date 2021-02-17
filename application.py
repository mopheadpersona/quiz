from flask import Flask, abort, render_template, request
from data import test_quiz, test_humans, test_quizes

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('home.html', quizes=test_quizes)

@app.route('/quiz')
def quiz():
	# return test_quiz
	return render_template('quiz.html', quiz=test_quiz)

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
