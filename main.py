import discord
import random
from discord.ext import commands
import datetime
import wikipedia
import requests
import yaml

conf = yaml.full_load(open('accessCode.yml'))
IPcode = conf['user']['IPcode'] 
token = conf['user']['token']
Wcode = conf['user']['Wcode']


client = discord.Client()
client = commands.Bot(command_prefix = '!')

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
    help_content =  """\n\n***!help***    : Displays all working commands.
                    \n***!time***    : Displays current users time.
                    \n***!ping***    : Displays current users ping.
                    \n***!roll***    : Rolls a 100 sided dice and generates a random number [1-100].
                    \n***!dox***     : Takes in IP Address and displays relevant information.
                    \n***!define***  : Takes in keyword and prints out Wiki search page summary .
                    \n***!weather*** : Takes in 'City' or 'City, Country' and displays current weather information.
                    \n**If the Bot is suffering from delay, please be patient and/or wait for an admin to reboot.**"""

    embed_help = discord.Embed(title="Commands List...", description=help_content)
    await ctx.send(content=None, embed=embed_help)

#User Time command
@client.command()
async def time(ctx):
    x = datetime.datetime.now()
    await ctx.send(x.strftime("```%A %B %d,  %Y  %I:%M %p```"))

#User Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f"```ping = {round(client.latency * 100)} ms```")

#Dice roll command
@client.command()
async def roll(ctx):
    await ctx.send(f"```You rolled a {random.randrange(101)}```")

#IP search command
@client.command()
async def dox(ctx, *, ipaddr: str = "9.9.9.9"):
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
async def weather(ctx, *, city: str):
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

        embed_weather = discord.Embed(title=(f"Weather in {city}"))
        embed_weather.add_field(name="Description", value=description, inline=False)

        embed_weather.add_field(name="Temperature (C)", value=temp_c, inline=False)
        embed_weather.add_field(name="Temperature (F)", value=temp_f, inline=False)

        embed_weather.add_field(name="Humidity", value=(f"{humidity} %"), inline=True)
        embed_weather.add_field(name="Pressure", value=(f"{pressure} hPa"), inline=True)

        embed_weather.timestamp = datetime.datetime.utcnow()
        embed_weather.set_footer(text="\u200b")

        await ctx.send(content=None, embed=embed_weather)
    except:
        embed_LocationError = discord.Embed(title="Location Error", description="Invalid Location. Try searching 'City, Country'.")
        await ctx.send(content=None, embed=embed_LocationError)
        print("Unit1: Location Error")
    
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
            embed_DisambiguationError = discord.Embed(title="Ambiguous Search Error.", description=e)
            await message.channel.send(content=None, embed=embed_DisambiguationError)
            print("Unit1: Disambiguation Message")
            return

    await client.process_commands(message)

client.run(token)