from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")  # Example: "us-west-2"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "health-genie-chatbot-rag")

if not GOOGLE_API_KEY or not PINECONE_API_KEY:
    raise ValueError("Missing API keys. Set GOOGLE_API_KEY and PINECONE_API_KEY in .env")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists; if not, create it
existing_indexes = pc.list_indexes().names()
if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,  # Use 384 if using MiniLM embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENV
        )
    )

# Initialize Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load Existing Pinecone Index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model
)

# Retriever setup
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# Function to retrieve relevant documents
def retrieve_relevant_docs(query):
    retrieved_docs = retriever.invoke(query)
    return " ".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""

# Function to get Gemini's response
def get_gemini_response(query, context):
    full_prompt = f"Context: {context}\nUser Query: {query}\nProvide a detailed response:"

    response = chat.send_message(full_prompt, stream=True)
    return "".join([chunk.text.strip() for chunk in response]).strip()

# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    current_response = None

    if request.method == "POST":
        user_query = request.form.get("input_text")
        if user_query:
            retrieved_texts = retrieve_relevant_docs(user_query)
            response_text = get_gemini_response(user_query, retrieved_texts)

            session["chat_history"].append(("You", user_query))
            session["chat_history"].append(("Health Genie", response_text))
            session.modified = True

        return redirect(url_for("index"))

    return render_template("index.html", chat_history=session["chat_history"], current_response=current_response)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
