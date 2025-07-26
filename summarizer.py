import sys
from openai import OpenAI
from tqdm import tqdm

from constants import MODEL_NAME, TEMPERATURE, MAX_TOKENS
from file_io import write_debug_summary


def _build_prompt(summary_prompt, previous_summary, current_chunk):
    return summary_prompt.replace(
        "{previous_summary or seed_description}", previous_summary
    ).replace(
        "{current_chunk}", current_chunk
    )


def _summarize_chunk(client, prompt):
    """Call OpenAI API to summarize a single chunk."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n❌ Error calling OpenAI API: {e}")
        sys.exit(1)


def process_chunks(chunks, seed_prompt, summary_prompt, debug=False):
    """Process all chunks and return the final summary."""
    client = OpenAI()

    # Initialize with seed prompt as the first "summary"
    previous_summary = seed_prompt

    for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
        full_prompt = _build_prompt(summary_prompt, previous_summary, chunk)
        previous_summary = _summarize_chunk(client, full_prompt)

        if debug:
            debug_filename = write_debug_summary(previous_summary, i + 1)
            if debug_filename:
                tqdm.write(f"✓ Saved intermediate summary to {debug_filename}")

    return previous_summary
