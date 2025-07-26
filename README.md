# LLM Chat Summarizer

A Python tool that uses rolling summarization to condense long chat conversations while preserving narrative flow, emotional context, and key information.

## Features

- **Rolling Summarization**: Processes conversations in chunks, with each summary building on the previous one
- **Preserves Context**: Maintains emotional journey, key decisions, and important relationships
- **Configurable**: Customizable prompts and chunk sizes
- **Debug Mode**: Save intermediate summaries to track the summarization process
- **Progress Tracking**: Visual progress bar for long conversations

## Installation

### Prerequisites

- Python 3.11+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-chat-summarizer.git
cd llm-chat-summarizer
```

2. Install dependencies using uv (recommended):
```bash
pip install uv
uv sync
```

Or using pip with pyproject.toml:
```bash
pip install -e .
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Basic Usage

```bash
uv run python main.py chat_export.md --seed-prompt seed_prompt.txt
```

### With Custom Summary Prompt

```bash
uv run python main.py chat_export.md --seed-prompt seed_prompt.txt --summary-prompt custom_prompt.txt
```

### Testing with Limited Chunks

```bash
uv run python main.py chat_export.md --seed-prompt seed_prompt.txt --max-chunks 5 --debug
```

### Full Command Line Options

- `input_file`: Path to the markdown file containing the chat conversation (required)
- `--seed-prompt`: Path to the seed prompt file (required)
- `--summary-prompt`: Path to custom summarization prompt file (optional)
- `--output`: Output file path (default: final_summary.txt)
- `--max-chunks`: Process only first N chunks (useful for testing)
- `--debug`: Save intermediate summaries for each chunk

## How It Works

1. **Tokenization**: The chat is split into chunks of ~15,000 tokens each
2. **Rolling Summarization**: 
   - First chunk is summarized using the seed prompt as context
   - Each subsequent chunk is summarized using the previous summary as context
   - This maintains narrative continuity throughout the conversation
3. **Final Output**: The last summary contains the condensed version of the entire conversation

## Prompt Files

### Seed Prompt
The seed prompt (`seed_prompt.txt`) provides initial context about the conversation. It should include:
- Key participants and their roles
- Overall situation/context
- Important background information

### Summary Prompt
The summary prompt (default: `default_summary_prompt.txt`) instructs the LLM on how to summarize. It can be customized to focus on specific aspects like:
- Emotional progression
- Key decisions
- Action items
- Relationship dynamics

## Example

```bash
# Export your chat from ChatGPT/Claude/etc as markdown
# Create a seed prompt with context
echo "This conversation is between a software developer and an AI assistant..." > seed_prompt.txt

# Run the summarizer
uv run python main.py my_chat_export.md --seed-prompt seed_prompt.txt --debug

# Review the final summary
cat final_summary.txt
```

## Technical Details

- Uses GPT-4o for summarization
- Token counting via tiktoken
- Chunk size: 15,000 tokens (configurable in constants.py)
- Output length: ~1000-1200 words per summary

## Project Structure

```
llm-chat-summarizer/
├── main.py              # Main orchestration
├── constants.py         # Configuration constants
├── file_io.py          # File reading/writing operations
├── tokenizer.py        # Text chunking and tokenization
├── summarizer.py       # OpenAI API calls and summarization logic
├── default_summary_prompt.txt  # Default summarization instructions
└── README.md
```

## License

MIT