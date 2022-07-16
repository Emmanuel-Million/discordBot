import discord
import random
from discord.ext import commands

TOKEN = "OTk3NjI3NTI2NTM0OTM0NjQ4.GOfOOJ.KURkQcGcz6EMqzP94FP2JzYYbNXx_vkqmuStyM"

client = discord.Client()
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def ping(ctx):
    await ctx.send(f"ping = {round(client.latency * 100)} ms")

@client.command()
async def roll(ctx):
    await ctx.send(f"You rolled a {random.randint(100)}")


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    if message.author ==client.user:
        return

    if message.channel.name == "general":
        if user_message.lower() == "hello":
            await message.channel.send(f"Hello {username} !")
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f"Goodbye {username} !")
            return

    if user_message.lower() == "!anywhere":
        await message.channel.send("This can be used anywhere!")
        return

    await client.process_commands(message)




client.run(TOKEN)