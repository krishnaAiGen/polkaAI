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
        
    def _clean_zero_percent_summaries(self, result):
        """Clean summaries that have 0% by setting them to empty strings"""
        if not result:
            return None

        # Extract summaries
        cleaned_result = {
            'summary_positive': result.get('summary_positive', ''),
            'summary_negative': result.get('summary_negative', ''),
            'summary_neutral': result.get('summary_neutral', '')
        }

        # Check each summary for 0% and clean if found
        for key in cleaned_result:
            if cleaned_result[key]:
                match = re.search(r'(\d+)%', cleaned_result[key])
                if match and int(match.group(1)) == 0:
                    cleaned_result[key] = ''

        return cleaned_result

    def _get_retry_prompt(self, input_text):
        """Get a more specific prompt emphasizing word count and percentage requirements"""
        return f"""Please analyze this content and provide summaries that are STRICTLY between 50-80 words for each sentiment category. 
        
        IMPORTANT REQUIREMENTS:
        1. Each non-empty summary MUST be between 50-80 words - no exceptions
        2. Each summary MUST start with the percentage (e.g., "Overall, X% of users...")
        3. For any sentiment category with 0% representation, provide an empty string
        4. Percentages across all categories must sum to 100%
        
        Current input: {input_text}
        
        Your response MUST follow this format:
        {{
          "summary_positive": "(50-80 words summary starting with percentage, or empty string if 0%)",
          "summary_neutral": "(50-80 words summary starting with percentage, or empty string if 0%)",
          "summary_negative": "(50-80 words summary starting with percentage, or empty string if 0%)"
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
                            # Clean any 0% summaries
                            cleaned_result = self._clean_zero_percent_summaries(result)
                            if cleaned_result:
                                return cleaned_result
                            elif not is_retry:
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
                            # Clean any 0% summaries
                            cleaned_result = self._clean_zero_percent_summaries(result)
                            if cleaned_result:
                                return cleaned_result
                            elif not is_retry:
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
        
    
# if __name__ == "__main__":
#     deepseek = DeepSeek(os.getenv("DEEPSEEK_URL"), os.getenv("DEEPSEEK_KEY"), os.getenv("OPENAI_API_KEY"))
#     deepseek.get_summary("""
#     [{'network': 'polkadot', 'postId': '1463', 'safeKey': 'n/a', 'postContent': 'Polkassembly serves as Polkadot and Kusamas primary governance hub, enabling participation in on-chain governance, delegation, proposal discussions, and community voting. This proposal seeks funding from the Polkadot Treasury to support Polkassemblys 2025 maintenance and key improvements in stability, user experience, and core features. It focuses on essential upgrades such as better UX/navigation, enhanced identity management, technical stability, and spam prevention &ndash; that will strengthen the platform&rsquo;s reliability and usability for the community What&rsquo;s our focus with this proposal? The primary focus for improvement is summarized as below: Identity - Increase stability in core flow. Simplify things for multisig account identity setup and fix issues. Add support for proxy-identity setup. RPC connectivity issues to be resolved on priority. Comments AI summary &amp; load speed improvement. Comments for Proxy and Multisig accounts revamp. Proposal creation Improve support for multi-asset proposals. Improve the proposal creation process for different tracks and scenarios. Add support for proposal creation through proxy and add support for multisig proposal creation. Add support for more wallets including Nova, Mimir, Polkagate Snap, Signet. Improve hardware wallet connectivity and functionality across all features. Redo the landing page to improve discovery and site navigation. Improve the proposal&rsquo;s detailed view layout to make information more accessible Site-idle connectivity issues and data loading. Reduce steps in proposal creation &amp; bundle decision deposit. Create a proxy management dashboard and explorer Improve UX and platform navigation. Add product walkthroughs for new user onboarding. Add support for OpenGov Nomination Pool wallet voting for all wallet types. Add comment filtering (DV, Proposer, Verified Accounts, Wallet linked). Improved Preimage management and add option to convert pre-image into proposal directly through all wallet types. Technical Improvements Upgraded to Next.js 15 with Turbopack support for improved development experience Node 20 support (compared to Node 18 in v1) Revamped Editor Better organized component architecture. Overhauled state management with Jotai Atoms. New design system Integration along with shadcn/ui component system. Overhauled project configuration with focus on security for easier open-source contribution. The API architecture has been overhauled to improve data organization and facilitate easier integration for community members. The API now offers expanded content delivery capabilities, enabling the return of data in markdown, block and HTML formats. The authentication mechanism has been updated to utilize HTTP cookies for session management, replacing the previous implementation that relied on local storage and JWT. Other technical improvements and details can be found within the proposal document. Proposal 2024 Here&rsquo;s the OG tracker ref link for our 2024 proposal and a detailed self report with features and product updates from last year&rsquo;s proposal. We worked with some amazing video designers to create a Polkassembly 2024 roundup. Users can watch the video here. Implementation Gallery Several UI/UX enhancements are actively being developed to refine navigation, improve usability, and ensure a better governance experience. Revamped Proposal Listing View Revamped Proposal Detail view Revamped Profile Page Spam Proposal Detailed View Spam Comments Delegation Dashboard &amp; Chat with delegates Bounty Dashboard Batch Voting Proxy Dashboard Analytics Dashboard Our stats reflect our continued dominance in the ecosystem Theme Product Metric Engagement on Polkassembly Number of users Last 30 days visits - 145K Total API Requests - 92M/month (Source: Cloudflare) MAU - 97k (Source: Google analytics) Number of comments Total Number of Comments on Polkassembly - 13695 Total Percentage of comments in governance on Polkadot - 82.66% (6288/7607) Total Percentage of comments in governance on Kusama - 68.2% (502/736) Number of disucussions Total Number of Discussions on Polkassembly &mdash; 2206 Total Percentage of discussions in governance on Polkadot - 93.69% (698/745) Total Percentage of discussions in governance on Kusama - 76.19% (32/42) Number of Proposals Total Percentage of proposals in governance on Polkadot - 39% Total Percentage of proposals in governance on Kusama - 20% Source: Polkassembly Firebase Views Total Views last 4 months: 750K (Polkadot Kusama) Source: Polkassembly Firebase Identity Verification Number of Judgements provided Total Percentage of judgements Polkadot - 52.22% (1216/2327) Category Amount (US$) Infrastructure &amp; Maintenance (12 months) $203,659 Development Budget $327,012 Total $530,671 The budget calculations can be found here. Refer to the full proposal document here.'}, {'id': 6448, 'username': 'TheMvp07', 'content': 'hello, it will be a great Polkadot future with all those improvements in polkassembly. I just have a suggestion around the mobile experience (safari), in the main page the News component usually takes a lot of time to show the information. Please consider this in the backlog. =)'}, {'id': 18294, 'username': 'PolkassemblyGov', 'content': '@TheMvp07 Noted. We will look into the issue and resolve it soon! Thanks for flagging.'}]

# """)
