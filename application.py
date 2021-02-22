from flask import Flask, abort, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from uuid import uuid4


app = Flask(__name__)
app.secret_key = 'uran horse button'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://deemaneken:star@localhost/quiz_db'
db = SQLAlchemy(app)
manager = LoginManager(app)

class Quiz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	json_column = db.Column(JSON)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

class LeaderBoard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(128))
	quiz = db.Column(db.String(255))
	result = db.Column(db.Integer)

db.create_all()

@manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

def insert(json):
	data = Quiz(json_column=json)
	db.session.add(data)
	db.session.commit()

def delete(id):
	query = Quiz.query.filter(Quiz.id == id).first()
	db.session.delete(query)
	db.session.commit()

@app.after_request
def redirect_to_signin(response):
	if response.status_code == 401:
		return redirect(url_for('login') + '?next=' + request.url)

	return response

@app.route('/login', methods=['GET', 'POST'])
def login():
	login = request.form.get('login')
	password = request.form.get('password')

	if login and password:
		user = User.query.filter_by(login=login).first()

		if user and check_password_hash(user.password, password):
			login_user(user)

			to_page = request.args.get('next')
			if to_page is None:
				return redirect(url_for('index'))

			return redirect(to_page)
		else:
			flash('Login or password is not correct')
	else:
		flash('Please fill login and password fields')
	
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	login = request.form.get('login')
	password = request.form.get('password')
	password2 = request.form.get('password2')

	if request.method == 'POST':
		if not (login or password or password2):
			flash('Please, fill all fields!')
		elif password != password2:
			flash('Passwords are not equal!')
		else:
			hash_password = generate_password_hash(password)
			new_user = User(login=login, password=hash_password)
			db.session.add(new_user)
			db.session.commit()

			return redirect('login')

	return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/')
def index():
	data = Quiz.query.all()
	quizes = list(map(lambda el: el.json_column, data))
	return render_template('home.html', quizes=data)

@app.route('/delete_quiz/<int:id>')
@login_required
def delete_quiz(id):
	delete(id)
	return redirect(url_for('index'))

@app.route('/quiz/<int:id>')
@login_required
def quiz(id):
	data = Quiz.query.filter(Quiz.id == id).first()
	return render_template('quiz.html', quiz=data)

@app.route('/create-quiz')
@login_required
def add_quiz():
	return render_template('create.html')

@app.route('/submit-new-quiz', methods=['POST'])
@login_required
def create_quiz():
	data = {}
	query = request.form
	counter = 0
	correct_id = str(uuid4())

	for key in query:
		if key.startswith('questions[question]'):
			counter += 1

	questions = []
	for i in range(1, counter + 1):
		question = {}
		question['question'] = query[f'questions[question][{i}]']
		question['id'] = str(uuid4())
		question['correct_answer_id'] = correct_id
		answers = []
		for j in range(1, 5):
			answer = {}
			answer['answer'] = query[f'answers[question][{i}][answer][{j}]']
			if query[f'correct_answer{i}'] == f'answers[question][{i}][answer][{j}]':
				answer['id'] = correct_id
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

@app.route('/submit/<int:id>', methods=['POST'])
@login_required
def submit(id):
	query = Quiz.query.filter(Quiz.id == id).first()
	results = request.form
	points = 0

	for question in query.json_column['questions']:
		if results[question['id']] == question['correct_answer_id']:
			points += 1

	user = current_user.login
	quiz = query.json_column["name"]
	new_row = LeaderBoard(user=user, quiz=quiz, result=points)
	db.session.add(new_row)
	db.session.commit()

	score = {}
	score["length"] = query.json_column["length"]
	score["result"] = points

	return render_template('score.html', score=score)


@app.route('/leader-board')
@login_required
def leader_board():
	data = LeaderBoard.query.all()

	return render_template('leaderboard.html', users=data)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404
