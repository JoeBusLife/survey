from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey
quests = satisfaction_survey.questions

app = Flask(__name__)

app.config['SECRET_KEY'] = "hi"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def survey_start_page():
    """
    Displays survey start page with survey name, instruction and a start button
    - If survey is started but not completed show continue button
    """
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    
    next_q_id = len(session['responses']) if session.get('responses') != None else None
    continue_btn = True if next_q_id != None and next_q_id != len(quests) else False
    
    return render_template('home.html', survey_title=survey_title, survey_instructions=survey_instructions, next_q_id=next_q_id, continue_btn=continue_btn)


@app.route('/start', methods=['POST'])
def survey_start():
    """Start survey by resetting responses in session and redirecting to first question page"""
    session['responses'] = []
    return redirect(f'/questions/0')


@app.route('/questions/<int:q_id>')
def show_question(q_id):
    """Display requested question if survey is started but not completed and the requested question is the next unawnsered question"""
    if(session.get('responses') is None):
        flash("Didn't start survey yet!", "error")
        return redirect('/')
    
    next_q_id = len(session.get('responses'))
    
    if(next_q_id >= len(quests)):
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
    """Store awnser to question and redirect to next question"""
    responses = session['responses']
    responses.append(request.form["answer"])
    session['responses'] = responses
    
    next_q_id = len(responses)
    return redirect(f'/questions/{next_q_id}')


@app.route('/thankyou')
def thankyou():
    """
    Check to make sure survey has been started and completed by user:
    - if it hasen't then redirect to start page
    - if it has then show page thanking user for completeing the survey
    """
    responses = session.get('responses')
    if(not responses or len(responses) < len(quests)):
        flash("Didn't complete survey yet!", "error")
        return redirect('/')
    
    return render_template('thankyou.html')