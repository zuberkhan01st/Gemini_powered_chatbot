from flask import Flask, request, jsonify
from chatbot.retriever import retrieve_relevant_docs, load_and_store_pdfs
from chatbot.generator import generate_response

app = Flask(__name__)

# Load and store PDFs when the server starts
print("🔄 Processing PDFs for embedding storage...")
load_and_store_pdfs()
print("✅ PDFs loaded successfully!")

@app.route("/")
def home():
    return jsonify({"message": "Health Genie AI Chatbot is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Retrieve relevant medical documents
    retrieved_texts = retrieve_relevant_docs(user_query)

    # Generate AI response
    ai_response = generate_response(user_query, retrieved_texts)

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
