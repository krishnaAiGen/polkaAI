from langchain_community.llms import Ollama
import re

class Summarization:
    def __init__(self, llm):
        self.llm = llm
    
    def get_text_length(self, input_text):
        splited_text = input_text.split(' ')
        return int(len(splited_text)/6)  
    
    def get_group_id(self, input_text):        
        grouped_id_text = {}
        
        for dict1 in input_text:
            id1 = dict1['id']
            content = dict1['content']
            
            if id1 not in grouped_id_text:
                grouped_id_text[id1] = content
            
            else:
                grouped_id_text[id1] = grouped_id_text[id1] + '\n' +  content
        
        return grouped_id_text
    
    def get_positive_negative_dict(self, grouped_id):
        positive_string = ''
        negative_string = ''
        neutral_string = ''
        
        positive_counter = 0
        negative_counter = 0
        neutral_count = 0
        
        
        # llm = Ollama(model=self.model, temperature=0.3)          

        for id1, content in grouped_id.items():
            output = self.llm.invoke("tell me whether this text is positive, negative or neutral and output should only contain either positive or negative or neutral" + content)
            # output = llm.invoke("tell me whether this text is positive, negative or neutral and output should only contain either positive or negative or neutral" + content)
            output_lower = output.lower()
            match = re.search(r'\b(positive|negative|neutral)\b', output_lower)
            
            if match:
                sentiment = match.group(0)
            else:
                sentiment = None
        
            if sentiment == 'positive':
                positive_string = positive_string + content
                positive_counter = positive_counter + 1
            
            elif sentiment == 'negative':
                negative_string = negative_string + content
                negative_counter = negative_counter + 1
            
            elif sentiment == 'neutral' or sentiment == None:
                neutral_string = neutral_string + content
                neutral_count = neutral_count + 1
                
        positive_negative_dict = [
            {
                "content" : positive_string,
                "percent": positive_counter/len(grouped_id),
                "type" : "positive"
                },
            {
                "content" : negative_string,
                "percent" : negative_counter/len(grouped_id),
                "type" : "negative"
                },
            
            {
                "content" : neutral_string,
                "percent" : neutral_count/len(grouped_id),
                "type" : "neutral"
                }
            ]

        
        return positive_negative_dict
                
    def get_summary(self, input_text, summary_type):  
        length_input = self.get_text_length(input_text)
        original_input_length = int(length_input * 6)
        print("Original length:", original_input_length)
        print("Length input (chunks):", length_input)
        
        # llm = Ollama(model=self.model, temperature=0.3)          

        def invoke_with_retry(prompt, max_retries=3):
            retries = 0
            output = None
            while output is None and retries < max_retries:
                output = self.llm.invoke(prompt)
                retries += 1
            return output
    
        def adjust_length_with_reinvoke(text, original_prompt, max_retries=3):
            # Check if the output is within the desired range (150-200 words)
            for attempt in range(max_retries):
                words = text.split()
                word_count = len(words)
                
                # If the text is within the target range, return it as is
                if 50 <= word_count <= 80:
                    return text
                
                # If the text is too long, reinvoke the LLM to generate within the target range
                print(f"Attempt {attempt+1}: Reinvoking LLM for a more concise summary (current length: {word_count} words)...")
                refined_prompt = original_prompt + " Ensure the summary is between 50-80 words."
                refined_text = invoke_with_retry(refined_prompt)
                
                if 50 <= len(refined_text.split()) <= 80:
                    return refined_text
                
                # Update text for next iteration or return if refined_text is valid
                if refined_text:
                    text = refined_text
            
            # Return the last generated text if it is still not within the range
            return text

        # Generate positive summary with a word constraint   
        prompt_list = {
            "positive" : "Generate a concise positive summary of around 50-80 words for the following text and don't give word count and unnecessary information in the output': ",
            "negative": "Generate a concise negative summary of around 50-80 words for the following text and don't give word count and unnecessary information in the output: ",
            "neutral": "Generate a concise neutral summary of around 50-80 words for the following text and don't give word count and unnecessary information in the output: "

            }
        
        output_list = []
        temp_prompt = prompt_list[summary_type] + f"{input_text}"
        output = invoke_with_retry(temp_prompt)
        if len(output.split()) >= 80 :
            output_refined = adjust_length_with_reinvoke(output, temp_prompt)
            return output_refined
            
        if len(output.split()) < 80:
            return output

        
        return output
    
    def refine_output(self, output_list, positive_negative_dict):
        output_list_refined = []
        
        for index in range(len(output_list)):
            if positive_negative_dict[index]['type'] == 'positive':
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling optimistic."
            
            elif positive_negative_dict[index]['type'] == 'negative':
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling against it."
            
            else:
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling neutral."
            
            if len(output_list[index]) == 0:
                final_text = output_list[index]
            else:
                final_text = prefix + output_list[index]
                
            output_list_refined.append(final_text)
        
        
        return output_list_refined
  
    def summarization(self, input_text):
        # Generate positive and negative summaries
        grouped_id = self.get_group_id(input_text)
        positive_negative_dict = self.get_positive_negative_dict(grouped_id)
        print(positive_negative_dict)
        
        output_list = []
        for dict1 in positive_negative_dict:
            input_text = dict1['content']
            summary_type = dict1['type']
            
            if len(input_text) == 0:
                output = input_text
            else:
                output = self.get_summary(input_text, summary_type)
            output_list.append(output)
        
        output_list_refined = self.refine_output(output_list, positive_negative_dict)
        
        return output_list_refined[0], output_list_refined[1], output_list_refined[2]
