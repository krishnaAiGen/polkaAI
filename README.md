# PolkaAI - Crypto Comment Sentiment Analyzer

A Python-based sentiment analysis tool that processes crypto-related comments and provides summarized sentiment analysis using both DeepSeek and OpenAI APIs.

## Project Structure
```
polka_ai/
├── __init__.py           # Package initialization
├── api/
│   └── sentiment.py      # Main sentiment analysis implementation
├── data/
│   └── store.py         # Data storage utilities
├── utils/               # Utility functions
│   └── __init__.py
tests/
├── __init__.py
└── test_sentiment.py    # Test cases
```

## Features

- Analyzes comments from crypto-related discussions
- Provides sentiment categorization (positive, neutral, negative)
- Generates detailed summaries for each sentiment category
- Handles edge cases with 0% representation
- Ensures summaries are concise (50-80 words)
- Fallback mechanism between DeepSeek and OpenAI APIs

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd polkaAI
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
# For development:
pip install -e ".[dev]"

# For production:
pip install .
```

4. Create a `.env` file in the project root with your API keys:
```
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=your_deepseek_api_url
OPENAI_API_KEY=your_openai_api_key
```

## Usage

```python
from polka_ai.api.sentiment import DeepSeek
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the DeepSeek class
analyzer = DeepSeek(
    deepseek_url=os.getenv('DEEPSEEK_API_URL'),
    deepseek_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_key=os.getenv('OPENAI_API_KEY')
)

# Example input format
input_data = [
    {
        "network": "polkadot",
        "postId": "123",
        "postContent": "Discussion about new features"
    },
    {
        "content": "This is amazing!",
        "id": 1,
        "username": "user1"
    },
    {
        "content": "Needs improvement",
        "id": 2,
        "username": "user2"
    }
]

# Get sentiment summaries
positive, negative, neutral = analyzer.get_summary(str(input_data))
print("Positive:", positive)
print("Negative:", negative)
print("Neutral:", neutral)
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest tests/
```

3. Format code:
```bash
black polka_ai tests
isort polka_ai tests
```

4. Check code quality:
```bash
flake8 polka_ai tests
```

## Response Format

The tool provides three types of summaries:
- Positive sentiment summary (50-80 words or empty if 0%)
- Negative sentiment summary (50-80 words or empty if 0%)
- Neutral sentiment summary (50-80 words or empty if 0%)

Each non-empty summary includes:
- Percentage of comments in that category
- Key themes and patterns
- Main points from the comments

## Error Handling

- Automatic retries on API failures
- Fallback to OpenAI if DeepSeek fails
- Timeout handling for API calls
- Validation of response formats and word counts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.