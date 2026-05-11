import platform
import subprocess

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from getpass import getpass

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
#python basics

# string_number = '69'
# item = 'banana'
# Item = 'Apple'
# list = [1,2,3,4,5,6,7,'piemel','banana'+item+Item]


#hangman typeshit

import random

hangman_art = {
    0: ("   \n"
        "   \n"
        "   \n"),
    1: (" o \n"
        "   \n"
        "   \n"),
    2: (" o \n"
        " | \n"
        "   \n"),
    3: (" o \n"
        "/| \n"
        "   \n"),
    4: (" o \n"
        "/|\\\n"
        "   \n"),
    5: (" o \n"
        "/|\\\n"
        "/  \n"),
    6: (" o \n"
        "/|\\\n"
        "/ \\\n")
}

words = ["banana", "apple", "discord", "python"]

games = {}

def checkWinCondition(letters_guessed, answer):
    for i in answer:
        if i not in letters_guessed:
            return False
    return True

@bot.command()
async def hangman(ctx):

    answer = random.choice(words)

    games[ctx.author.id] = {
        "answer": answer,
        "wrong_guesses": 0,
        "letters_guessed": set(),
        "guesses": 0,
        "hidden_word": ["_"] * len(answer)
    }

    await ctx.send(
        f"Hangman gestartet!\n"
        f"```{hangman_art[0]}```\n"
        f"{' '.join(games[ctx.author.id]['hidden_word'])}"
    )

@bot.command()
async def hguess(ctx, guessed_letter):

    if ctx.author.id not in games:
        await ctx.send("Du hast kein aktives Spiel")
        return

    game = games[ctx.author.id]

    answer = game["answer"]
    wrong_guesses = game["wrong_guesses"]
    letters_guessed = game["letters_guessed"]
    hidden_word = game["hidden_word"]

    letters_guessed.add(guessed_letter)

    if guessed_letter in answer:

        for i in range(len(answer)):
            if answer[i] == guessed_letter:
                hidden_word[i] = guessed_letter

        if checkWinCondition(letters_guessed, answer):
            await ctx.send(
                f"Correct!\n"
                f"Word: **{answer}**"
            )

            del games[ctx.author.id]
            return

    else:
        game["wrong_guesses"] += 1
        wrong_guesses = game["wrong_guesses"]

    game["guesses"] += 1

    if wrong_guesses >= 6:

        await ctx.send(
            f"```{hangman_art[6]}```\n"
            f"Game Over\n"
            f"Word: **{answer}**"
        )

        del games[ctx.author.id]
        return

    await ctx.send(
        f"```{hangman_art[wrong_guesses]}```\n"
        f"{' '.join(hidden_word)}\n"
        f"Letters guessed: {', '.join(letters_guessed)}"
    )

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
