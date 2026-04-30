
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
     await message.channel.send(
        "https://www.reddit.com/media?url=https%3A%2F%2Fpreview.redd.it%2Fpost-your-favorite-glep-screenshot-ill-go-first-v0-qyielkk6q3cd1.jpeg%3Fwidth%3D2360%26format%3Dpjpg%26auto%3Dwebp%26s%3D1b9ef5d6ce3fa3c87bf5ab1b401d9d081b2a2d53")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        await message.channel.send("Typeshit")
        return
    if "job" in message.content.lower():
           await message.channel.send(
             "https://tenor.com/view/breaking-phone-glep-smiling-friends-destroying-phone-angry-gif-14103972177458051138")
    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

cock