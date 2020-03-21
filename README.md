# PaulBot
*A discord bot for pictures of Paul the cat.*

## Commands

### Command Prefix :
Set to `!` by default but can be changed in config. 

### Meow :
Replies with a text message, the message is currently static however in future(sometime in v0.2) will be random from a list.

### Pet :
Replies with a random image of Paul from the `./Images/[cat]` folder uses defaultCat setting if no cat is provided.

*Usage:* `!pet [cat]`

### PetPetPet :
Replies with `numImg` random images from a random pool of 15 images from `./Images/[cat]`.

*Usage:* `!petpetpet [cat] [numImg]`

### Feed :
Iterates a statistic of how much food a cat has been fed.

*Usage:* `!feed [cat] [numFood]`

### Info :
A disorganized collection of statistics for a user, if no user is given or the user is invalid it displays overall total statistics.

*Usage:* `!info @[user]`

## Setup

The bot requires a discord Oauth token which is stored in a file called `.env` in the program directory, this file is not included in this repo and must be setup for the bot to work. The contents of the file should be:

`DISCORD_TOKEN = "[OAuth Token]"`

Where [OAuth Token] is a discord bot’s OAuth token.

### Python Libraries

- discord.py

- python_dotenv

- pymongo

- yaml

### Config

On first launch a config file (`config.yaml`) will be created from `config.defaults`, this file contains all config options for paulBot aside from the oauth token.


*config.defaults*

```yaml
commandPrefix: "!"
imageFolder: "./Images"
imageSubfolders: 
  - Paul
defaultCat: Paul
databaseAddress: localhost
```
**defaultCat** = Default image subfolder to use if one isnt provided on command execution.

**databaseAddress** = ip of the mongoDB database being used for the bot.


### MongoDB Structure

The database should be named `paulDB` and have a collection called `users`, users needs to be initialized with a document with this structer:

```javascript
{
    "uuid":"totals",
    "totals":{}
}
```


## Additional Notes

A `debug-[date]-[time].log` file will be created on each startup of the bot in the `./Logs` directory. The date time format is `yearMonthDay-hourMinuteSecond`.
