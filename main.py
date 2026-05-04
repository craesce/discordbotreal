
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
