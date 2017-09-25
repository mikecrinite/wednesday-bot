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
handler.setFormatter(logging.Formatter('[%(levelname)] %(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?', description=description)
index = 0


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


bot.run(credentials.get_creds('token'))
