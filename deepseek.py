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
        self.timeout = 120  # 60 second timeout for API calls
        
    def _validate_word_count(self, text):
        """Validate if the text is between 50-80 words"""
        if not text:
            return False
        words = text.split()
        return 50 <= len(words) <= 80

    def _extract_percentage(self, text):
        """Extract percentage from summary text"""
        if not text:
            return 0
        match = re.search(r'(\d+)%', text)
        return int(match.group(1)) if match else 0

    def _process_summaries(self, result):
        """Process summaries to handle 0% cases and validate word counts"""
        if not result:
            return None
            
        # Extract summaries and their percentages
        summaries = {
            'summary_positive': result.get('summary_positive', ''),
            'summary_negative': result.get('summary_negative', ''),
            'summary_neutral': result.get('summary_neutral', '')
        }
        
        # Check percentages and clear summaries with 0%
        for key in summaries:
            percentage = self._extract_percentage(summaries[key])
            if percentage == 0:
                summaries[key] = ''
        
        # Validate word counts for non-empty summaries
        if not all(self._validate_word_count(summary) for summary in summaries.values() if summary):
            return None
            
        return summaries

    def _validate_summary(self, result):
        """Validate if all summaries in the result are within word limits"""
        if not result:
            return False
            
        processed = self._process_summaries(result)
        return processed is not None

    def _get_retry_prompt(self, input_text):
        """Get a more specific prompt emphasizing word count requirements"""
        return f"""Please analyze this content and provide summaries that are STRICTLY between 50-80 words for each sentiment category. For any sentiment category that has 0% representation, provide an empty string instead of a summary. Current input: {input_text}
        
        Your response MUST follow this format and word count requirement:
        {{
          "summary_positive": "(50-80 words summary for positive sentiment, or empty string if 0%)",
          "summary_neutral": "(50-80 words summary for neutral sentiment, or empty string if 0%)",
          "summary_negative": "(50-80 words summary for negative sentiment, or empty string if 0%)"
        }}"""

    def _try_deepseek(self, input_text, is_retry=False):
        """Attempt to get response from DeepSeek API with timeout"""
        for attempt in range(self.max_attempts):
            print(f"\033[92mdeepseek_attempt {attempt}\033[0m")

            try:
                messages = [
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
                    IMPORTANT: Each summary MUST be between 50-80 words - no exceptions.
                    IMPORTANT: For any sentiment category with 0% representation, provide an empty string instead of a summary.
                    Edge Cases: If all comments fall into one category, summarize accordingly. Avoid redundancy.
                    Example Output:
                    {
                      "summary_positive": "Overall, 35% of users are optimistic. They appreciate Polkassembly's innovations and future plans.",
                      "summary_neutral": "",
                      "summary_negative": "Overall, 65% of users are against it. Concerns include UI issues, stability, and potential loss of effectiveness."
                    }
                    Follow the JSON format exactly. No extra text or explanations. Each non-empty summary MUST be 50-80 words."""}
                ]
                
                if is_retry:
                    messages.append({"role": "user", "content": self._get_retry_prompt(input_text)})
                else:
                    messages.append({"role": "user", "content": input_text})

                response = self.deepseek_client.chat.completions.create(
                    model="n/a",
                    messages=messages,
                    timeout=self.timeout
                )

                for choice in response.choices:
                    content = choice.message.content
                    json_match = re.search(r'\{[^{}]*\}', content)
                    if json_match:
                        try:
                            result = ast.literal_eval(json_match.group())
                            processed_result = self._process_summaries(result)
                            if processed_result:
                                return processed_result
                            elif not is_retry:
                                # If validation fails and this isn't already a retry, try again with specific prompt
                                return self._try_deepseek(input_text, is_retry=True)
                        except (ValueError, KeyError, SyntaxError):
                            continue
                
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                print(f"DeepSeek attempt {attempt} failed: {str(e)}")
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise RuntimeError(f"DeepSeek API failed after {self.max_attempts} attempts: {str(e)}")
        
        return None

    def _try_openai(self, input_text, is_retry=False):
        """Fallback to OpenAI API with timeout"""
        for attempt in range(self.max_attempts):
            try:
                print(f"openai_attempt {attempt}")
                
                messages = [
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
                    - IMPORTANT: Each summary MUST be between 50-80 words - no exceptions.
                    - IMPORTANT: For any sentiment category with 0% representation, provide an empty string instead of a summary.
                    - Edge Cases: If all comments fall into one category, summarize accordingly. Avoid redundancy.
                    
                    Example Output:
                    {
                      "summary_positive": "Overall, 35% of users are optimistic. They appreciate Polkassembly's innovations and future plans.",
                      "summary_neutral": "",
                      "summary_negative": "Overall, 65% of users are against it. Concerns include UI issues, stability, and potential loss of effectiveness."
                    }
                    
                    Follow the JSON format exactly. No extra text or explanations. Each non-empty summary MUST be 50-80 words."""}
                ]
                
                if is_retry:
                    messages.append({"role": "user", "content": self._get_retry_prompt(input_text)})
                else:
                    messages.append({"role": "user", "content": input_text})

                response = self.openai_client.chat.completions.create(
                    model="o1-preview",
                    messages=messages,
                    timeout=self.timeout
                )
                
                for choice in response.choices:
                    content = choice.message.content
                    json_match = re.search(r'\{[^{}]*\}', content)
                    if json_match:
                        try:
                            result = ast.literal_eval(json_match.group())
                            processed_result = self._process_summaries(result)
                            if processed_result:
                                return processed_result
                            elif not is_retry:
                                # If validation fails and this isn't already a retry, try again with specific prompt
                                return self._try_openai(input_text, is_retry=True)
                        except (ValueError, KeyError, SyntaxError):
                            continue
                
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                print(f"OpenAI attempt {attempt} failed: {str(e)}")
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise RuntimeError(f"OpenAI API error after {self.max_attempts} attempts: {str(e)}")
        
        return None
    
    def get_summary(self, input_text):
        """Main method to get sentiment score, trying DeepSeek first then falling back to OpenAI"""
        try:
            # Try DeepSeek first
            result = self._try_deepseek(input_text)
            if result is not None:
                return result.get('summary_positive', ''), result.get('summary_negative', ''), result.get('summary_neutral', '')
            else:
                # If DeepSeek fails, try OpenAI
                result = self._try_openai(input_text)
                if result is not None:
                    return result.get('summary_positive', ''), result.get('summary_negative', ''), result.get('summary_neutral', '')

            return None, None, None
            
        except Exception as e:
            print(f"All API attempts failed: {str(e)}")
            raise RuntimeError(f"Both APIs failed: {str(e)}")