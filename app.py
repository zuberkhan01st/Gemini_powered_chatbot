from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Health Genie - Your Mental and Pressure Relief Assistant")

st.title("Health Genie")
st.subheader("Empowering You with Reliable Information and Support")

# Disclaimer for responsible health advice
st.write(
    """**Disclaimer:** Health Genie provides informative resources and cannot diagnose illnesses or replace professional medical advice. Always consult with a healthcare professional for personalized guidance."""
)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input and response handling
input_text = st.text_input("Ask your question about mental or pressure relief:", key="input")
submit_button = st.button("Ask Health Genie")

if submit_button and input_text:
    response = get_gemini_response(input_text)
    
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    
    # Display the response
    st.subheader("Health Genie Response")
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    st.write(response_text)
    
    # Add bot response to session state chat history
    st.session_state['chat_history'].append(("Health Genie", response_text))

# Display the chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"**{role}:** {text}")

st.write("**Additional Resources:**")
st.write("- National Alliance on Mental Illness (NAMI): [https://www.nami.org/](https://www.nami.org/)")
st.write("- MentalHealth.gov: [https://www.samhsa.gov/mental-health](https://www.samhsa.gov/mental-health)")
st.write("- Crisis Text Line: Text HOME to 741741 (US)")
