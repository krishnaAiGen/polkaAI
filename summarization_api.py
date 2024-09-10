from langchain_community.llms import Ollama

class Summarization:
    def __init__(self, model):
        self.model = model
    
    def get_text_length(self, input_text):
        splited_text = input_text.split(' ')
        return int(len(splited_text)/6)  
    
    def get_summary(self, input_text):  
        length_input = self.get_text_length(input_text)
        original_input_length = int(length_input * 6)
        print("Original length:", original_input_length)
        print("Length input (chunks):", length_input)
        
        llm = Ollama(model=self.model, temperature=0.3)          

        def invoke_with_retry(prompt, max_retries=3):
            retries = 0
            output = None
            while output is None and retries < max_retries:
                output = llm.invoke(prompt)
                retries += 1
            return output
    
        def adjust_length_with_reinvoke(text, original_prompt, max_retries=3):
            # Check if the output is within the desired range (150-200 words)
            for attempt in range(max_retries):
                words = text.split()
                word_count = len(words)
                
                # If the text is within the target range, return it as is
                if 20 <= word_count <= 40:
                    return text
                
                # If the text is too long, reinvoke the LLM to generate within the target range
                print(f"Attempt {attempt+1}: Reinvoking LLM for a more concise summary (current length: {word_count} words)...")
                refined_prompt = original_prompt + " Ensure the summary is between 150-200 words."
                refined_text = invoke_with_retry(refined_prompt)
                
                if 20 <= len(refined_text.split()) <= 40:
                    return refined_text
                
                # Update text for next iteration or return if refined_text is valid
                if refined_text:
                    text = refined_text
            
            # Return the last generated text if it is still not within the range
            return text

        # Generate positive summary with a word constraint   
        prompt_list = [
            "Generate a concise positive summary of around 20-40 words for the following text: ",
            "Generate a concise negative summary of around 20-40 words for the following text: ",
            "Generate a concise neutral summary of around 20-40 words for the following text: "

            ]
        
        output_list = []
        for prompt in prompt_list:
            temp_prompt = prompt + f"{input_text}"
            output = invoke_with_retry(temp_prompt)
            if len(output.split()) >= 40 :
                output_refined = adjust_length_with_reinvoke(output, temp_prompt)
            
            if len(output.split()) < 40:
                output_list.append(output)
            
            else:
                output_list.append(output_refined)
        
        output_positive = output_list[0]
        output_negative = output_list[1]
        output_neutral = output_list[2]
        
        return output_positive, output_negative, output_neutral
            
    def summarization(self, input_text):
        # Generate positive and negative summaries
        output_positive, output_negative, output_neutral = self.get_summary(input_text)
        
        return output_positive, output_negative, output_neutral



