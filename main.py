import argparse
import os
import sys

from constants import CHUNK_SIZE, DEFAULT_OUTPUT_FILE
from file_io import read_input_files, write_final_summary
from tokenizer import get_encoding, count_tokens, tokenize_text
from summarizer import process_chunks


def _print_verification(args):
    print("\n--- Verification ---")
    print(f"Input file: {args.input_file}")
    print(f"Output will be saved to: {args.output}")
    print(f"Max chunks: {args.max_chunks if args.max_chunks else 'All'}")
    print(f"Debug mode: {'ON' if args.debug else 'OFF'}")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize long chat conversations using rolling summaries"
    )

    # Required arguments
    parser.add_argument(
        "input_file",
        help="Path to the markdown file containing the chat conversation"
    )
    parser.add_argument(
        "--seed-prompt",
        required=True,
        help="Path to the seed prompt file"
    )

    # Optional arguments
    parser.add_argument(
        "--summary-prompt",
        help="Path to custom summarization prompt file (optional override)"
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output file path for the final summary (default: {DEFAULT_OUTPUT_FILE})"
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        help="Process only first N chunks (for testing)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Save intermediate summaries for debugging"
    )

    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    chat_content, seed_prompt, summary_prompt = read_input_files(args)
    _print_verification(args)

    print("\n--- Tokenization ---")
    encoding = get_encoding()
    total_tokens = count_tokens(chat_content, encoding)
    chunks = tokenize_text(chat_content, encoding)
    chunks_to_process = chunks[:args.max_chunks] if args.max_chunks else chunks

    print(f"Total tokens in chat: {total_tokens:,}")
    print(f"Split into {len(chunks)} chunks of ~{CHUNK_SIZE:,} tokens each")

    print("\n--- Processing Chunks ---")
    print(f"Will process {len(chunks_to_process)} chunks")

    final_summary = process_chunks(
        chunks_to_process,
        seed_prompt,
        summary_prompt,
        debug=args.debug
    )

    print(f"\n✓ All chunks processed successfully.")
    print(f"Final summary length: {len(final_summary)} characters")

    write_final_summary(final_summary, args.output)



if __name__ == "__main__":
    main()