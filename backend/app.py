import os
import faiss
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from llama_index.readers.llama_parse import LlamaParse
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Disable "huggingface/tokenizers" warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Files to save embeddings and FAISS index
EMBEDDINGS_FILE = "embeddings.npy"
FAISS_INDEX_FILE = "faiss_index.faiss"
SEGMENTS_FILE = "segments.npy"

# Initialize OpenAI client
client = None

def init_openai(api_key):
    global client
    client = OpenAI(api_key=api_key)

# ... keep existing code (all the helper functions from your Python script)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        llama_parse_key = request.headers.get('X-Llama-Parse-Key')
        openai_key = request.headers.get('X-OpenAI-Key')
        
        if not message or not llama_parse_key or not openai_key:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Initialize OpenAI client with the provided key
        init_openai(openai_key)
        
        # Get PDF path - assuming PDFs are stored in the public/pdfs directory
        pdf_path = os.path.join('..', 'public', 'pdfs', 'document.pdf')
        
        # Use the semantic search pipeline to get response
        response = semantic_search_pipeline(llama_parse_key, pdf_path, message)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)