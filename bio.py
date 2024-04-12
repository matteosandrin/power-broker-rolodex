from anthropic import Anthropic
from api_keys import CLAUDE_API_KEY
from index import parse_index
from pages import get_pages
from prompt import get_prompt, AnswerSize, answer_size_to_max_tokens, pages_to_answer_size

client = Anthropic(
    api_key=CLAUDE_API_KEY,
)

INDEX = parse_index()


def get_bio(person):
    documents = get_pages(person["pages"], expand=True)
    name = get_name(person)
    answer_size = pages_to_answer_size(person["pages"])
    bio = claude_generate_bio(name, documents, answer_size)
    return bio


def get_name(person):
    return person["first"] + " " + person["last"]


def claude_generate_bio(name, documents, size: AnswerSize):
    input_content = []
    prompt = get_prompt(name, documents, size)
    print(len(prompt.split()))
    input_content = [{
        "type": "text",
        "text": prompt
    }]
    message = client.messages.create(
        max_tokens=answer_size_to_max_tokens(size),
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


def estimate_cost(name, documents, size):
    prompt = get_prompt(name, documents, size)
    prompt_token_count = client.count_tokens(prompt)
    answer_token_count = answer_size_to_max_tokens(size)
    input_cost_mtok = 15.0  # $15 per million tokens
    output_cost_mtok = 75.0  # $75 per million tokens
    one_million = 1000000
    input_cost = prompt_token_count / one_million * input_cost_mtok
    output_cost = answer_token_count / one_million * output_cost_mtok
    return input_cost + output_cost


def estimate_total_cost():
    sorted_index = sorted(INDEX, key=lambda p: len(p["pages"]), reverse=True)
    total_cost = 0.0
    for person in sorted_index:
        documents = get_pages(person["pages"], expand=True)
        name = get_name(person)
        answer_size = pages_to_answer_size(person["pages"])
        cost = estimate_cost(documents, name, answer_size)
        print("{} {} ${:.2f}".format(person["first"], person["last"], cost))
        total_cost += cost
    print("total cost: ${:.2f}".format(total_cost))
