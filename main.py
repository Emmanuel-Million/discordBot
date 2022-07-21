import discord
import random
from discord.ext import commands
import datetime
import wikipedia
import requests
import yaml
from googletrans import Translator

conf = yaml.full_load(open('accessCode.yml'))
IPcode = conf['user']['IPcode'] 
token = conf['user']['token']
Wcode = conf['user']['Wcode']

with open("langCodes.txt", "r") as f:
    langCodes = [line.strip() for line in f]
langCodes = '\n'.join(langCodes)

client = discord.Client()
client = commands.Bot(command_prefix = '!', case_insensitive=True)

client.remove_command('help')

#Bot ready
@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))
    time = datetime.datetime.now()
    print(time.strftime("%A %B %d,  %Y  %I:%M %p"))

#Help command
@client.command()
async def help(ctx):
    help_content =  """__**General commands**__
                    **help** - Displays all working commands.
                    **time** - Displays current users time.
                    **ping** - Displays current users ping.
                    **roll** - Rolls a 100 sided dice and generates a random number [1-100].
                    \n__**Translation commands**__
                    **tl** - Translate following text into english
                    **tlto** - Destination language and text and translates
                    **lc** - Shows all langauage codes for tlto command
                    \n__**Unique commands**__
                    **ip** - Takes in IP Address and displays relevant information.
                    **define** - Takes in keyword and prints out Wiki search page summary .
                    **weather** - Takes in 'City' or 'City, Country' and displays current weather information."""

    embed_help = discord.Embed(title="__**Commands**__", description=help_content)
    embed_help.set_footer(text="Prefix for all commands is '!' All commands are not case sensitive.")
    await ctx.send(content=None, embed=embed_help)
    print("Unit1: Displayed")
#User Time command
@client.command()
async def time(ctx):
    x = datetime.datetime.now()
    await ctx.send(x.strftime("%A %B %d,  %Y  %I:%M %p"))

#User Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f"ping = {round(client.latency * 100)} ms")

#Dice roll command
@client.command()
async def roll(ctx):
    await ctx.send(f"You rolled a {random.randrange(101)}")

#IP search command
@client.command()
async def ip(ctx, *, ipaddr):
    try:
        r = requests.get(f"https://extreme-ip-lookup.com/json/{ipaddr}?key={IPcode}")
        geo = r.json()
    
        embed_dox = discord.Embed()

        embed_dox.add_field(name="IP", value=geo["query"], inline=True)
        embed_dox.add_field(name="IP Type", value=geo["ipType"], inline=True)
        embed_dox.add_field(name="Country", value=geo["country"], inline=True)
        embed_dox.add_field(name="City", value=geo["city"], inline=True)
        embed_dox.add_field(name="Continent", value=geo["continent"], inline=True)
        embed_dox.add_field(name="IP Name", value=geo["ipName"], inline=True)
        embed_dox.add_field(name="ISP", value=geo["isp"], inline=True)
        embed_dox.add_field(name="Latitude", value=geo["lat"], inline=True)
        embed_dox.add_field(name="Longitude", value=geo["lon"], inline=True)
        embed_dox.add_field(name="Org", value=geo["org"], inline=True)
        embed_dox.add_field(name="Region", value=geo["region"], inline=True)
        embed_dox.add_field(name="Status", value=geo["status"], inline=True)

        embed_dox.timestamp = datetime.datetime.utcnow()
        embed_dox.set_footer(text="\u200b")

        await ctx.send(content=None, embed=embed_dox)
        print(f"Unit1: Dox Successful for IP: {ipaddr}")
    
    except:
        embed_QueryError = discord.Embed(title="Query Error", description="Invalid IP. Try another search.")
        await ctx.send(content=None, embed=embed_QueryError)
        print("Unit1: Query Error")

#Weather command
@client.command()
async def weather(ctx, *, city):
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={Wcode}&q={city}")
        data = r.json()
        main = data["main"]

        temp = main['temp']
        temp_c =int(round(temp - 273.15))
        temp_f =  round((temp_c * 1.8) + 32)
        pressure = main['pressure']
        humidity = main['humidity']

        weather = data["weather"]
        description = weather[0]['description']

        embed_weather = discord.Embed(title=(f"__**Weather in {city}**__"))
        embed_weather.add_field(name="Description", value=description, inline=False)
        embed_weather.add_field(name="Temperature (C)", value=temp_c, inline=False)
        embed_weather.add_field(name="Temperature (F)", value=temp_f, inline=False)
        embed_weather.add_field(name="Humidity", value=(f"{humidity} %"), inline=True)
        embed_weather.add_field(name="Pressure", value=(f"{pressure} hPa"), inline=True)

        embed_weather.timestamp = datetime.datetime.utcnow()
        embed_weather.set_footer(text="\u200b")

        await ctx.send(content=None, embed=embed_weather)
        print(f"Unit1: Weather Search successful for {city}")
    except:
        embed_LocationError = discord.Embed(title="Location Error", description="Invalid Location. Try searching 'City, Country'.")
        await ctx.send(content=None, embed=embed_LocationError)
        print("Unit1: Location Error")

#Translate to EN command
@client.command()
async def tl(ctx, *, text):
    translator = Translator()
    result = translator.translate(text)
    embed_tl = discord.Embed(title="__**Translating to en**__", description=result.text)
    await ctx.send (content=None, embed=embed_tl)
    print("Unit1: Translation successful")

#Translate from EN to any language command
@client.command()
async def tlto(ctx, dest,  *, text):
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest)
        embed_tlto = discord.Embed(title=(f"__**Translating to {dest}**__"), description=result.text)
        await ctx.send (content=None, embed=embed_tlto)
        print("Unit1: Translation successful")
    except:
        embed_error = discord.Embed(title="__**Invalid Destination Info**__", description="Remember to type the destination langauge **BEFORE** your desired text \nType ' !lc ' to see all langauge codes")
        await ctx.send (content=None, embed=embed_error)
        print("Unit1: Invalid langauage code")

#Show language codes command
@client.command()
async def lc(ctx):
    embed_lc = discord.Embed(title="__**Language codes**__", description=langCodes)
    await ctx.send (content=None, embed=embed_lc)
    print("Unit1: Language Codes Shown")

# Chat Log, Bot Reaction, Wiki Search
@client.event
async def on_message(message):

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    #Keep bot from responding to self
    if message.author == client.user:
        return

    if message.channel.name == "general":
        if user_message.startswith(("I'm", "im", "Im")):
            name = user_message.split(" ", 1)[1]
            await message.channel.send(f"Hi {name}, I'm a Bot.")
            return

    if user_message.startswith("!define"):
        search = user_message.split(" ", 1)[1]
        try:
            result = wikipedia.summary(search, sentences = 3, auto_suggest = False, redirect = True)
            embed_result = discord.Embed(title=(f"__**Searching {search}...**__"), description=result)
            await message.channel.send(content=None, embed=embed_result)
            print(f"Unit1: Defined '{search}'")
            return

        except(wikipedia.exceptions.PageError): 
            embed_PageError = discord.Embed(title="__**Incorrect Page ID**__", description="Page ID does not match any pages. Try another search.")
            await message.channel.send(content=None, embed=embed_PageError)
            print("Unit1: Incorrect Page ID Error")
            return

        except wikipedia.exceptions.DisambiguationError as e:
            embed_DisambiguationError = discord.Embed(title="__**Ambiguous Search Error**__.", description=e)
            await message.channel.send(content=None, embed=embed_DisambiguationError)
            print("Unit1: Disambiguation Message")
            return

    await client.process_commands(message)

client.run(token)