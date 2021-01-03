
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES_KEY = "responses"
# ^^^ Need help understanding what this is doing
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route('/')
def start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    return render_template('start.html', title=title, instructions=instructions, questions=questions)


@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route('/answer', methods=["POST"])
def get_response():
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    # ^^^ Why is it necessary to rebind the name insessions when appending to a list?
    if (len(responses) == len(satisfaction_survey.questions)):
        return render_template('complete.html', responses=responses)
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:id>')
def render_question(id):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    questions = satisfaction_survey.questions
    if (len(responses) != id):
        flash (f"Invalid question ID:{id}")
        return redirect(f"/questions/{len(responses)}")
    return render_template('questions.html', questions=questions, id=id)
