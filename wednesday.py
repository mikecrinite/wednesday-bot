#!/usr/bin/python3
import logging
from discord.ext import commands
from discord.ext.commands import Context, MissingRequiredArgument
from datetime import datetime
import requests

import credentials  # Make your own credentials file
from persistence import persistence
from util import util

description = """Is it Wednesday, my dudes?"""

# The suggested logger setup from the discord.py documentation
logger = logging.getLogger('wednesday')
logger.setLevel(logging.DEBUG)
loggerd = logging.getLogger('discord')
loggerd.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/wednesday.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[weds] %(levelname)s %(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)
loggerd.addHandler(handler)

# Set up wednesday-bot with ? command prefix
bot = commands.Bot(command_prefix='?', description=description)


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
    await bot.say(util.my_dudes(today))
    await bot.send_file(channel, util.image(today))


@bot.command(pass_context=True)
async def meme(ctx, top_text: str, bottom_text: str, image_url: str):
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
    logger.info(final_url + " responded : " + o)
    await bot.send_message(channel, mention + " " + final_url)



@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id:  # don't reply to your own messages
        if message.channel.is_private:
            if not persistence.is_dude(message.author.id):
                await bot.send_message(message.channel, 'Hey there. Slidin in the DMs are we?')
                await bot.send_message(message.channel, ':wink:')
        if bot.user.mentioned_in(message) and message.mention_everyone is False:
            if 'help' in message.content.lower():
                await bot.send_message(message.channel, 'Check me out: https://github.com/mikecrinite/wednesday-bot')
                return
            elif util.thanked(message.content.lower()):
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


@bot.event
async def on_command_error(error, ctx):
    if error == MissingRequiredArgument:
        # For now, this MUST be in meme()
        # TODO: add a help and change this message
        logger.error(ctx.message + " : not enough arguments")
        await bot.send_message(ctx.message.channel, "You must input:"
                                                    "```\"Top text\""
                                                    "\"Bottom text\""
                                                    "\"image_url\"")

# If script is starting, we need to load dudes
persistence.load_dudes()
bot.run(credentials.get_creds('token'))
