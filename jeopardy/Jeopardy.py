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


def load_questions(self):
    questions = os.path.join(os.path.dirname(__file__), 'resources/JEOPARDY_QUESTIONS.json')
    with open(questions, 'r') as f:
        self.questions = json.load(f)


def get_random_question(self):
    """
    Retrieves a random question from the list of questions and returns
    the question formatted as a pretty string
    :return: The question as a string formatted for Discord
    """
    self.curr = jq(random.choice(self.questions))

    return self.curr.pretty_format_discord()


def response(self, response: str):
    if response.lower() == self.curr.answer.lower():
        return [True, self.curr.value]
    else:
        return [False, "Incorrect"]


def no_response(self):
    return "The correct response was: " + self.curr.answer


# Set up Jeopardy
jeopardy_logger = logging.getLogger('wednesday.jeopardy')
jeopardy_logger.setLevel(logging.INFO)
load_questions()


