from anthropic import Anthropic
from api_keys import CLAUDE_API_KEY
from index import parse_index
from pages import get_pages
from prompt import get_prompt, PromptSize

client = Anthropic(
    api_key=CLAUDE_API_KEY,
)

INDEX = parse_index()
prompt_size_to_max_tokens = {
    PromptSize.SMALL : 1024,
    PromptSize.MEDIUM : 2048,
    PromptSize.LARGE : 4096,
}

def get_bio(person):
    documents = get_pages(person["pages"], expand=True)
    name = person["first"] + " " + person["last"]
    bio = claude_generate_bio(name, documents, PromptSize.MEDIUM)
    return bio


def claude_generate_bio(name, documents, size: PromptSize):
    input_content = []
    prompt = get_prompt(name, documents, size)
    print(prompt)
    input_content = [{
        "type": "text",
        "text": prompt
    }]
    message = client.messages.create(
        max_tokens=prompt_size_to_max_tokens[size],
        messages=[
            {
                "role": "user",
                "content": input_content
            }
        ],
        model="claude-3-opus-20240229",
    )
    if len(message.content) > 0:
        return message.content[0].text
    else:
        raise

