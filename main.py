import random
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

combo_triggered_messages = set()


image_map = {
    "🐱": "img/rosi.jpg",
    "🔥": "https://media.giphy.com/media/3o72F8t9TDi2xVnxOE/giphy.gif"
}


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await message.channel.send("Typeshit")

    if "job" in message.content.lower():
        await message.channel.send(
            "https://tenor.com/view/breaking-phone-glep-smiling-friends-destroying-phone-angry-gif-14103972177458051138"
        )

    await bot.process_commands(message)


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

words = [
    "banana",
    "apple",
    "discord",
    "python",
    "penis",
    "67",
    "glep",
    "typeshit"
]

games = {}


@bot.command()
async def hangman(ctx):

    answer = random.choice(words)

    games[ctx.author.id] = {
        "answer": answer,
        "wrong_guesses": 0,
        "letters_guessed": set(),
        "hidden_word": ["[ ]"] * len(answer)
    }

    msg = await ctx.send(
        f"Hangman gestartet!\n"
        f"```{hangman_art[0]}```\n"
        f"{' '.join(games[ctx.author.id]['hidden_word'])}",
        file=discord.File("img/default.jpg")
    )
    for emoji in image_map.keys():
        await msg.add_reaction(emoji)


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

    if wrong_guesses == len(hangman_art) - 1:

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
    await ctx.send("die Idee nieder")



@bot.event
async def on_reaction_add(reaction, user):

    if user.bot:
        return

    message = reaction.message
    emoji = str(reaction.emoji)

    image_map = {
        "🐱": "img/rosi.jpg",
        "🔥": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzY1YXEzbjNpcDFiNjNzajQ3MXgyYWU4NzJ4MDNvc25sOG1lZzE3aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kucy3N9OuBSFvvFxiZ/giphy.gif"
    }

    # =====================================
    # DOUBLE EMOJI COMBO
    # =====================================



    if message.id in combo_triggered_messages:
        return

    reaction_emojis = [str(r.emoji) for r in message.reactions]

    if (
            "6️⃣" in reaction_emojis
            and "7️⃣" in reaction_emojis
            and message.id not in combo_triggered_messages
    ):
        combo_triggered_messages.add(message.id)

        await message.channel.send(
            "https://tenor.com/view/67-6767-676767-cat67-cat-gif-18345003009543756801"
        )

        return
    # =====================================
    # NORMAL EMOJI CHECK
    # =====================================

    if emoji not in image_map:
        return

    image = image_map[emoji]

    # =====================================
    # BOT MESSAGE = EDIT ONLY
    # =====================================

    if message.author == bot.user:

        # LOCAL FILE
        if image.startswith("img/"):

            filename = os.path.basename(image)

            file = discord.File(
                image,
                filename=filename
            )

            embed = discord.Embed(
                description=f"{emoji} by {user.display_name}"
            )

            embed.set_image(
                url=f"attachment://{filename}"
            )

            await message.edit(
                embed=embed,
                attachments=[file]
            )

        # URL IMAGE / GIF
        else:

            embed = discord.Embed(
                description=f"{emoji} by {user.display_name}"
            )

            embed.set_image(url=image)

            await message.edit(
                embed=embed,
                attachments=[]
            )

    # =====================================
    # NON-BOT MESSAGE = SEND NEW IMAGE
    # =====================================

    else:

        # LOCAL FILE
        if image.startswith("img/"):

            await message.channel.send(
                file=discord.File(image)
            )

        # URL IMAGE
        else:

            await message.channel.send(image)

bot.run(
    token,
    log_handler=handler,
    log_level=logging.DEBUG
)