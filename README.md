# wednesday-bot
## Is it Wednesday, my dudes?

If you found this helpful or funny in any way, please let me know. I noticed I occasionally get visitors. Say hi!
If you came here because you need help figuring out your own Discord bot, feel free to ask for help.

### Command(s):

- `?day` : wednesday-bot will tell you what day it is and provide a helpful visual aid, should you continue to be confused but just don't want to admit it. Often, on days other than Wednesday, the visual aid will simply alert you that it is in fact not Wednesday, which is really the only important thing you need to know.
- `?meme` : wednesday-bot will create a link to https://memegen.link that you can use to generate an image macro for your given text and image
- `?jeopardy`: WB will provide you with a jeopardy clue. Respond in the form of a question (as per the Jeopardy rules) and possibly in the future WB will remember your total
- `?russian_roulette`: Find out how it feels to REALLY be ALIVE! (Possible side-effects include death)

### Startup:

You'll need to set some environment variables:
```
TOKEN:     your_discord_api_token
CHANNEL:   123456789  # The channel id that wednesday bot should send reminders to
```

There are three ways you can run this bad boy:

1. You can use ```./dockerizeAndRun``` which will dockerize and run the service. This is kind of in its infancy but since this project is also for teaching myself some stuff, I'm not worried about it being sexy right now.
2. Use the ```./run``` script which will handle log rotation and then ask if WB is alive. You can ```./stop``` to kill the process or ```./restart``` to fetch the latest from git and then start up the bot with the latest changes. This is probably the best way tbh.
3. You can just run ```python3 wednesday.py``` or ```./wednesday.py``` 

### FAQ: 

#### Why?
Because I was tired of not being able to know what day it was at a moment's notice.
(But actually, the goal was to help learn python and also because my friends really enjoy this meme)

#### How to use:
If you want him on your server, you can ask, but honestly he's hosted on my personal AWS instance which is currently not costing me anything so I don't really know if I want to have him on a bunch of Discord servers.
It wouldn't hurt to ask, though.

Otherwise, you can fork the bad boy and set up your own wednesday-bot until I get a raise and wouldn't mind paying for the traffic on an AWS instance.

#### DISCLAIMER TO CURRENT/PROSPECTIVE EMPLOYERS:
This repo is for the memes. Commit messages/filenames/etc are not indicative of how I do things in a professional environment.
But it is an indication of how I write code so yeah go ahead and look at that.
