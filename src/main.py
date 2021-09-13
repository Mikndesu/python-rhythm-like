import discord
import os

TOKEN=os.getenv("PUBLIC_KEY")

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in.')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "/example":
        await message.channel.send("Succeeded")

client.run(TOKEN)