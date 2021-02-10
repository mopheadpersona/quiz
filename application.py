from flask import Flask, abort, render_template, request
from data import test_quiz 

app = Flask(__name__)


@app.route('/')
def index():
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


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404
