import json
import os

def list_to_string(input_text):
    input_string = []
    input_id = []
    
    for dict1 in input_text:
        input_string.append(dict1['content'])
        input_id.append(str(dict1['id']))
        input_id.append(',')
    
    input_string_joined = ' '.join(input_string)
    input_id_joined = ' '.join(input_id)
    
    return input_string_joined, input_id_joined

def create_database():
    data = {
        
    }
    
    # Define the file path for saving the JSON file
    file_path = "data/sentiment_data.json"
    
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    
    print(f"Sentiment database created at {file_path}")
    
def store_data(input_string_joined, post_id, output_positive, output_negative, output_neutral):
    file_path = "data/sentiment_data.json"
    
    # Check if the file exists, if not create an empty JSON structure
    if not os.path.exists(file_path):
        data = {}
    else:
        # Open the existing file and load the data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    
    print(post_id)
    
    # Store the input and outputs in the correct format
    data[post_id] = {
        "input_id" : post_id,
        "input_text" : input_string_joined,
        "output_positive": output_positive,
        "output_negative": output_negative,
        "output_neutral": output_neutral
    }
        
    # Write the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Use indent for better readability
    
    print(f"New sentiment data saved at {file_path}")

    
    
    