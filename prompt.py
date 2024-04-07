from enum import Enum


class PromptSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


INITIAL_PROMPT = """
I'm going to give you a series of documents. Read the documents carefully, 
because I'm going to ask you a question about them. Here are the documents:
"""

DOCS_PROMPT = """
<documents>
{docs}
</documents>
"""

QUOTE_PROMPT = """
First, find the quotes from the document that are most relevant to answering the
question, and then print them in numbered order in <quotes></quotes> tags.
Quotes should be relatively short. If there are no relevant quotes, write "No
relevant quotes" instead.
"""

QUESTION_PROMPT = """
Then, answer the question in <answer></answer> tags. Do not include or reference
quoted content verbatim in the answer. Don't say "According to Quote [1]" when
answering. Don't explain what the book "The Power Broker" is. {style}

If the question cannot be answered by the document, say so.

Here is the question: Who is {name}?
"""

STYLE_PROMPT_SM = """The answer should be one paragraph in the style of a
short biography, highlighting how the person is relevant to the the book "The
Power Broker" by Robert Caro specifically, and to history in general.
"""

STYLE_PROMPT_MD = """The answer should be three paragraphs long and in the
style of a short biography, highlighting how the person is relevant to the the
book "The Power Broker" by Robert Caro specifically, and to history in general.
The first paragraph should be about how the person is relevant to the book. The
second paragraph should go deeper on the relationship between the person and
Robert Moses. The third paragraph should explain how the person is relevant to
history in general.
"""

MODERATION_PROMPT = """Write in language that is academic, safe, inoffensive, 
eloquent, succinct"""

DOC_PROMPT = """
<document index="{index}">
{content}
</document>
"""

def get_question_prompt(name, size: PromptSize):
    style = ""
    if size == PromptSize.SMALL:
        style = STYLE_PROMPT_SM
    elif size == PromptSize.MEDIUM:
        style = STYLE_PROMPT_MD
    style += MODERATION_PROMPT
    return QUESTION_PROMPT.format(name=name, style=style)


def get_prompt(name, documents, size: PromptSize):
    docs_prompt = ""
    for i, doc in enumerate(documents):
        docs_prompt += DOC_PROMPT.format(index=i+1, content=doc)
    question_prompt = get_question_prompt(name, size)
    return INITIAL_PROMPT + DOCS_PROMPT.format(docs=docs_prompt) + \
        QUOTE_PROMPT + question_prompt
