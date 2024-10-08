from flask import Flask, request, jsonify
from summarization_api import Summarization  # Replace with the actual path to your PoemController class
from langchain_community.llms import Ollama
from store_data import *

app = Flask(__name__)

# Instantiate the PoemController with the required model
# model = "phi3:medium"  # Replace this with the actual model instance
model = "phi3"
llm = Ollama(model=model, temperature=0.3)          
summ_controller = Summarization(llm)
create_database()

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()    
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Call the summarization function
    output_positive, output_negative, output_neutral = summ_controller.summarization(input_text)
    
    try:
        input_string_joined, input_id_joined = list_to_string(input_text)
        store_data(input_string_joined, input_id_joined, output_positive, output_negative, output_neutral)
    except Exception as e:
        print(e)
    
    return jsonify({"summary_positive": output_positive, "summary_negative": output_negative, "summary_neutral": output_neutral})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
