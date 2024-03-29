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
        raise


def extract_pages(page_nums, full_text_path="./power-broker-full-text.txt"):
    full_text = open(full_text_path).read()
    page_ranges = page_nums_to_page_ranges(page_nums)
    for start, end in page_ranges:
        pass


def page_nums_to_page_ranges(page_nums):
    page_ranges = []
    i = 0
    while i < len(page_nums):
        page_ranges.append([page_nums[i], page_nums[i]+1])
        adv = 1
        for k in range(i+1, len(page_nums)):
            if page_nums[k] == page_nums[k-1] + 1:
                page_ranges[-1][1] = page_nums[k] + 1
                adv += 1
            else:
                break
        i += adv
    return [tuple(pr) for pr in page_ranges]


extract_pages([60, 61, 62, 102, 104, 107, 108, 109])
