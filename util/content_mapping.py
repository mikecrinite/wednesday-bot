
# { keyword : [reply, reaction, stop_processing?] }
"""
listen_mappings contains target words that the bot should constantly be listening
for. each target word maps to a list containing
    - the reply (should the bot say anything in response?)
    - a reaction (should the bot react to the previous message?)
    - True/False indicating whether the bot should stop looking for keywords
"""
listen_mappings = {
    'lol': ['', '🍭', False],
    'shit': ['', '💩', False],
    'stop': ['', '', False]
}

mention_mappings = {
    'fuck you': ['I\'m sorry you feel that way, my guy', '😢', True],
    'diabetes': ['Thankfully, frogs don\'t get diabetes.', '', False],
    'bonzi': ['#fuckbonzi', ':B:', False]
}


def listen_to(message):
    """
    Checks if message contains a target word.
    Upon receiving a target word, add it to the list to return
    """
    l = []
    for key in listen_mappings:
        if key in message.content.lower:
            v = listen_mappings[key]
            l.append(v)
            if stop_processing(l):
                break
    return l


def mentioned_in(message):
    """
    If the bot is mentioned, check if any target words exist.
    Upon receiving a target word, add it to the list to return
    """
    m = []
    for key in mention_mappings:
        if key in message.content.lower:
            m.append(mention_mappings[key])
    return m


def stop_processing(l):
    return l[2]
