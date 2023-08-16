from flask import Flask, render_template, request, session
import openai
import os
from dotenv import load_dotenv

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")
page_password = os.getenv("PAGE_PASSWORD")


openai.api_key = private_key
model_engine = "text-davinci-003"  # or any other GPT-3 model try text-curie-001 or text-davinci-003


application = Flask(__name__)

# Set the secret key for session management
application.secret_key = os.urandom(16)

@application.route('/')
def home():
    return render_template('index.html', home = False)

@application.route('/portfolio')
def portfolio():
    return render_template('index.html', home = True)

# create password page
@application.route('/files', methods=['POST'])
def files():
    if request.method == 'POST':
        page_input = request.form.get('page_input')
        if page_input == page_password:
            return render_template('index.html', home=True)
    return render_template('files.html', password=False)



@application.route('/margaret')
def bot():
    session['conversation'] = []
    return render_template('bot.html')

@application.route('/get_response', methods=['POST'])
def get_response():
    # get user input from HTML form
    user_input = request.form['user_input']

    conversation = session.get('conversation', [])

    # add user input to conversation history
    conversation.append('You: ' + user_input)

    # get AI response using OpenAI API
    prompt = '\n'.join(conversation[-20:])  # use last 8 messages as prompt
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text

    # add AI response to conversation history
    conversation.append('' + response)

    # Store updated conversation history in session
    session['conversation'] = conversation

    # render conversation history and AI response to HTML template
    return render_template('bot.html', conversation=conversation)

if __name__ == '__main__':
    application.run(debug=False)
