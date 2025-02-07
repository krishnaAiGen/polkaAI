from flask import Flask, request, jsonify
from summarization_api import Summarization  # Replace with the actual path to your PoemController class
from langchain_ollama.llms import OllamaLLM
from store_data import *
from model import InitializeModel


summ_model = OllamaLLM(model="mistral", temperature=1)
llm_list =  InitializeModel()
summ_controller = Summarization(llm_list, summ_model)     
 
create_database()

def summarize_text():
    data = {
    "text": [
        {
            "postId": "2772",
            "network": "polkadot"
        },
        {
            "content": "It goes without saying that Polkadot—especially OpenGov—wouldn’t be what it is today without the Polkassembly team. Their work has been crucial in making governance more accessible and transparent. Looking forward to seeing them continue to innovate and strengthen the ecosystem!",
            "id": "9384"
        },
        {
            "content": "Really liking the direction Polkassembly is taking with OpenGov, especially around bounties and delegation. The improved curator dashboard and structured funding for bounties has made it easier to track and manage contributions, which is huge for accountability. Also, the upgrades around progress reports have been something new. It’s exciting to see partnerships increasing at Polkassembly. Excited to see the proposed features in 2025!",
            "id": "24890"
        },
        {
            "content": "Expand governance infrastructure by introducing JAM-based governance middleware, multichain support, and extended off-chain participation tools. Really excited to see Polkassembly pushing OpenGov forward! The focus on JAM-based governance, multichain support, and better off-chain participation tools is exactly what’s needed to make governance more accessible and efficient. Giving the community more ways to engage—without relying so much on the treasury—is a huge win. Looking forward to seeing these improvements in action!",
            "id": "22393"
        },
        {
            "content": "Supercool roadmap. JAM is the next big thing for Polkadot.",
            "id": "24888"
        }
    ]
}

    
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Call the summarization function
    post_id = input_text[0]['postId']
    input_text.pop(0)
    
    output_positive, output_negative, output_neutral = summ_controller.summarization(input_text)
    
    try:
        input_string_joined, input_id_joined = list_to_string(input_text)
        store_data(input_string_joined, post_id, output_positive, output_negative, output_neutral)
    except Exception as e:
        print(e)
    
    return jsonify({"summary_positive": output_positive, "summary_negative": output_negative, "summary_neutral": output_neutral})

if __name__ == "__main__":
    summarize_text()
    

        
    
    
