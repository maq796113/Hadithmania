import re


def split_text_into_chunks(text, limit):
    chunks = []
    current_chunk = ""
    split_pattern = re.compile(r'(?<!b)\. ')

    for sentence in split_pattern.split(text):
        if len(current_chunk) + len(sentence) + 2 <= limit:  # +2 for the period and space
            current_chunk += sentence + '. '
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            if sentence != split_pattern.split(text)[-1]:
                current_chunk = sentence + '. '
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
