from langchain_community.llms import Ollama

class Summarization:
    def __init__(self, model):
        self.model = model
    
    def get_text_length(self, input_text):
        splited_text = input_text.split(' ')
        return int(len(splited_text)/3)      
    
    def get_summary(self, input_text):  
        length_input = self.get_text_length(input_text)
        llm = Ollama(model=self.model, temperature=1)          
        initial_prompt = f"Generate me a positive conversation summary of following text in {length_input} words: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        
        output_positive = llm.invoke(final_prompt)
        
        initial_prompt = f"Generate me a negative conversation summary of following text in {length_input} words: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        
        output_negative = llm.invoke(final_prompt)
    
        return output_positive, output_negative
                
    def summarization(self, input_text):
        output_positive, output_negative = self.get_summary(input_text)
        
        return output_positive, output_negative
