from flask import Flask, request, jsonify
from threading import Lock
from summarization_api import Summarization
from langchain_ollama.llms import OllamaLLM
from store_data import *
from model import InitializeModel

# Global lock to ensure sequential processing
request_lock = Lock()

summ_model = OllamaLLM(model="mistral", temperature=1)
llm_list = InitializeModel()
summ_controller = Summarization(llm_list, summ_model)

create_database()
app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    with request_lock:
        try:
            print("Processing request")
            data = request.get_json()   
            input_text = data.get('text')
            
            if not input_text:
                return jsonify({"error": "No text provided"}), 400
            
            # Extract post_id from first element
            post_id = input_text[0]['postId']
            input_text.pop(0)
            
            # Perform summarization
            output_positive, output_negative, output_neutral = summ_controller.summarization(input_text)
            
            # Store data
            try:
                input_string_joined, input_id_joined = list_to_string(input_text)
                store_data(input_string_joined, post_id, output_positive, output_negative, output_neutral)
            except Exception as e:
                print(f"Storage error: {e}")
            
            return jsonify({
                "summary_positive": output_positive, 
                "summary_negative": output_negative, 
                "summary_neutral": output_neutral
            })
        
        except Exception as e:
            print(f"Request processing error: {e}")
            return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, threaded=False)