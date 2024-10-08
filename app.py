from flask import Flask, request, jsonify
from summarization_api import Summarization  # Replace with the actual path to your PoemController class

app = Flask(__name__)

# Instantiate the PoemController with the required model
model = "phi3:medium"  # Replace this with the actual model instance
summ_controller = Summarization(model)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Call the summarization function
    output_positive, output_negative = summ_controller.summarization(input_text)
    
    return jsonify({"summary_positive": output_positive, "summary_negative": output_negative})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
