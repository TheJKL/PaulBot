import os
import random
import logging
import yaml
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import pymongo

version = "0.2pre1-dev"
#TODO docstrigs
#init
#logging
timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename=f"Logs/debug-{timestr}.log",level=logging.DEBUG)
logging.info("Log Start")
#oauth
load_dotenv()
token = os.getenv('DISCORD_TOKEN')#load Oauth
#config load
if "config.yaml" not in os.listdir("./"):#check to see if a config file exists
    os.system("cp config.defaults config.yaml")#create config from template (if it doesnt exist)
with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
#config init
imgParentDir = config["imageFolder"]
imgChildDirs = config["imageSubfolders"]
petpetpetDir = config["lotteryFolder"]
dbAddr = config["databaseAddress"]
bot = commands.Bot(command_prefix=config["commandPrefix"])
defaultCat = config["defaultCat"]
#mongo init
client = pymongo.MongoClient(f"mongodb://{dbAddr}/")
db = client.paulDB
settings = db.settings
users = db.users

@bot.event
async def on_ready():#confirms init
    print(f"{bot.user.name} Initialized and connected to Discord.")
    logging.info("Bot Connected to Discord")

@bot.command(name = "meow")#sends gib food
async def meow(ctx):
    logging.info("Meow command")
    await ctx.send("MEEEEEEOOOOOOWWWW!!!!!!!   *Translation*: **GIB FOOD!**")

@bot.command(name = "info")#TODO Info command
async def info(ctx,user = ""):
    embed = discord.Embed(title = "Test", description = "A test embed that will eventually be used for statistics.", color = 0x672aff)
    embed.add_field(name = "Field 1", value = 1337, inline = False)
    embed.add_field(name = "Field 2", value = "YOLO!")
    embed.add_field(name = "Field 3", value = "Swag")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/522136892448178206/667924013967867934/image0.jpg")
    await ctx.send(embed = embed)

@bot.command(name = "pet")#sends random image of paul
async def petCat(ctx, cat = "", numImg = 1):
    logging.info("Pet Command")

    if cat.capitalize() not in imgChildDirs:
        cat = defaultCat
    else:
        cat = cat.capitalize()

    imgs = os.listdir(f"{imgParentDir}/{cat}")#list of image files in the Paul folder
    img = discord.File(f"{imgParentDir}/{cat}/{random.choice(imgs)}")
    await ctx.send(file = img)

@bot.command(name = "petpetpet")#paul lottery command 
async def petpetpet(ctx, numImg = 3, cat = ""):
    if numImg > 10:#limit petpetpet images to 10 - 1 per command call
        numImg = 3
        await ctx.send("HISSSSSS!!!   *Translation*: **!!ERROR CUTENESS OVERLOAD!!**")
    
    if cat.capitalize() not in imgChildDirs:
        imgDir = petpetpet
    else:
        imgDir = cat.capitalize()
    
    logging.info(f"PetPetPet Command, NumImg = {numImg}, cat = {cat}")
    imgs = os.listdir(f"{imgParentDir}/{imgDir}")
    img = []

    for _ in range(numImg):#chooses images to send
        rand = random.choice(imgs)
        image = discord.File(f"{imgParentDir}/{imgDir}/{rand}")
        img.append(str(rand))
        await ctx.send(file = image)

    embed = discord.Embed(description = "", color = 0x672aff)
    if all(image == img[0] for image in img):#TODO add responses for two of a kind (or some percantage threshhold)
        embed.add_field(name  = "PetPetPet!", value = "**YOU WON!!!**")
    else:
        embed.add_field(name  = "PetPetPet!", value = "**You Lost!**")
    await ctx.send(embed = embed)

@bot.command(name = "feed")
async def feed(ctx, cat = "", numFood = 1):
    numFood = int(abs(numFood))
    if cat.capitalize() not in imgChildDirs:
        cat = defaultCat
    else:
        cat = cat.capitalize()
    user = db.users.find_one({"uuid":ctx.author.id})
    if not user:#check if the user is in the DB
        createUser(ctx.author.id)
        user = db.users.find_one({"uuid":ctx.author.id})
    logging.info(f"feed command, cat = {cat}, numFood = {numFood}")
    if not user["food"] < numFood:
        if numFood < 100:
            await ctx.send("Nom"*numFood)
        else:
            await ctx.send(":regional_indicator_n: :regional_indicator_o: :regional_indicator_m:")
        db.users.update_one({"uuid":"totals"},{"$inc":{f"food.{cat}":numFood}})#increment food fed to cats
        db.users.update_one({"uuid":"totals"},{"$inc":{f"feed.{cat}":1}})#increment total feed command executes
        db.users.update_one({"uuid":ctx.author.id},{"$inc":{"food":-1*numFood}})#remove food from user
        db.users.update_one({"uuid":ctx.author.id},{"$inc":{f"totals.feed.{cat}":1}})#increment users total command execs
    else:
        await ctx.send("MEOWWWWW   *Translation*: **You don't have that much food.**")

def createUser(uuid):
    if not users.count_documents({"uuid":uuid}):
        users.insert_one({
            "uuid" : uuid,
            "food" : 10,
            "totals" : {}
            })

def sendImage(ctx,img,cat):
    await ctx.send(file = img)
    db.users.update_one({"uuid":"totals"},{"$inc":{f"sentImg.{cat}":1}})


bot.run(token)