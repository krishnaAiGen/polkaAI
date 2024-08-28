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
        print("original length", original_input_length)
        print(length_input)
        
        # Initialize the LLM with a lower temperature for concise and coherent summaries
        llm = Ollama(model=self.model, temperature=0.3)          
        
        # Function to invoke LLM with retries if output is None
        def invoke_with_retry(prompt, max_retries=3):
            retries = 0
            output = None
            while output is None and retries < max_retries:
                output = llm.invoke(prompt)
                retries += 1
            return output
        
        # Generate positive summary
        positive_prompt = f"Generate me a very short positive conversation summary of the following text: '{input_text}'"
        output_positive = invoke_with_retry(positive_prompt)
        print(output_positive)
        
        # Generate negative summary
        negative_prompt = f"Generate me a very short negative conversation summary of the following text: '{input_text}'"
        output_negative = invoke_with_retry(negative_prompt)
        print("\n\n", output_negative)
        
        return output_positive, output_negative
                
    def summarization(self, input_text):
        output_positive, output_negative = self.get_summary(input_text)
        
        return output_positive, output_negative




