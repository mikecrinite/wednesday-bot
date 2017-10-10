import os
import random
import requests
import logging

util_logger = logging.getLogger('wednesday.util')


def my_dudes(n):
    """
    Return text corresponding to which day it is
    """
    return {
        0: "it is monday, my dudes",
        1: "it is tuesday, my dudes",
        2: "IT IS WEDNESDAY, MY DUDES",
        3: "it is thursday, my dudes...",
        4: "it is friday, my dudes",
        5: "it is saturday, my dudes",
        6: "it is sunday, my dudes",
    }[n]


def image(x):
    """
    Return a dank meme corresponding to how close to Wednesday it is, my dudes.
    """
    return{
        0: 'memes/monday/' + random.choice(os.listdir('memes/monday')),
        1: 'memes/tuesday/' + random.choice(os.listdir('memes/tuesday')),
        2: 'memes/wednesday/' + random.choice(os.listdir('memes/wednesday')),
        3: 'memes/thursday/' + random.choice(os.listdir('memes/thursday')),
        4: 'memes/friday/' + random.choice(os.listdir('memes/friday')),
        5: 'memes/saturday/' + random.choice(os.listdir('memes/saturday')),
        6: 'memes/sunday/' + random.choice(os.listdir('memes/sunday')),
    }[x]


def thanked(message):
    """
    Try to determine if wednesday-bot was thanked in the previous message.
    Obviously at this point it is a very cursory check.
    :param message: Message to parse
    :return: True if thanked
    """
    if 'no thanks' in message or 'for nothing' in message:
        util_logger.info(message + " : false")
        return False
    elif 'thank' in message:
        util_logger.info(message + " : true")
        return True
    return False


def prepare_for_memegen(text):
    """
    see https://memegen.link

    memegen requires reserved characters to be escaped using
    the replacements below
    """
    text = text.replace("-", "--")
    text = text.replace("_", "__")
    text = text.replace(" ", "_")
    text = text.replace("?", "~q")
    text = text.replace("%", "~p")
    text = text.replace("#", "~h")
    text = text.replace("/", "~s")
    text = text.replace("\"", "\'\'")

    return text


def url_is_valid(url):
    """
    Uses the Requests library to attempt to access a url, and
    determines whether the url is valid by its response
    :param url: Address to check
    :return: True if url returns 200
    """
    try:
        o = requests.head(url, allow_redirects=True)
        if o.status_code == requests.codes.ok:
            util_logger.info(url + " responded with 200")
            return True
        else:
            return False
    except Exception:
        util_logger.warning("url " + url + " did not respond with a 200")
    return False
