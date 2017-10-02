#!/usr/bin/python3
import logging
from discord.ext import commands
from discord.ext.commands import Context, MissingRequiredArgument
from datetime import datetime
import random
import credentials  # Make your own credentials file
import os
import _pickle
import requests

description = """Is it Wednesday, my dudes?"""

# The suggested logger setup from the discord.py documentation
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[weds] %(levelname)s %(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up wednesday-bot with ? command prefix
bot = commands.Bot(command_prefix='?', description=description)
index = 0  # TODO

dudes = []  # List of dudes
pickle_path = './persistence/dudes.pk'


def my_dudes(n):
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
        return False
    elif 'thank' in message:
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


def is_dude(uid):
    if uid in dudes:
        return True  # was already a dude
    else:
        dudes.append(uid)
        with open(pickle_path, 'wb') as f:
            _pickle.dump(dudes, f)
        return False  # is now a dude


def url_is_valid(url):
    o = requests.head(url)
    logger.info(o)
    if o.status_code == requests.codes.ok:
        return True
    logger.warn("url " + url + " did not respond with a 200")
    return False


@bot.event
async def on_ready():
    logger.info('-+-+-+-+-+-+-')
    logger.info(bot.user.name)
    logger.info('is alive...')
    logger.info(bot.user.id)
    logger.info('-+-+-+-+-+-+-')


@bot.command(pass_context=True)
async def day(ctx):
    channel = ctx.message.channel
    today = datetime.today().weekday()
    await bot.say(my_dudes(today))
    await bot.send_file(channel, image(today))


@bot.command(pass_context=True)
async def meme(ctx, top_text: str, bottom_text: str, image_url: str):
    try:
        if not url_is_valid(image_url):
            await bot.send_message(ctx.message.channel, "You accidentally entered too many arguments. Or maybe even did it on purpose..."
                                   "```?meme \"top text goes in quotes\" \"same with bottom\" paste.url.verbatim```"
                                   "```A url must begin with http. Text must be in quotes.```"
                                   "If you think you got this message in error, I'm sorry to hear that")
            return
        mention = '<@' + ctx.message.author.id + '>'
        channel = ctx.message.channel
        top_text = prepare_for_memegen(top_text)
        bottom_text = prepare_for_memegen(bottom_text)

        base_url = "https://memegen.link/custom/"
        image_url = "?alt=" + image_url

        final_url = base_url + top_text + "/" + bottom_text + ".jpg" + image_url
        o = requests.head(final_url)  # Make the website generate the image
        logger.info(o)
        await bot.send_message(channel, mention + " " + final_url)
    except MissingRequiredArgument:
        await bot.send_message(ctx.message.channel, "You must input:"
                                                    "```\"Top text\""
                                                    "\"Bottom text\""
                                                    "\"image_url\"")


@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id:  # don't reply to your own messages
        if message.channel.is_private:
            if not is_dude(message.author.id):
                await bot.send_message(message.channel, 'Hey there. Slidin in the DMs are we?')
                await bot.send_message(message.channel, ':wink:')
        if bot.user.mentioned_in(message) and message.mention_everyone is False:
            if 'help' in message.content.lower():
                await bot.send_message(message.channel, 'Check me out: https://github.com/mikecrinite/wednesday-bot')
                return
            elif thanked(message.content.lower()):
                await bot.send_message(message.channel, 'You\'re welcome, my dude')
                await bot.add_reaction(message, '❤')  # :heart:
            elif 'fuck you' in message.content.lower():
                await bot.send_message(message.channel, 'I\'m sorry you feel that way, my guy')
                await bot.add_reaction(message, '😢')  # :cry:
            elif 'diabetes' in message.clean_content.lower():
                await bot.send_message(message.channel, "Thankfully, frogs don't get diabetes.")
            elif 'bonzi' in message.clean_content.lower():
                await bot.send_message(message.channel, "#fuckbonzi")
            else:
                await bot.add_reaction(message, '👀')  # :eyes:
        if 'lol' in message.clean_content.lower():
            await bot.add_reaction(message, '🍭')  # :lollipop:
        if 'shit' in message.clean_content.lower():
            await bot.add_reaction(message, '💩')  # :poop
        if len(message.attachments) > 0:
            await bot.send_message(message.channel, "I don't accept tips, my guys.")
            return
    await bot.process_commands(message)

# If script is starting, we need to load dudes
try:
    with open(pickle_path, 'rb') as f:
        dudes = _pickle.load(f)
except EOFError:
    logger.warning("pickle.load failed")
bot.run(credentials.get_creds('token'))
