from langchain_ollama.llms import OllamaLLM
import re
from openai_summ import revise_text, get_summ

class Summarization:
    def __init__(self, llm, summ_model):
        self.llm = llm.llm_objects
        self.summ_model = summ_model
    
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
    
    def get_sentiment_consensus(self, content):
        sentiment_dict = {
            'positive': 0,
            'negative': 0,
            'neutral' : 0
            }
        
        for model in self.llm:
            print(content)
            output = model.invoke("tell me whether this text is positive, negative or neutral and output should only contain either positive or negative or neutral" + content)
            output_lower = output.lower()
            match = re.search(r'\b(positive|negative|neutral)\b', output_lower)
            
            if match:
                sentiment = match.group(0)
            else:
                sentiment = 'neutral'
            
            sentiment_dict[sentiment] = sentiment_dict[sentiment] + 1 
        
        max_key = max(sentiment_dict, key=sentiment_dict.get)
        
        return max_key
 
            
    def get_positive_negative_dict(self, grouped_id):
        positive_string = ''
        negative_string = ''
        neutral_string = ''
        
        positive_counter = 0
        negative_counter = 0
        neutral_count = 0
        
        
        # llm = Ollama(model=self.model, temperature=0.3)          

        for id1, content in grouped_id.items():
            sentiment = self.get_sentiment_consensus(content)
        
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
        # Generate positive summary with a word constraint   
        prompt_list = {
            "positive" : "Generate a concise positive summarized text of around 50-80 words for the following discussion and don't give word count and unnecessary information in the output: ",
            "negative": "Generate a concise negative summarized text of around 50-80 words for the following discussion and don't give word count and unnecessary information in the output:  ",
            "neutral": "Generate a concise neutral summarized text of around 50-80 words for the following discussion and don't give word count and unnecessary information in the output:"

            }
        
        final_prompt = prompt_list[summary_type] + input_text
        
        output = get_summ(final_prompt)

        return output
    
    def refine_output(self, output_list, positive_negative_dict):
        output_list_refined = []
        
        for index in range(len(output_list)):
            if positive_negative_dict[index]['type'] == 'positive':
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling optimistic. "
            
            elif positive_negative_dict[index]['type'] == 'negative':
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling against it. "
            
            else:
                prefix = f"Overall {int(positive_negative_dict[index]['percent']* 100)} % of users are feeling neutral. "
            
            if len(output_list[index]) == 0:
                final_text = output_list[index]
            else:
                final_text = prefix + output_list[index]
            
            # final_text = revise_text(final_text)
            output_list_refined.append(final_text)
        
        
        return output_list_refined
  
    def summarization(self, input_text):
        print("I am inside summarization")
        # Generate positive and negative summaries
        grouped_id = self.get_group_id(input_text)
        positive_negative_dict = self.get_positive_negative_dict(grouped_id)
        # print(positive_negative_dict)
        
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
