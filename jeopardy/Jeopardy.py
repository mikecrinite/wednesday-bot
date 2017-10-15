import json
import os
import random

from jeopardy.JeopardyQuestion import JeopardyQuestion as jq


class Jeopardy:
    """
    THIS...IS...JEOPARDY!

    :questions: A list of questions in JEOPARDY_QUESTIONS.json from reddit
    :curr: The current question, parses into a JeopardyQuestion
    """
    def __init__(self):
        self.questions = []
        self.curr = None

        self.load_questions()

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


if __name__ == '__main__':
    j = Jeopardy()

