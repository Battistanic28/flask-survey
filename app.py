from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    return render_template('base.html', title=title, instructions=instructions, questions=questions)

@app.route('/questions/<int:id>')
def render_question(id):
    questions = satisfaction_survey.questions
    return render_template('questions.html', questions=questions, id=id)