# Health Genie

Health Genie is a Flask-based AI-powered chatbot that provides personalized medical advice and recommendations using Google Gemini Pro. The platform is restricted to medical-related queries, offering information on health, diseases, treatments, and holistic healing methods.

---

## Features
- **AI-Powered Medical Assistance**: Provides medical advice using Google Gemini Pro's generative AI model.
- **Medical Query Validation**: Ensures users can only ask health-related questions. Non-medical queries are declined politely.
- **Chat History**: Retains the conversation history for the current session for user reference.
- **Predefined Initialization**: Starts with an example question to guide users on how to interact with the chatbot.

---

## Technology Stack
- **Backend**: Flask
- **Frontend**: HTML, CSS
- **AI Model**: Google Gemini Pro
- **Environment Management**: Python `dotenv`

---

## Setup Instructions

### Prerequisites
- Python 3.8 or above
- Google Generative AI API key (Gemini Pro access)
- Flask, dotenv, and google-generativeai Python libraries

### Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd health-genie
   ```
### Installation
2. **Install Dependencies**:
   ```bash
   pip install flask python-dotenv google-generativeai
```
