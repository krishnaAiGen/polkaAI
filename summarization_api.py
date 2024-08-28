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
                if 150 <= word_count <= 200:
                    return text
                
                # If the text is too long, reinvoke the LLM to generate within the target range
                print(f"Attempt {attempt+1}: Reinvoking LLM for a more concise summary (current length: {word_count} words)...")
                refined_prompt = original_prompt + " Ensure the summary is between 150-200 words."
                refined_text = invoke_with_retry(refined_prompt)
                
                # Update text for next iteration or return if refined_text is valid
                if refined_text:
                    text = refined_text
            
            # Return the last generated text if it is still not within the range
            return text

        # Generate positive summary with a word constraint
        positive_prompt = (
            f"Generate a concise positive summary of around 150-200 words for the following text: '{input_text}'"
        )
        output_positive = invoke_with_retry(positive_prompt)
    
        # Check the word count and refine if it is greater than 200
        if len(output_positive.split()) > 200:
            output_positive = adjust_length_with_reinvoke(output_positive, positive_prompt)
        
        print("Positive Summary:", output_positive)
        
        # Generate negative summary with a word constraint
        negative_prompt = (
            f"Generate a concise negative summary of around 150-200 words for the following text: '{input_text}'"
        )
        output_negative = invoke_with_retry(negative_prompt)
    
        # Check the word count and refine if it is greater than 200
        if len(output_negative.split()) > 200:
            output_negative = adjust_length_with_reinvoke(output_negative, negative_prompt)
        
        print("\n\nNegative Summary:", output_negative)
        
        return output_positive, output_negative
            
    def summarization(self, input_text):
        # Generate positive and negative summaries
        output_positive, output_negative = self.get_summary(input_text)
        
        return output_positive, output_negative

    
    # def get_summary(self, input_text):  
    #     length_input = self.get_text_length(input_text)
    #     original_input_length = int(length_input * 6)
    #     print("original length", original_input_length)
    #     print(length_input)
        
    #     # Initialize the LLM with a lower temperature for concise and coherent summaries
    #     llm = Ollama(model=self.model, temperature=0.3)          
        
    #     # Function to invoke LLM with retries if output is None
    #     def invoke_with_retry(prompt, max_retries=3):
    #         retries = 0
    #         output = None
    #         while output is None and retries < max_retries:
    #             output = llm.invoke(prompt)
    #             retries += 1
    #         return output
        
    #     # Generate positive summary
    #     positive_prompt = f"Generate me a very short positive conversation summary of the following text: '{input_text}'"
    #     output_positive = invoke_with_retry(positive_prompt)
    #     print(output_positive)
        
    #     # Generate negative summary
    #     negative_prompt = f"Generate me a very short negative conversation summary of the following text: '{input_text}'"
    #     output_negative = invoke_with_retry(negative_prompt)
    #     print("\n\n", output_negative)
        
    #     return output_positive, output_negative
                
    # def summarization(self, input_text):
    #     output_positive, output_negative = self.get_summary(input_text)
        
    #     return output_positive, output_negative



