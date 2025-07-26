import tiktoken
from constants import CHUNK_SIZE, ENCODING_NAME


def get_encoding():
    return tiktoken.get_encoding(ENCODING_NAME)


def count_tokens(text, encoding=None):
    if encoding is None:
        encoding = get_encoding()
    return len(encoding.encode(text))


def tokenize_text(text, encoding=None):
    """Tokenize text and return list of token chunks."""
    if encoding is None:
        encoding = get_encoding()

    tokens = encoding.encode(text)
    chunks = []

    for i in range(0, len(tokens), CHUNK_SIZE):
        chunk_tokens = tokens[i:i + CHUNK_SIZE]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks