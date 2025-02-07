from langchain_ollama.llms import OllamaLLM

class InitializeModel:
    def __init__(self):
        model_list = ['phi3']
        self.llm_objects = []  # Use self to define instance variable
        
        for model in model_list:
            llm = OllamaLLM(model=model, temperature=1)    
            self.llm_objects.append(llm)  # Append to the 



        