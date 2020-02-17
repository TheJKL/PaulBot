# PaulBot
*A discord bot for pictures of Paul the cat.*

## Commands

**Meow :**
Replies with a text message, the message is currently static however in future(sometime in v0.2) will be random from a list.

**Pet :**
Replies with a random image of Paul from the `./Images` folder

### Command Prefix :
Currently this is set to `;;` by default. 

## Setup

The bot requires a discord Oauth token which is stored in a file called `.env` in the program directory, this file is not included in this repo and must be setup for the bot to work. The contents of the file should be:

`DISCORD_TOKEN = "[OAuth Token]"`

Where [OAuth Token] is a discord bot’s OAuth token.

### Python Libraries

-discord.py

-python_dotenv

## Additional Notes

A `debug-[date]-[time].log` file will be created on each startup of the bot in the `./Images` directory. The date time format is `yearMonthDay-hourMinuteSecond`.
