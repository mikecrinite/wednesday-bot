import logging
from discord.ext import commands
from datetime import datetime
import random
import credentials  # Make your own credentials file

description = """Is it Wednesday, my dudes?"""

# The suggested logger setup from the discord.py documentation
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
# Absolutely don't need this written to a log file, but keeping for future reference
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?', description=description)


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

    TODO: organize some meme folders, call from there instead, post direct images instead of links
    """
    return{
        0: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Monday
            ],
        1: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Tuesday
            "http://i.imgur.com/zBviPIU.jpg"
            ],
        2: ["http://i0.kym-cdn.com/photos/images/original/001/091/264/665.jpg",     # Wednesday MY DUDES!
                "http://i0.kym-cdn.com/photos/images/original/001/118/749/887.jpg",
                "http://i0.kym-cdn.com/photos/images/original/000/937/093/395.png",
                "http://i0.kym-cdn.com/photos/images/original/001/091/264/665.jpg",
                "http://i0.kym-cdn.com/photos/images/original/001/279/213/5ce.jpg"
            ],
        3: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Thursday
            ],
        4: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Friday
            ],
        5: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Saturday
            ],
        6: ["https://i.imgur.com/mfhfh7o.jpg"                                       # Sunday
            ],
    }[x]


@bot.event
async def on_ready():
    print('-+-+-+-+-+-+-')
    print(bot.user.name)
    print('is alive...')
    print(bot.user.id)
    print('-+-+-+-+-+-+-')


@bot.command()
async def day():
    today = datetime.today().weekday()
    await bot.say(my_dudes(today))
    await bot.say(random.choice(image(today)))


bot.run(credentials.getCreds('token'))
