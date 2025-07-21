from enum import Enum
from openai import OpenAI
from config import OPENAI_API_KEY
import lmstudio as lms
import semchunk
import tiktoken
import sys
import os

class Mode(Enum):
    LOCAL = "local"
    OPENAI = "openai"

LOCAL_SERVER_API_HOST = "192.168.1.3:1234"
LOCAL_MODEL_NAME = "google/gemma-3-27b"

MAX_CHUNK_SIZE = 2048
MIN_CHUNK_SIZE = 16
COMPRESSION_FACTOR = 0.04

class LLMClient:
    def __init__(self, mode):
        self.mode = mode
        if mode == Mode.LOCAL:
            self.client = lms.get_default_client(LOCAL_SERVER_API_HOST)
            self.model = self.client.llm.load_new_instance(LOCAL_MODEL_NAME, config={
                "contextLength": 8192,
            })
        elif mode == Mode.OPENAI:
            self.client = OpenAI(api_key=OPENAI_API_KEY)

    def respond(self, system_prompt, user_prompt, temperature=0.2):
        if self.mode == Mode.LOCAL:
            chat = lms.Chat(initial_prompt=system_prompt)
            chat.add_user_message(user_prompt)
            return self.model.respond(chat, config={
                "temperature": temperature,
            }).content.strip()
        elif self.mode == Mode.OPENAI:
            response = self.client.responses.create(
                model="gpt-4.1",
                instructions=system_prompt,
                input=user_prompt,
                temperature=0.2,
            )
            return response.output_text

def get_chunks(text, encoding):
    chunker = semchunk.chunkerify('gpt-4', MAX_CHUNK_SIZE)
    chunks = chunker(text)
    chunks = [c for c in chunks if len(encoding.encode(c)) >= MIN_CHUNK_SIZE]
    return chunks

def get_mode(raw_mode):
    if raw_mode.lower() == Mode.LOCAL.value:
        return Mode.LOCAL
    elif raw_mode.lower() == Mode.OPENAI.value:
        return Mode.OPENAI
    else:
        raise ValueError("Invalid mode. Use 'LOCAL' or 'OPENAI'.")

def get_tmp_dir(chapter_filename):
    chapter_name = os.path.basename(chapter_filename).split('.')[0]
    tmp_dir_name = f"{chapter_name}_summary_tmp"
    if not os.path.exists(tmp_dir_name):
        os.makedirs(tmp_dir_name)
    return tmp_dir_name

def load_existing_summaries(tmp_dir_name):
    summaries = []
    i = 0
    while os.path.exists(f"{tmp_dir_name}/summary_chunk_{i}.txt"):
        with open(f"{tmp_dir_name}/summary_chunk_{i}.txt", "r") as f:
            summaries.append(f.read())
        i += 1
    return summaries

def summarize_chunks(client, chunks, encoding, tmp_dir_name):
    summaries = []
    for i, chunk in enumerate(chunks):
        chunk_size = len(encoding.encode(chunk))
        summary_token_count = int(chunk_size * COMPRESSION_FACTOR)
        print(f"Chunk {i} of ({len(chunks)-1}): {chunk_size} tokens")
        print(f"    Summary size: {summary_token_count} tokens")
        print(f"    Content: {repr(chunk[:60] + '...' if len(chunk) > 60 else chunk)}")
        
        prompt = open("prompts/single_excerpt_summary_prompt.txt", "r").read()
        prompt = prompt.format(word_count=summary_token_count)
        print(f"    Prompt: {repr(prompt[:60] + '...' if len(prompt) > 60 else prompt)}")
        print()

        response = client.respond(
            system_prompt=prompt,
            user_prompt=chunk,
        )
        print(f"    Response: {response}")
        print()

        summaries.append(response)

        with open(f"{tmp_dir_name}/summary_chunk_{i}.txt", "w") as f:
            f.write(response)
    return summaries

def merge_summaries(client, summaries, word_count):
    prompt = open("prompts/merge_summary_prompt.txt", "r").read()
    prompt = prompt.format(word_count=word_count)
    print(f"Merge prompt: {repr(prompt[:60] + '...' if len(prompt) > 60 else prompt)}")

    return client.respond(
        system_prompt=prompt,
        user_prompt="\n\n".join(summaries),
    )

def style_summary(client, text):
    prompt = open("prompts/style_prompt.txt", "r").read()
    print(f"Style prompt: {repr(prompt[:60] + '...' if len(prompt) > 60 else prompt)}")

    return client.respond(
        system_prompt=prompt,
        user_prompt=text,
    )

def save_final_summary(final_summary, tmp_dir_name):
    with open(f"{tmp_dir_name}/final_summary.txt", "w") as f:
        f.write(final_summary)

def summarize_chapter(client, chapter_filename):
    tmp_dir_name = get_tmp_dir(chapter_filename)
    chapter_text = open(chapter_filename, "r").read()
    encoding = tiktoken.encoding_for_model('gpt-4')
    chunks = get_chunks(chapter_text, encoding)

    print(f"Filename: {chapter_filename}")
    print(f"Number of tokens: {len(encoding.encode(chapter_text))}")
    print(f"Number of chunks: {len(chunks)}")
    print()

    summaries = []
    if os.path.exists(tmp_dir_name):
        summaries = load_existing_summaries(tmp_dir_name)

    if len(summaries) > 0:
        print(f"Found {len(summaries)} existing summaries in {tmp_dir_name}. Continuing from there.")
    else:
        summaries = summarize_chunks(client, chunks, encoding, tmp_dir_name)
    print()

    word_count = int(len(encoding.encode(chapter_text)) * COMPRESSION_FACTOR)
    merged_summary = merge_summaries(client, summaries, word_count)
    final_summary = style_summary(client, merged_summary)

    print(f"Final summary: {final_summary}")
    save_final_summary(final_summary, tmp_dir_name)

if __name__ == "__main__":
    chapter_filename = sys.argv[1]
    raw_mode = sys.argv[2]
    MODE = get_mode(raw_mode)
    client = LLMClient(MODE)
    summarize_chapter(client, chapter_filename)