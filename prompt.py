from enum import Enum
from typing import List


class AnswerSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


def answer_size_to_max_tokens(size: AnswerSize) -> int:
    token_num_dict = {
        AnswerSize.SMALL: 1024 * 1,
        AnswerSize.MEDIUM: 1024 * 2,
        AnswerSize.LARGE: 1024 * 4,
    }
    return token_num_dict[size]


def pages_to_answer_size(pages: List[int]) -> AnswerSize:
    pages_count = len(pages)
    if pages_count <= 20:
        return AnswerSize.SMALL
    elif pages_count > 20 and pages_count <= 50:
        return AnswerSize.MEDIUM
    elif pages_count > 50:
        return AnswerSize.LARGE


INITIAL_PROMPT = """
I'm going to give you a series of documents. Read the documents carefully,
because I'm going to ask you a question about them. Here are the documents:
""".replace("\n", " ")

DOCS_PROMPT = """
<documents>
{docs}
</documents>
"""

QUESTION_PROMPT = """
Answer the question in <answer></answer> tags. {style} Don't explain what the
book "The Power Broker" is. If the question cannot be answered by the document,
say so.

Here is the question: Who is {name}?
""".replace("\n", " ")

STYLE_PROMPT = """The answer should be {num} paragraph{s} long and in the
style of a short biography, highlighting how the person is relevant to the
book "The Power Broker" by Robert Caro specifically, and how the person is
relevant more broadly in a historical context.
""".replace("\n", " ")

DOC_PROMPT = """
<document index="{index}">
{content}
</document>
"""


def get_question_prompt(name, size: AnswerSize):
    style = STYLE_PROMPT
    if size == AnswerSize.SMALL:
        style = style.format(num="one", s="")
    elif size == AnswerSize.MEDIUM:
        style = style.format(num="three", s="s")
    elif size == AnswerSize.LARGE:
        style = style.format(num="six", s="s")
    return QUESTION_PROMPT.format(name=name, style=style)


def get_prompt(name, documents, size: AnswerSize):
    docs_prompt = ""
    for i, doc in enumerate(documents):
        docs_prompt += DOC_PROMPT.format(index=i+1, content=doc)
    question_prompt = get_question_prompt(name, size)
    return INITIAL_PROMPT + DOCS_PROMPT.format(docs=docs_prompt) + question_prompt
