import logging

# { keyword : [reply, reaction, stop_processing?] }
"""
listen_mappings contains target words that the bot should constantly be listening
for. each target word maps to a list containing
    - the reply (should the bot say anything in response?)
    - a reaction (should the bot react to the previous message?)
    - True/False indicating whether the bot should stop looking for keywords

If you want to add something, make sure you add it to the correct mapping:
    - listen_mappings: if the key shows up in any message the bot can see, the bot will
      add the reaction and send the response
    - mention_mappings: if the key shows up in a message that mentions the bot, it will
      add the reaction and send the response

We can probably consolidate those two functions at one point....
"""
listen_mappings = {
    'lol': ['', '🍭', False],
    'shit': ['', '💩', False],
    'stop': ['', '', False]
}

mention_mappings = {
    'repo': ['Check me out: https://github.com/mikecrinite/wednesday-bot', '', True],
    'fuck you': ['I\'m sorry you feel that way, my guy', '😢', True],
    'diabetes': ['Thankfully, frogs don\'t get diabetes.', '', False],
    'bonzi': ['#fuckbonzi', '🅱', False]
}

cm_logger = logging.getLogger('wednesday.content_mapping')
cm_logger.setLevel(logging.INFO)


def listen_to(message):
    """
    Checks if message contains a target word.
    Upon receiving a target word, add it to the list to return
    """
    l = []
    for key in listen_mappings:
        if key in message:
            v = listen_mappings[key]
            l.append(v)
            if stop_processing(v):
                break
    return l


def mentioned_in(message):
    """
    If the bot is mentioned, check if any target words exist.
    Upon receiving a target word, add it to the list to return
    """
    m = []
    for key in mention_mappings:
        if key in message:
            v = mention_mappings[key]
            m.append(v)
            if stop_processing(v):
                break
    return m


def stop_processing(l):
    return l[2]
