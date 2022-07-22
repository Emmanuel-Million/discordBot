import discord
import random
from discord.ext import commands
import datetime
import wikipedia
import requests
import yaml
from googletrans import Translator
import praw
import pytz
from geopy import geocoders


conf = yaml.full_load(open('accessCode.yml'))
IPcode = conf['user']['IPcode'] 
token = conf['user']['token']
Wcode = conf['user']['Wcode']
clientId = conf['user']['clientId']
clientSecret = conf['user']['clientSecret']
username = conf['user']['username']
password = conf['user']['password']

reddit = praw.Reddit(check_for_async=False,
                    client_id=clientId,
                    client_secret=clientSecret,
                    username=username,
                    password=password,
                    user_agent="DiscordPythonBot")

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
                    **pfp** - Gets @'ed users discord avatar and displays it.
                    \n__**Translation commands**__
                    **tl** - Translate following text into english
                    **tlto** - Destination language and text and translates
                    **lc** - Shows all langauage codes for tlto command
                    \n__**Anime commands**__
                    **animeme** - Displays reddit posts from r/Animemes. 
                    **animewallpaper** - Displays reddit posts from r/Animewallpaper.
                    \n__**Unique commands**__
                    **ip** - Takes in IP Address and displays relevant information.
                    **define** - Takes in keyword and prints out Wiki search page summary .
                    **weather** - Takes in 'City' or 'City, State/Country' and displays current weather information."""

    embed_help = discord.Embed(title="__**Commands**__", description=help_content)
    embed_help.set_footer(text="Prefix for all commands is '!' All commands are not case sensitive.")
    await ctx.send(content=None, embed=embed_help)
    print("Unit1: Displayed")

#User Time command
@client.command()
async def time(ctx, *, city=None):
    

    if city is None:
        time = datetime.datetime.now()
        await ctx.send(time.strftime("%A %B %d,  %Y  %I:%M %p"))
    else:
        gn = geocoders.GeoNames()
        coord = gn.geocode(city)
        print(coord)

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

        await ctx.send(content=None, embed=embed_dox)
        print(f"Unit1: Dox Successful for IP: {ipaddr}")
    
    except:
        embed_QueryError = discord.Embed(title="Query Error", description="Invalid IP. Try another search.")
        await ctx.send(content=None, embed=embed_QueryError)
        print("Unit1: Query Error")

#IP search command Error handling
@ip.error
async def ip_error(ctx, error):
    embed_ipError = discord.Embed(title="Mising Ip", description="The IP after the command is missing.")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=embed_ipError)
        print("Unit1: Invalid ip")

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

        embed_weather = discord.Embed(title=(f"Weather in {city}"))
        embed_weather.add_field(name="Description", value=description, inline=False)
        embed_weather.add_field(name="Temperature (C)", value=temp_c, inline=False)
        embed_weather.add_field(name="Temperature (F)", value=temp_f, inline=False)
        embed_weather.add_field(name="Humidity", value=(f"{humidity} %"), inline=True)
        embed_weather.add_field(name="Pressure", value=(f"{pressure} hPa"), inline=True)

        await ctx.send(content=None, embed=embed_weather)
        print(f"Unit1: Weather Search successful for {city}")
    except:
        embed_LocationError = discord.Embed(title="Location Error", description="Invalid Location. Try searching 'City, Country'.")
        await ctx.send(content=None, embed=embed_LocationError)
        print("Unit1: Location Error")

#Weather command Error handling
@weather.error
async def weather_error(ctx, error):
    embed_weatherError = discord.Embed(title="Mising location", description="The location (City / City,Country) for this command is missing.")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=embed_weatherError)
        print("Unit1: Invalid text")

#Translate to EN command
@client.command()
async def tl(ctx, *, text):
    translator = Translator()
    result = translator.translate(text)
    embed_tl = discord.Embed(description=result.text)
    await ctx.send (content=None, embed=embed_tl)
    print("Unit1: Translation successful")

#Translate from EN to any language command
@client.command()
async def tlto(ctx, dest,  *, text):
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest)
        embed_tlto = discord.Embed(description=result.text)
        await ctx.send (content=None, embed=embed_tlto)
        print("Unit1: Translation successful")
    except:
        embed_error = discord.Embed(title="Invalid Destination Info", description="Remember to type the destination langauge **BEFORE** your desired text \nType ' !lc ' to see all langauge codes")
        await ctx.send (content=None, embed=embed_error)
        print("Unit1: Invalid langauage code")

#Translate from EN to any language command Error handling 
@tlto.error
async def tlto_error(ctx, error):
    embed_tltoError = discord.Embed(title="Mising text", description="The text to be translated is missing.")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=embed_tltoError)
        print("Unit1: Invalid text")

#Animeme
@client.command()
async def animeme(ctx):
    subreddit = reddit.subreddit("Animemes")
    all_subs = []

    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    embed_reddit = discord.Embed(title = name)
    embed_reddit.set_image(url = url)

    await ctx.send(embed=embed_reddit)
    print("Unit1: Meme sent")

#Animewallpaper
@client.command()
async def animewallpaper(ctx):
    subreddit = reddit.subreddit("Animewallpaper")
    all_subs = []
    top = subreddit.top(limit = 50)
    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    embed_reddit = discord.Embed(title = name)
    embed_reddit.set_image(url = url)

    await ctx.send(embed=embed_reddit)
    print("Unit1: Wallpaper sent")

#Show language codes command
@client.command()
async def lc(ctx):
    embed_lc = discord.Embed(title="Language codes", description=langCodes)
    await ctx.send (content=None, embed=embed_lc)
    print("Unit1: Language Codes Shown")

#Profile picture command
@client.command()
async def pfp(ctx, member: discord.Member = None):
    if member is None:
        embed_emptyUserError = discord.Embed(title="Empty user", description="Make sure to @ a user after the command.")
        await ctx.send(embed=embed_emptyUserError)
        print("Unit1: Empty user")

    else:
        pfp = member.avatar_url
        embed_pfp = discord.Embed(title=member)
        embed_pfp.set_image(url = pfp)
        await ctx.send(embed=embed_pfp)
        print("Unit1: pfp sent")

#Profile picture command error handling
@pfp.error
async def pfp_error(ctx, error):
    embed_pfpError = discord.Embed(title="Invalid user", description="That user does not exist.")

    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send(embed=embed_pfpError)
        print("Unit1: Invalid user")

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
    
    #Bot response event
    if message.channel.name == "general":
        if user_message.startswith(("I'm", "im", "Im")):
            name = user_message.split(" ", 1)[1]
            await message.channel.send(f"Hi {name}, I'm a Bot.")
            return

    #Wiki search command
    if user_message.startswith("!define"):
        search = user_message.split(" ", 1)[1]
        try:
            result = wikipedia.summary(search, sentences = 3, auto_suggest = False, redirect = True)
            embed_result = discord.Embed(title=(f"Searching for {search}..."), description=result)
            await message.channel.send(content=None, embed=embed_result)
            print(f"Unit1: Defined '{search}'")
            return

        except(wikipedia.exceptions.PageError): 
            embed_PageError = discord.Embed(title="Incorrect Page ID*", description="Page ID does not match any pages. Try another search.")
            await message.channel.send(content=None, embed=embed_PageError)
            print("Unit1: Incorrect Page ID Error")

        except wikipedia.exceptions.DisambiguationError as e:
            embed_DisambiguationError = discord.Embed(title="Ambiguous Search Error.", description=e)
            await message.channel.send(content=None, embed=embed_DisambiguationError)
            print("Unit1: Disambiguation Message")

    await client.process_commands(message)

client.run(token)