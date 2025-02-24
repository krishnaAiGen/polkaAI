import re
import time
import ast
from openai import OpenAI

from dotenv import load_dotenv
import os
load_dotenv()


class DeepSeek:
    def __init__(self, deepseek_url, deepseek_key, openai_key):
        self.deepseek_client = OpenAI(
            base_url=deepseek_url,
            api_key=deepseek_key
        )
        self.openai_client = OpenAI(api_key=openai_key)

        self.max_attempts = 5
        self.retry_delay = 1  # 1 second delay between retries
        
    def _try_deepseek(self, input_text):
        """Attempt to get response from DeepSeek API"""
        for attempt in range(self.max_attempts):
            print(f"\033[92mdeepseek_attempt {attempt}\033[0m")

            try:
                response = self.deepseek_client.chat.completions.create(
                    model="n/a",
                    messages=[
                        {"role": "system", "content": """
                         You are a summarization expert for crypto related comments. You will recieve content in following json strcture:
                         [
                              {
                                "network": "string",
                                "postId": "string",
                                "postContent": "string"
                              },
                              {
                                "content": "string",
                                "id": "integer",
                                "username": "string"
                              },
                              {
                                "content": "string",
                                "id": "integer",
                                "username": "string"
                              }
                              
                            ]
                         
                         In the input json, the  "postConetnt"" is a content of a post and  "content" is a comments
                         on that post.
                         
                         Instructions:
                        Classify each comment as positive, neutral, or negative.
                        Calculate sentiment percentages based on total comments.
                        Summarize key themes from each sentiment category.
                        Edge Cases: If all comments fall into one category, summarize accordingly. Avoid redundancy.
                        Example Output:
                        json
                        Copy
                        Edit
                        {
                          "summary_positive": "Overall, 35% of users are optimistic. They appreciate Polkassembly's innovations and future plans.",
                          "summary_neutral": "Overall, 57% of users are neutral. Discussions focus on budget adjustments, stability, and UI improvements.",
                          "sumary_negative": "Overall, 7% of users are against it. Concerns include UI issues, stability, and potential loss of effectiveness."
                        }
                        Follow the JSON format exactly. No extra text or explanations. Each summarized statemnt in the output should be 50-80 words long.

                         """},
                        {"role": "user", "content": input_text}
                    ]
                )

                
                for choice in response.choices:
                    content = choice.message.content
                    json_match = re.search(r'\{[^{}]*\}', content)
                    if json_match:
                        try:
                            result = ast.literal_eval(json_match.group())
                            return result
                        except (ValueError, KeyError, SyntaxError):
                            continue
                
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise RuntimeError(f"DeepSeek API failed after {self.max_attempts} attempts: {str(e)}")
        
        return None  # If no valid JSON found after all attempts
    
    def _try_openai(self, input_text):
        """Fallback to OpenAI API"""
        for attempt in range(self.max_attempts):
            try:
                print(f"openai_attempt {attempt}")
                response = self.openai_client.chat.completions.create(
                    model="o1-preview",
                    messages=[
                        {"role": "system", "content": """
                         You are a summarization expert for crypto-related comments. You will receive content in the following JSON structure:
                         [
                              {
                                "network": "string",
                                "postId": "string",
                                "postContent": "string"
                              },
                              {
                                "content": "string",
                                "id": "integer",
                                "username": "string"
                              },
                              {
                                "content": "string",
                                "id": "integer",
                                "username": "string"
                              }
                            ]
                         
                         In the input JSON, the "postContent" is the content of a post and "content" represents comments
                         on that post.
                         
                         Instructions:
                        - Classify each comment as positive, neutral, or negative.
                        - Calculate sentiment percentages based on total comments.
                        - Summarize key themes from each sentiment category.
                        - Edge Cases: If all comments fall into one category, summarize accordingly. Avoid redundancy.
                        
                        Example Output:
                        {
                          "summary_positive": "Overall, 35% of users are optimistic. They appreciate Polkassembly's innovations and future plans.",
                          "summary_neutral": "Overall, 57% of users are neutral. Discussions focus on budget adjustments, stability, and UI improvements.",
                          "summary_negative": "Overall, 7% of users are against it. Concerns include UI issues, stability, and potential loss of effectiveness."
                        }
                        
                        Follow the JSON format exactly. No extra text or explanations. Each summarized statement in the output should be 50-80 words long.
                         """},
                        {"role": "user", "content": input_text}
                    ]
                )
                
                for choice in response.choices:
                    content = choice.message.content
                    json_match = re.search(r'\{[^{}]*\}', content)
                    if json_match:
                        try:
                            result = ast.literal_eval(json_match.group())
                            return result
                        except (ValueError, KeyError, SyntaxError):
                            continue
                
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise RuntimeError(f"OpenAI API error after {self.max_attempts} attempts: {str(e)}")
        
        return None  # If no valid JSON found after all attempts
    
    def get_summary(self, input_text):
        """Main method to get sentiment score, trying DeepSeek first then falling back to OpenAI"""
        try:
            # Try DeepSeek first
            result = self._try_deepseek(input_text)
            if result is not None:
                return result['summary_positive'], result['summary_neutral'], result['summary_negative']
            else:
                # If DeepSeek fails, try OpenAI
                result = self._try_openai(input_text)
                
                return result['summary_positive'], result['summary_neutral'], result['summary_negative']

            return None
            
        except Exception as e:
            raise RuntimeError(f"Both APIs failed: {str(e)}")
            

