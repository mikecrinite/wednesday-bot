import json
import os
import random
import logging

from jeopardy.JeopardyQuestion import JeopardyQuestion as jq


"""
THIS...IS...JEOPARDY!

:questions: A list of questions in JEOPARDY_QUESTIONS.json from reddit
:curr: The current question, parses into a JeopardyQuestion
"""
questions = []
curr = None


def load_questions():
    global questions
    questions = os.path.join(os.path.dirname(__file__), 'resources/JEOPARDY_QUESTIONS.json')
    with open(questions, 'r') as f:
        questions = json.load(f)


def get_random_question():
    """
    Retrieves a random question from the list of questions and returns
    the question formatted as a pretty string
    :return: The question as a string formatted for Discord
    """
    global curr
    curr = jq(random.choice(questions))

    return curr.pretty_format_discord()


def response(resp: str):
    if resp.lower() == curr.answer.lower():
        return [True, curr.value]
    else:
        return [False, "Incorrect"]


def no_response():
    return "The correct response was: " + curr.answer


# Set up Jeopardy
jeopardy_logger = logging.getLogger('wednesday.jeopardy')
jeopardy_logger.setLevel(logging.INFO)
load_questions()


