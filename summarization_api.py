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
        llm = Ollama(model=self.model, temperature=1)          
        
        initial_prompt = f"Generate me a short positive conversation summary of following text: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        output_positive = llm.invoke(final_prompt)
        print(output_positive)
        
        
        initial_prompt = f"Generate me a short negative conversation summary of following text: "
        final_prompt = f"{initial_prompt} '{input_text}'"
        output_negative = llm.invoke(final_prompt)
        print(output_negative)
        
        # else:
        #     print("Outside 200")
        #     diff_length = original_input_length - 200
        #     total_length = int(30 + ( 0.05 *diff_length))
        #     print(total_length)
            
        #     initial_prompt = f"Generate me a positive conversation summary of following text in {total_length} words: "
        #     # initial_prompt = f"Generate me a positive conversation summary of following text"
        #     final_prompt = f"{initial_prompt} '{input_text}'"
        #     output_positive = llm.invoke(final_prompt)
            
        #     output_positive_length = len(output_positive.split(' '))
        #     while True:
        #         if output_positive_length > total_length:
        #             print("generating desired words text")
        #             initial_prompt = f"You generated summary of {output_positive_length} words but I need within {total_length} words"
        #             print(initial_prompt)
        #             # initial_prompt = f"Generate me a positive conversation summary of following text"
        #             final_prompt = f"{initial_prompt} '{input_text}'"
        #             output_positive = llm.invoke(final_prompt)
        #             output_positive_length = len(output_positive.split(' '))
        #             print(output_positive_length)
                    

        #     initial_prompt = f"Generate me a negative conversation summary of following text in {total_length} words: "
        #     # initial_prompt = f"Generate me a negative conversation summary of following text"
        #     final_prompt = f"{initial_prompt} '{input_text}'"
        #     output_negative = llm.invoke(final_prompt)
            
        #     output_negative_length = len(output_negative.split(' '))
        #     while True:
        #         if output_negative_length > total_length:
        #             print("generating desired words text")
        #             initial_prompt = f"You generated summary of {output_positive_length} words but I need within {total_length} words"
        #             final_prompt = f"{initial_prompt} '{input_text}'"
        #             output_negative = llm.invoke(final_prompt)
        #             output_negative_length = len(output_negative.split(' '))
        #             print(output_negative_length)

                    
    
        return output_positive, output_negative
                
    def summarization(self, input_text):
        output_positive, output_negative = self.get_summary(input_text)
        
        return output_positive, output_negative




