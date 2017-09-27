#!/usr/bin/python3
import logging
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime
import random
import credentials  # Make your own credentials file
import os

description = """Is it Wednesday, my dudes?"""

# The suggested logger setup from the discord.py documentation
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[weds] %(levelname)s %(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?', description=description)
index = 0  # TODO


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
        0: './monday/' + random.choice(os.listdir('./monday')),
        1: './tuesday/' + random.choice(os.listdir('./tuesday')),
        2: './wednesday/' + random.choice(os.listdir('./wednesday')),
        3: './thursday/' + random.choice(os.listdir('./thursday')),
        4: './friday/' + random.choice(os.listdir('./friday')),
        5: './saturday/' + random.choice(os.listdir('./saturday')),
        6: './sunday/' + random.choice(os.listdir('./sunday')),
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


@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id:  # don't reply to your own messages
        if message.channel.is_private:
            await bot.send_message(message.channel, 'Hey there. Slidin in the DMs are we?')
        if bot.user.mentioned_in(message) and message.mention_everyone is False:
            if 'help' in message.content.lower():
                await bot.send_message(message.channel, 'Check me out: https://github.com/mikecrinite/wednesday-bot')
                return
            elif thanked(message.content.lower()):
                await bot.send_message(message.channel, 'You\'re welcome, my dudes')
                await bot.add_reaction(message, ':heart:')  # :heart: TODO
            elif 'fuck you' in message.content.lower():
                await bot.send_message(message.channel, 'I\'m sorry you feel that way, my guy')
                await bot.add_reaction(message, '😢')  # :cry:
            else:
                await bot.add_reaction(message, '👀')  # :eyes:
        if 'lol' in message.clean_content.lower():
            await bot.add_reaction(message, '🍭')  # :lollipop:
        if 'shit' in message.clean_content.lower():
            await bot.add_reaction(message, '💩') # :poop
        if len(message.attachments) > 0:
            await bot.send_message(message.channel, "I don't accept tips, my guys.")
            return
    await bot.process_commands(message)


bot.run(credentials.get_creds('token'))
