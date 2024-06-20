from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []

    current_response = None

    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            response_text = get_gemini_response(input_text)
            session['chat_history'].append(("You", input_text))
            session['chat_history'].append(("Health Genie", response_text))
            current_response = response_text
            session.modified = True
        return redirect(url_for('index'))

    return render_template('index.html', chat_history=session['chat_history'], current_response=current_response)

if __name__ == '__main__':
    app.run(debug=True)
