import os
import faiss
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from llama_index.readers.llama_parse import LlamaParse
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    """
    Initialize OpenAI client with the provided API key.
    """
    global client
    client = OpenAI(api_key=api_key)


# Step 1: Load and parse PDF with LlamaParse
def parse_pdf_with_llama(api_key, pdf_path):
    """
    Parse a PDF file using LlamaParse.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    llama_parse = LlamaParse(api_key=api_key)
    documents = llama_parse.load_data(pdf_path)
    logging.info(f"Number of extracted documents: {len(documents)}")
    return documents


# Step 2: Split documents into smaller segments
def segment_document(document_text, max_length=200):
    """
    Segment a document into smaller chunks based on maximum length.
    """
    segments = []
    current_segment = []

    for line in document_text.split('\n'):
        if len(" ".join(current_segment)) + len(line) <= max_length:
            current_segment.append(line)
        else:
            segments.append(" ".join(current_segment))
            current_segment = [line]
    
    if current_segment:
        segments.append(" ".join(current_segment))

    return segments


# Step 3: Generate embeddings and save them
def generate_and_save_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    """
    Generate embeddings and save them to a file.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=False)

    np.save(EMBEDDINGS_FILE, embeddings)
    np.save(SEGMENTS_FILE, texts)
    return embeddings


# Step 4: Create FAISS index and save it
def create_and_save_faiss_index(embeddings):
    """
    Create FAISS index and save it to a file.
    """
    embedding_dim = len(embeddings[0])
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    faiss.write_index(index, FAISS_INDEX_FILE)
    return index


# Step 5: Load embeddings and FAISS index
def load_embeddings_and_index():
    """
    Load embeddings, FAISS index, and segments from files.
    """
    if not os.path.exists(EMBEDDINGS_FILE) or not os.path.exists(FAISS_INDEX_FILE):
        raise FileNotFoundError("Embeddings or FAISS index files don't exist. Run initial generation.")

    embeddings = np.load(EMBEDDINGS_FILE)
    index = faiss.read_index(FAISS_INDEX_FILE)
    segments = np.load(SEGMENTS_FILE, allow_pickle=True)
    return embeddings, index, segments


# Step 6: Query GPT function
def ask_gpt(question, context):
    """
    Ask a question to GPT using the provided context.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant who answers questions based on context."},
            {"role": "user", "content": f"Question: {question}\n\nContext: {context}"}
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content


# Step 7: Main pipeline
def semantic_search_pipeline(api_key, pdf_path, query):
    """
    Execute the full semantic search pipeline.
    """
    # Check if embeddings and FAISS index exist
    if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(FAISS_INDEX_FILE):
        embeddings, index, segments = load_embeddings_and_index()
    else:
        # Parsing and segmentation
        parsed_data = parse_pdf_with_llama(api_key, pdf_path)
        segmented_data = []
        for doc in parsed_data:
            text = doc.text if hasattr(doc, "text") else ""
            if text:
                segments = segment_document(text, max_length=200)
                segmented_data.extend(segments)

        # Generate embeddings and create index
        embeddings = generate_and_save_embeddings(segmented_data)
        index = create_and_save_faiss_index(embeddings)
        segments = segmented_data

    # Semantic search
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=1)

    # Get most relevant context
    top_context = segments[indices[0][0]]

    # Generate response with GPT
    return ask_gpt(query, top_context)


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Flask route to handle chat requests.
    """
    try:
        # Extract JSON payload
        data = request.json
        message = data.get('message')
        llama_parse_key = os.getenv('LLAMllx-vbWvgnlEl3mre2RbUnAm9FUgmU0Jb1Cs7j6chsSd6sST1qHWA_PARSE_KEY')
        openai_key = os.getenv('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')
        
        # Validate inputs
        if not message or not isinstance(message, str):
            return jsonify({'error': 'Invalid message format'}), 400

        if not llama_parse_key or not openai_key:
            return jsonify({'error': 'API keys are not configured'}), 500

        # Initialize OpenAI client with the provided key
        init_openai(openai_key)
        
        # Get PDF path - assuming PDFs are stored in the public/pdfs directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, 'public', 'pdfs', 'Actual fake.pdf')

        # Use the semantic search pipeline to get response
        response = semantic_search_pipeline(llama_parse_key, pdf_path, message)
        
        return jsonify({'response': response})

    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        return jsonify({'error': str(e)}), 404

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
