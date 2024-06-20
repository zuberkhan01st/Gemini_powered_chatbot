from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No API key provided. Please set the GOOGLE_API_KEY environment variable.")

# Configure the generative AI model
genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get formatted responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text.strip()  # Remove leading/trailing whitespace

    # Apply desired formatting (adjust based on your needs)
    formatted_response = ""
    for line in response_text.splitlines():
        if line.isupper():  # Highlight headings
            formatted_response += f"<strong>{line}</strong><br>"
        else:
            formatted_response += f"{line}<br>"

    return formatted_response.strip()  # Remove leading/trailing newline

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Predefined initial chat
initial_question = (
    "I want you to act as a doctor and come up with creative treatments for illnesses or diseases. "
    "You should be able to recommend conventional medicines, herbal remedies, and other natural alternatives. "
    "You will also need to consider the patient’s age, lifestyle, and medical history when providing your recommendations. "
    "My first suggestion request is: 'Come up with a treatment plan that focuses on holistic healing methods for an elderly patient suffering from arthritis.'"
)

# Route to initialize chat with predefined message
@app.route('/initialize', methods=['GET'])
def initialize():
    session['chat_history'] = []
    initial_response = get_gemini_response(initial_question)
    session['chat_history'].append(("You", initial_question))
    session['chat_history'].append(("Health Genie", initial_response))
    session.modified = True
    return redirect(url_for('index'))

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
