from anthropic import Anthropic
from api_keys import CLAUDE_API_KEY

client = Anthropic(
    api_key=CLAUDE_API_KEY,
)


def generate_blurb(name, documents):
    input_content = []
    for i, doc in enumerate(documents):
        input_content.append({
            "type": "text",
            "text": "DOCUMENT {}\n{}".format(i, doc)
        })
    input_content.append({
        "type": "text",
        "text": "Read the documents above, and in the context of the book "
        "\"The Power Broker\" by Robert Caro, answer the following question: "
        "Who is {}? Write one paragraph in the style of a "
        "biography blurb".format(name)
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
        raise KeyError

