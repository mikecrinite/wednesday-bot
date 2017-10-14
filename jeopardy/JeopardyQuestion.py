class JeopardyQuestion:
    def __init__(self, json_question):
        self.round = json_question['round']
        self.show_number = json_question['show_number']
        self.value = json_question['value']
        self.answer = json_question['answer']
        self.air_date = json_question['air_date']
        self.category = json_question['category']
        self.question = json_question['question']
        self.pretty = ""

    def pretty_format_discord(self):
        """
        Formats the message in such a way that it will be printed
        in a human-readable (and pretty) way when sent to Discord
        :return:
        """
        self.pretty = "```\n" \
                      "%s\n" \
                      "Category: %s\n" \
                      "Clue: %s\n" \
                      "```" % (self.value, self.category, self.question)
        return self.pretty


