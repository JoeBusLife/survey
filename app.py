from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey
# from random import randint,  choice, sample

app = Flask(__name__)

app.config['SECRET_KEY'] = "hi"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
quests = satisfaction_survey.questions
next_q_id = 0

@app.route('/')
def survey_start_page():
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template('home.html', survey_title=survey_title, survey_instructions=survey_instructions, next_q_id=next_q_id)

@app.route('/questions/<int:q_id>')
def show_question(q_id):
    if(len(responses) >= len(quests)):
        return redirect('/thankyou')
    elif(q_id != next_q_id):
        flash('Invalid question url!', 'error')
        return redirect(f'/questions/{next_q_id}')
    
    quest = quests[q_id]
    question = quest.question
    choices = quest.choices
    allow_text = quest.allow_text
    
    return render_template('question.html', q_id=q_id, question=question, choices=choices, allow_text=allow_text)

@app.route('/answer', methods=['POST'])
def submit_question():
    responses.append(request.form["answer"])
    global next_q_id
    next_q_id += 1
    return redirect(f'/questions/{next_q_id}')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')