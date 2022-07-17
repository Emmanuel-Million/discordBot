import discord
import random
from discord.ext import commands
import datetime
import wikipedia

TOKEN = "OTk3NjI3NTI2NTM0OTM0NjQ4.GOfOOJ.KURkQcGcz6EMqzP94FP2JzYYbNXx_vkqmuStyM"

client = discord.Client()
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))
    time = datetime.datetime.now()
    print(time)

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def time(ctx):
    await ctx.send(datetime.datetime.now())

@client.command()
async def ping(ctx):
    await ctx.send(f"ping = {round(client.latency * 100)} ms")

@client.command()
async def roll(ctx):
    await ctx.send(f"You rolled a {random.randrange(101)}")

@client.command()
async def fgo(ctx, arg):
    await ctx.send(f"https://gamepress.gg/grandorder/servant/{arg}")

@client.event
async def on_message(message):

    # chat log
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    # keeps bot from responding to itself
    if message.author == client.user:
        return

    if message.channel.name == "general":
        if user_message.lower() == "hello":
            await message.channel.send(f"Hello {username} !")
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f"Goodbye {username} !")
            return

    # wikipedia search
    if user_message.startswith("!define"):
        search = user_message[8:]
        try:
            result = wikipedia.summary(search, sentences = 3, auto_suggest = False, redirect = True)
            embed_result = discord.Embed(title="Searching...", description=result, color=discord.Color.blue())
            await message.channel.send(content=None, embed=embed_result)
            return
        except(wikipedia.exceptions.PageError): 
            await message.channel.send(f"Page id {search} does not match any pages. Try another search.")
            return

    await client.process_commands(message)

client.run(TOKEN)