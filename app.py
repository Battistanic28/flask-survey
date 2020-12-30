from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
    if (len(responses) != id):
        flash (f"Invalid question ID:{id}")
        return redirect(f"/questions/{len(responses)}")
    return render_template('questions.html', questions=questions, id=id)

@app.route('/answer', methods=["POST"])
def get_response():
    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(satisfaction_survey.questions)):
        return render_template('complete.html', responses=responses)

    else:
        return redirect(f'/questions/{len(responses)}')
    
