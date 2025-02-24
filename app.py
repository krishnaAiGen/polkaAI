from flask import Flask, request, jsonify
from threading import Lock
import logging
import signal
import time
from summarization_api import Summarization
from langchain_ollama.llms import OllamaLLM
from store_data import *
from model import InitializeModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global lock to ensure sequential processing
request_lock = Lock()

# Initialize summarization model
summ_model = OllamaLLM(model="mistral", temperature=1)
llm_list = InitializeModel()
summ_controller = Summarization(llm_list, summ_model)

create_database()
app = Flask(__name__)

# Set of blocked IPs (can be dynamically updated)
BLOCKED_IPS = set()

# Rate limiting dictionary (IP-based)
request_count = {}
RATE_LIMIT = 10  # Max requests per minute per IP
BLOCK_THRESHOLD = 20  # If exceeded, the IP gets blocked
CLEANUP_INTERVAL = 60  # Cleanup interval for rate limits

# Function to clear rate-limited IPs every CLEANUP_INTERVAL seconds
def cleanup_rate_limits():
    while True:
        time.sleep(CLEANUP_INTERVAL)
        request_count.clear()

# Signal handler to prevent server crash from external signals
def signal_handler(sig, frame):
    logging.warning("Received termination signal. Shutting down gracefully.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.before_request
def block_malicious_requests():
    """Block known malicious IPs and rate-limit requests."""
    client_ip = request.remote_addr

    # Block known bad IPs
    if client_ip in BLOCKED_IPS:
        logging.warning(f"Blocked request from {client_ip}")
        return jsonify({"error": "Access denied"}), 403

    # Rate limiting check
    request_count[client_ip] = request_count.get(client_ip, 0) + 1
    if request_count[client_ip] > RATE_LIMIT:
        logging.warning(f"Rate limit exceeded for {client_ip}")
        if request_count[client_ip] > BLOCK_THRESHOLD:
            BLOCKED_IPS.add(client_ip)
            logging.warning(f"IP {client_ip} has been permanently blocked due to excessive requests.")
        return jsonify({"error": "Rate limit exceeded"}), 429

@app.route('/summarize', methods=['POST'])
def summarize_text():
    """Endpoint to summarize text while handling errors robustly."""
    with request_lock:
        try:
            logging.info("Processing request")
            data = request.get_json()

            if not isinstance(data, dict):
                logging.error("Received invalid JSON format")
                return jsonify({"error": "Invalid request format"}), 400
            
            input_text = data.get('text')

            if not input_text or not isinstance(input_text, list):
                logging.error("Missing or invalid 'text' field in request")
                return jsonify({"error": "No valid text provided"}), 400
            
            if not isinstance(input_text[0], dict) or 'postId' not in input_text[0]:
                logging.error("Invalid input structure")
                return jsonify({"error": "Invalid input format"}), 400

            # Extract post_id and remove from input
            post_id = input_text[0]['postId']
            input_text.pop(0)

            # Perform summarization with timeout
            try:
                output_positive, output_negative, output_neutral = summ_controller.summarization(input_text)
            except Exception as e:
                logging.error(f"Summarization error: {e}")
                return jsonify({"error": "Summarization failed"}), 500

            # Store data securely
            try:
                input_string_joined, input_id_joined = list_to_string(input_text)
                store_data(input_string_joined, post_id, output_positive, output_negative, output_neutral)
            except Exception as e:
                logging.error(f"Storage error: {e}")

            return jsonify({
                "summary_positive": output_positive, 
                "summary_negative": output_negative, 
                "summary_neutral": output_neutral
            })
        
        except Exception as e:
            logging.error(f"Unexpected server error: {e}")
            return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    from threading import Thread
    # Start the rate limit cleanup thread
    Thread(target=cleanup_rate_limits, daemon=True).start()
    app.run(host='0.0.0.0', port=6000, threaded=True)
