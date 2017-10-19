#!/usr/bin/python3
import logging
import requests
import asyncio
import re
from asyncio import CancelledError
from discord.ext import commands
from discord.ext.commands import Context, MissingRequiredArgument
from datetime import datetime


import credentials  # Make your own credentials file
from persistence import persistence
from util import util
from util import content_mapping as cm
from jeopardy import Jeopardy

description = """Is it Wednesday, my dudes?"""

# Set up logger for this class and discord
logger = logging.getLogger('wednesday')
logger.setLevel(logging.INFO)
loggerd = logging.getLogger('discord')
loggerd.setLevel(logging.INFO)

# Set up file handler
handler = logging.FileHandler(filename='logs/wednesday.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[weds] %(levelname)s %(asctime)s:%(name)s: %(message)s'))

# Add file handler to loggers
logger.addHandler(handler)
loggerd.addHandler(handler)
persistence.prs_logger.addHandler(handler)
util.util_logger.addHandler(handler)
cm.cm_logger.addHandler(handler)
Jeopardy.jeopardy_logger.addHandler(handler)

# Set up wednesday-bot with ? command prefix
bot = commands.Bot(command_prefix='?', description=description)

# Specify Wednesday discord channel
wednesday_channel = bot.get_channel(credentials.get_creds('channel'))
j_regex = re.compile('(what|who)\s+(is|was|are|were).*')


async def respond_to(message, responses, mentioned):
    channel = message.channel
    for a in responses:
        if a[1] != '':
            await bot.add_reaction(message, a[1])
        if a[0] != '':
            await bot.send_message(channel, a[0])
        if a[2]:  # Stop processing results
            return
    if len(responses) == 0 and mentioned:
        await bot.add_reaction(message, '👀')  # :eyes:


async def wednesday_reminder():
    """
    wednesday-bot will send an automatic Wednesday reminder
    to the channel in your credentials file (under the key 'channel')
    """
    flag = False
    await bot.wait_until_ready()
    while not bot.is_closed:
        now = datetime.today()
        if now.weekday() == 2 and now.hour == 6 and not flag:  # 6am on Wednesday, if no reminder sent already
                logger.info("Deploying Wednesday reminder")
                await bot.send_message(wednesday_channel, util.my_dudes(2))
                await bot.send_file(wednesday_channel, util.image(2))
                flag = True
        else:
            if flag:
                logger.info("Resetting Wednesday reminder flag")
                flag = False
        await asyncio.sleep(30)  # Discord.py needs control once every minute. Sleeping for minutes kills this task


@bot.event
async def on_ready():
    logger.info('-+-+-+-+-+-+-')
    logger.info(bot.user.name)
    logger.info('is alive...')
    logger.info(bot.user.id)
    logger.info('-+-+-+-+-+-+-')


@bot.command(pass_context=True)
async def day(ctx):
    """
    Prints a helpful, friendly message to let you know which day of the week it is.
    Also provides a helpful visual, in case you are still confused.
    """
    channel = ctx.message.channel
    today = datetime.today().weekday()
    await bot.say(util.my_dudes(today))
    await bot.send_file(channel, util.image(today))


@bot.command(pass_context=True)
async def meme(ctx, top_text: str, bottom_text: str, image_url: str):
    """
    Generates a meme of variable dankness. Dankness depends on your inputs for top text, botton text
    and background image url, all three of which must be surrounded in quotes.

    :param top_text: Required: must be surrounded in quotes
    :param bottom_text: Required: must be surrounded in quotes
    :param image_url: Required: must be surrounded in quotes
    """
    logger.info(ctx.message.author + " requested : " + top_text + " " + bottom_text + " " + image_url)
    if not util.url_is_valid(image_url):
        await bot.send_message(ctx.message.channel,
                               "You accidentally entered too many arguments. Or maybe even did it on purpose..."
                               "```?meme \"top text goes in quotes\" \"same with bottom\" paste.url.verbatim```"
                               "```A url must begin with http. Text must be in quotes.```"
                               "If you think you got this message in error, I'm sorry to hear that")
        return
    mention = '<@' + ctx.message.author.id + '>'
    channel = ctx.message.channel
    top_text = util.prepare_for_memegen(top_text)
    bottom_text = util.prepare_for_memegen(bottom_text)

    base_url = "https://memegen.link/custom/"
    image_url = "?alt=" + image_url

    final_url = base_url + top_text + "/" + bottom_text + ".jpg" + image_url
    o = requests.head(final_url)  # Make the website generate the image
    logger.info(final_url + " responded : " + str(o))
    await bot.send_message(channel, mention + " " + final_url)


@bot.command(pass_context=True)
async def jeopardy(ctx):
    """
    WIP: Get a jeopardy question from WB. Answer correctly to earn REAL WEDNESDAY-BUCKS!
    """
    if Jeopardy.active:
        bot.send_message(ctx.message.channel, "You are already playing jeopardy")
        return
    await bot.send_message(ctx.message.channel, Jeopardy.get_random_question())
    time = 0
    while Jeopardy.active:
        if time == 15:
            await bot.send_message(ctx.message.channel, "The answer was: " + Jeopardy.curr.answer)
            Jeopardy.active = False
        time += 1
        await asyncio.sleep(1)


@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id:  # don't reply to your own messages
        if Jeopardy.active:
            if j_regex.match(message.content.lower()):
                j_regex.sub(message.content.lower(), '')  # remove the question and just send the response
                result = Jeopardy.response(message.content)
                await bot.send_message(message.channel, str(message.author) + " ---> " + result[1])
        if message.channel.is_private:
            if not persistence.is_dude(message.author.id):
                await bot.send_message(message.channel, 'Hey there. Slidin in the DMs are we?')
                await bot.send_message(message.channel, ':wink:')
        if bot.user.mentioned_in(message) and message.mention_everyone is False:
            if util.thanked(message.content.lower()):
                await bot.send_message(message.channel, 'You\'re welcome, my dude')
                await bot.add_reaction(message, '❤')  # :heart:
                return
            await respond_to(message, cm.mentioned_in(message.content.lower()), True)
            return
        await respond_to(message, cm.listen_to(message.content.lower()), False)
        if len(message.attachments) > 0:
            logger.info(str(message.author) + " sent " + str(message.attachments) + " attachments.")
            return
    await bot.process_commands(message)


@bot.event
async def on_command_error(error, ctx):
    if error == MissingRequiredArgument:
        logger.error(str(ctx.message) + " : not enough arguments")
    if error == CancelledError:
        logger.error(str(error))


if __name__ == "__main__":
    # If script is starting, we need to load dudes
    persistence.load_dudes()

    # Begin background loop
    bot.loop.create_task(wednesday_reminder())

    # This MUST be the final function call that runs
    bot.run(credentials.get_creds('token'))
