import os
import random
import logging

import discord
from discord.ext import commands

from dotenv import load_dotenv

import time

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename=f"Logs/debug-{timestr}.log",level=logging.DEBUG)

logging.info("Log Start")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')#load Oauth

bot = commands.Bot(command_prefix=";;")

@bot.event
async def on_ready():#confirms init
    print(f"{bot.user.name} Initialized and connected to Discord.")
    logging.info("Bot Connected to Discord")

@bot.command(name = "meow")#sends gib food
async def meow(ctx):
    logging.info("Meow command")
    await ctx.send("MEEEEEEOOOOOOWWWW!!!!!!!   *Translation*: **GIB FOOD!**")

#@bot.command(name = "embed")#embed message test (uncomment line to reenable)
async def embedTest(ctx):
    embed = discord.Embed(title = "Test", description = "A test embed that will eventually be used for statistics.", color = 0x672aff)
    embed.add_field(name = "Field 1", value = 1337, inline = False)
    embed.add_field(name = "Field 2", value = "YOLO!")
    embed.add_field(name = "Field 3", value = "Swag")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/522136892448178206/667924013967867934/image0.jpg")
    await ctx.send(embed = embed)

@bot.command(name = "pet")#sends random image of paul
async def petCat(ctx):
    logging.info("Pet Command")
    imgs = os.listdir("./Images/Paul")#list of image files in the Paul folder
    #print(imgs)#debug
    img = discord.File(f"./Images/Paul/{random.choice(imgs)}")
    await ctx.send(file = img)

@bot.command(name = "petpetpet")#paul lottery command 
async def petpetpet(ctx,numImg = 3):
    if numImg > 10:
        numImg = 3
        await ctx.send("HISSSSSS!!!   *Translation*: **!!ERROR CUTENESS OVERLOAD!!**")
    
    logging.info(f"PetPetPet Command, NumImg = {numImg}")
    imgs = os.listdir("./Images/petpetpet")
    img = []
    for _ in range(numImg):#chooses images to send
        image = discord.File(f"./Images/petpetpet/{random.choice(imgs)}")
        img.append(image)
        await ctx.send(file = image)

    embed = discord.Embed(description = "", color = 0x672aff)
    if all(image == img[0] for image in img):#TODO add responses for two of a kind (or some percantage threshhold)
        embed.add_field(name  = "PetPetPet!", value = "**YOU WON!!!**")
    else:
        embed.add_field(name  = "PetPetPet!", value = "**You Lost!**")
    await ctx.send(embed = embed)

bot.run(token)