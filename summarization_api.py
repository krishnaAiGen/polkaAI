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
        llm = Ollama(model=self.model, temperature=0.3)          
        
        initial_prompt = f"Generate me a very short positive conversation summary of following text: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        output_positive = llm.invoke(final_prompt)
        print(output_positive)
        
        if output_positive is None:
            while output_positive is None:
                initial_prompt = f"Generate me a very short positive conversation summary of following text: "
                final_prompt = f"{initial_prompt} '{input_text}'"
                output_positive = llm.invoke(final_prompt)
                
        
        initial_prompt = f"Generate me a very short negative conversation summary of following text: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        output_negative = llm.invoke(final_prompt)
        print("\n\n", output_negative)
             
        if output_negative is None:
            while output_negative is None:
                initial_prompt = f"Generate me a very short negative conversation summary of following text: "
                final_prompt = f"{initial_prompt} '{input_text}'"
                output_negative = llm.invoke(final_prompt)
                
        
        return output_positive, output_negative
                
    def summarization(self, input_text):
        output_positive, output_negative = self.get_summary(input_text)
        
        return output_positive, output_negative




