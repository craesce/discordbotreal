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
    0: (" |\n"
        " |\n"
        " |\n"),

    1: (" _______\n"
        " |/\n"
        " |\n"
        " |\n"
        " |\n"),

    2: (" _______\n"
        " |/   |\n"
        " |\n"
        " |\n"
        " |\n"),

    3: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |\n"
        " |\n"),

    4: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |    |\n"
        " |\n"),

    5: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |   /|\n"
        " |\n"),

    6: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |   /|\\\n"
        " |\n"),

    7: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |   /|\\\n"
        " |   /\n"),

    8: (" _______\n"
        " |/   |\n"
        " |    o\n"
        " |   /|\\\n"
        " |   / \\\n")
}

words = ["banana", "apple", "discord", "python", "penis", "67", "glep", "typeshit"]

games = {}

@bot.command()
async def hangman(ctx):

    answer = random.choice(words)

    games[ctx.author.id] = {
        "answer": answer,
        "wrong_guesses": 0,
        "letters_guessed": set(),
        "guesses": 0,
        "hidden_word": ["[ ]"] * len(answer)
    }

    await ctx.send(
        f"Hangman gestartet!\n"
        f"```{hangman_art[0]}```\n"
        f"{' '.join(games[ctx.author.id]['hidden_word'])}"
    )

@bot.command()
async def hguess(ctx, guessed_input):

    if ctx.author.id not in games:
        await ctx.send("Du hast kein aktives Spiel")
        return

    game = games[ctx.author.id]

    answer = game["answer"]
    letters_guessed = game["letters_guessed"]
    hidden_word = game["hidden_word"]

    guessed_input = guessed_input.lower()


    if len(guessed_input) > 1:

        if guessed_input == answer:

            await ctx.send(
                f"GEWONNEN!\n"
                f"Das Wort war: **{answer}**"
            )

            del games[ctx.author.id]
            return

        else:
            game["wrong_guesses"] += 1

    else:

        if guessed_input in letters_guessed:
            await ctx.send("Schon geraten.")
            return

        letters_guessed.add(guessed_input)

        if guessed_input in answer:

            for i in range(len(answer)):
                if answer[i] == guessed_input:
                    hidden_word[i] = guessed_input

        else:
            game["wrong_guesses"] += 1

    wrong_guesses = game["wrong_guesses"]

    if all(char in letters_guessed for char in answer):

        await ctx.send(
            f"GEWONNEN!\n"
            f"Das Wort war: **{answer}**"
        )

        del games[ctx.author.id]
        return

    if wrong_guesses == len(hangman_art)-1:

        await ctx.send(
            f"```{hangman_art[wrong_guesses]}```\n"
            f"Game Over\n"
            f"Wort: **{answer}**"
        )

        del games[ctx.author.id]
        return

    await ctx.send(
        f"```{hangman_art[wrong_guesses]}```\n"
        f"{' '.join(hidden_word)}\n"
        f"Letters guessed: {', '.join(sorted(letters_guessed))}"
    )

@bot.command()
async def idee(ctx):
    await ctx.send(

        f"die Idee nieder")

reaction_sessions = {}
@bot.command()
async def reaction(ctx):

    embed = discord.Embed(
        title = "Reaction",
        description = "React with :cat:"
    )

    msg = await ctx.send(embed=embed)

    await msg.add_reaction(":cat:")

    reaction_sessions[msg.id] = True

@bot.event()
async def on_reaction_add(reaction, user):

    if user.bot:
        return

    message = reaction.message

    if message.id not in reaction_sessions:
        return

    emoji = str(reaction.emoji)

    responses = {
        ":cat:": "C:\Users\KleinCh\PycharmProjects\clean-repo\img\rosi.jpg"
    }

    if emoji in responses:
        await message.channel.send(responses[emoji])

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
