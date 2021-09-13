import discord
import os

TOKEN=os.getenv("TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in.')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("You aren't currently connected to a Voice Channel.")
            return
        await message.author.voice.channel.connect()
        await message.channel.send("Connected.")

    if message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("Unconneted.")
            return
        await message.guild.voice_client.disconnect()
        await message.channel.send("Disconnected.")

client.run(TOKEN)