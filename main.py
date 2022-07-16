import discord
import random

TOKEN = "OTk3NjI3NTI2NTM0OTM0NjQ4.GOfOOJ.KURkQcGcz6EMqzP94FP2JzYYbNXx_vkqmuStyM"

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready {0.user}".format(client))

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
        elif user_message.lower() == "!random":
            response = f"This is your random number: {random.randrange(100)}"
            await message.channel.send(response)
            return

    if user_message.lower() == "!anywhere":
        await message.channel.send("This can be used anywhere!")
        return


client.run(TOKEN)