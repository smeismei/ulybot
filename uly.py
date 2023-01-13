import discord
from discord.ext import commands
import tenor
import random
import asyncio
import requests
import randomjoke
from discord import FFmpegPCMAudio
from config import ULYTOKEN
import sqlite
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="&", description="""funky command!""", intents=intents
)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print("---------------------------------")
    print("Servers connected to:")
    for guild in bot.guilds:
        print(guild.name)
    print("---------------------------------")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "among" in message.content.lower():
        gif = tenor.random_gif("among us")
        await message.channel.send(gif)

    if "git" in message.content.lower():
        await message.channel.send("got")

    if "cat" in message.content.lower() or "kitty" in message.content.lower():
        gif = tenor.random_gif("kitty")
        await message.channel.send(gif)

    if "yippee" in message.content.lower():
        gif = tenor.random_gif("autism creature")
        await message.channel.send(gif)

    if "pepsi" in message.content.lower():
        with open("assets/video.mp4", "rb") as f:
            video = discord.File(f)
            await message.channel.send(file=video)

    if "anni" in message.content.lower() or "pizza" in message.content.lower():
        with open("assets/kissa.png", "rb") as f:
            image = discord.File(f)
            await message.channel.send(file=image)

    if "slay" in message.content.lower():
        with open("assets/jerma.mp4", "rb") as f:
            video = discord.File(f)
            await message.channel.send(file=video)

    if random.randint(1, 5) == 1 and "peli" in message.content.lower():
        try:
            with open("assets/call.mp4", "rb") as f:
                video = discord.File(f)
                await message.channel.send(file=video)
        except discord.errors.Forbidden:
            pass

    await bot.process_commands(message)


@bot.command()
async def joke(ctx):
    await ctx.send(
        f"<:bleh:1063451486484443267> {randomjoke.get_joke()} <:bleh:1063451486484443267>"
    )


@bot.command()
async def sniff(ctx: commands.Context):
    if isinstance(ctx.author, discord.Member) and ctx.author.voice:
        channel = ctx.author.voice.channel
        if channel:
            try:
                voice = await channel.connect()
            except discord.ClientException:
                await ctx.send("I am already sniffing.")
                return
            msg = await ctx.send("<a:catsniff:1063491145365192775>")

            def my_after(error):
                coro = voice.disconnect()
                fut = asyncio.run_coroutine_threadsafe(coro, voice.loop)
                fut2 = asyncio.run_coroutine_threadsafe(msg.delete(), voice.loop)
                try:
                    fut.result()
                    fut2.result()
                except:
                    pass

            source = FFmpegPCMAudio("assets/sniff.mp3")
            player = voice.play(source, after=my_after)

    else:
        await ctx.send("You need to join a voice channel first!")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel!")
    else:
        await ctx.send("I am currently not in a voice channel!")


@bot.command()
async def guess(ctx):
    await ctx.send("Guess a number between 1 and 10.")

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await bot.wait_for("message", check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.send(f"Time's up! It was {answer}. Better luck next time.")

    if int(guess.content) == answer:
        await ctx.send("YIPPEE!!")
    else:
        await ctx.send(f"Fuckoboingo! It's actually {answer}!")


@bot.command(aliases=["forage", "pick"])
async def berry(ctx):
    row = sqlite.select_berries(ctx.author.id)
    if row is not None:
        now = datetime.now().timestamp()
        seconds = now - row[1]
        cooldown = 10
        if seconds < cooldown:
            await ctx.send(
                f"Give the berries time to grow! **Try again in {int(cooldown - seconds)} seconds.**"
            )
            return
    amount = random.randint(1, 50)
    sqlite.add_berries(ctx.author.id, amount)
    await ctx.send(f"You foraged **{amount} berries!** :blueberries:")


bot.run(ULYTOKEN)
