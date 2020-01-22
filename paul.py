import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=";;")

@bot.event
async def on_ready():
    print(f"{bot.user.name} Initialized and connected to Discord.")

@bot.command(name = "meow")
async def meow(ctx):
    await ctx.send("MEEEEEEOOOOOOWWWW!!!!!!!   *Translation*: **GIB FOOD!**")

bot.run(token)