from anthropic import Anthropic
from api_keys import CLAUDE_API_KEY
from index import parse_index
from pages import get_pages

client = Anthropic(
    api_key=CLAUDE_API_KEY,
)

INDEX = parse_index()
PROMPT = """Read the documents above and answer the following question, 
in the context of the book "The Power Broker" by Robert Caro: 
Who is {}? Write one paragraph in the style of a biography blurb, 
highlighting how the person is relevant to history in general and to 
the the book specifically"""

def get_bio(person):
    documents = get_pages(person["pages"], expand=True)
    name = person["first"] + " " + person["last"]
    print("name:", name)
    print("document:", documents)
    bio = claude_generate_bio(name, documents)
    return bio

def claude_generate_bio(name, documents):
    input_content = []
    for i, doc in enumerate(documents):
        input_content.append({
            "type": "text",
            "text": "DOCUMENT {}\n{}".format(i, doc)
        })
    input_content.append({
        "type": "text",
        "text": PROMPT.format(name)
    })
    message = client.messages.create(
        max_tokens=1024,
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

