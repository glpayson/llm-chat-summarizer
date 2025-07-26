import sys
from constants import DEFAULT_SUMMARY_PROMPT_FILE


def read_input_files(args):
    try:
        # Read the main chat file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            chat_content = f.read()
        print(f"✓ Read chat file: {len(chat_content)} characters")

        # Read seed prompt
        with open(args.seed_prompt, 'r', encoding='utf-8') as f:
            seed_prompt = f.read()
        print(f"✓ Read seed prompt: {len(seed_prompt)} characters")

        # Read summary prompt
        if args.summary_prompt:
            with open(args.summary_prompt, 'r', encoding='utf-8') as f:
                summary_prompt = f.read()
            print(f"✓ Read custom summary prompt: {len(summary_prompt)} characters")
        else:   # Use default summary prompt from file
            try:
                with open(DEFAULT_SUMMARY_PROMPT_FILE, 'r', encoding='utf-8') as f:
                    summary_prompt = f.read()
                print(f"✓ Read default summary prompt: {len(summary_prompt)} characters")
            except FileNotFoundError:
                print(f"Error: Default summary prompt file '{DEFAULT_SUMMARY_PROMPT_FILE}' not found")
                sys.exit(1)

        return chat_content, seed_prompt, summary_prompt

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)


def write_final_summary(summary, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"✓ Final summary saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error saving final summary: {e}")
        sys.exit(1)


def write_debug_summary(summary, chunk_number):
    """Write an intermediate summary for debugging."""
    debug_filename = f"summary_chunk_{chunk_number:03d}.txt"
    try:
        with open(debug_filename, 'w', encoding='utf-8') as f:
            f.write(f"Summary after processing chunk {chunk_number}:\n\n")
            f.write(summary)
        return debug_filename
    except Exception as e:
        print(f"❌ Error saving debug summary: {e}")
        return None
