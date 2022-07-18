import discord
import random
from discord.ext import commands
import datetime
import wikipedia

with open("TOKEN.txt", "r", encoding="utf-8") as f:
    TOKEN = f.read()

client = discord.Client()
client = commands.Bot(command_prefix = '!')

client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))
    time = datetime.datetime.now()
    print(time.strftime("%A %B %d,  %Y  %I:%M %p"))

@client.command()
async def help(ctx):
    help_content = "\n\n***!help***   : Displays all working commands \n\n***!time***   : Displays current users time \n\n***!ping***   : Displays current users ping \n\n***!roll***   : Rolls a 100 sided dice and generates a random number [1-100] \n\n***!define*** : Searches keyword and prints out Wiki page summary \n\n**If the Bot is suffering from delay, please be patient and/or wait for an admin to reboot.**"
    embed_help = discord.Embed(title="Commands List...", description=help_content)
    await ctx.send(content=None, embed=embed_help)

@client.command()
async def time(ctx):
    x = datetime.datetime.now()
    await ctx.send(x.strftime("```%A %B %d,  %Y  %I:%M %p```"))

@client.command()
async def ping(ctx):
    await ctx.send(f"```ping = {round(client.latency * 100)} ms```")

@client.command()
async def roll(ctx):
    await ctx.send(f"```You rolled a {random.randrange(101)}```")

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

    #"I'm" bot reaction
    if message.channel.name == "general":
        if user_message.startswith(("I'm", "im", "Im")):
            name = user_message.split(" ", 1)[1]
            await message.channel.send(f"Hi {name}, I'm a Bot.")
            return

    # wikipedia search
    if user_message.startswith("!define"):
        search = user_message.split(" ", 1)[1]
        try:
            result = wikipedia.summary(search, sentences = 3, auto_suggest = False, redirect = True)
            embed_result = discord.Embed(title="Searching...", description=result)
            await message.channel.send(content=None, embed=embed_result)
            print(f"Unit1: Defined '{search}'")
            return

        except(wikipedia.exceptions.PageError): 
            embed_PageError = discord.Embed(title="Incorrect Page ID", description="Page ID does not match any pages. Try another search.")
            await message.channel.send(content=None, embed=embed_PageError)
            print("Unit1: Incorrect Page ID Error")
            return

        except wikipedia.exceptions.DisambiguationError as e:
            embed_DisambiguationError = discord.Embed(title="Ambiguous Search Error", description=e)
            await message.channel.send(content=None, embed=embed_DisambiguationError)
            print("Unit1: Disambiguation Message")
            return

    await client.process_commands(message)

client.run(TOKEN)