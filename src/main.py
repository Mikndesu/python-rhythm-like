import discord
import pytube
import os

TOKEN=os.getenv("TOKEN")

test_url="https://www.youtube.com/watch?v=WWB01IuMvzA"

client = discord.Client()

def youtube_dl(url):
    yt = pytube.YouTube(url)
    stream = yt.streams.get_by_itag(251).download("aaa.mp3")


@client.event
async def on_ready():
    print('Logged in.')


@client.event
async def on_message(message):
    youtube_dl(test_url)

    if message.author.bot:
        return

    if message.content == "!join":
        if message.author.voice is None:
            await message.channel.send("You aren't currently connected to a Voice Channel.")
            return
        await message.author.voice.channel.connect()
        await message.channel.send("Connected.")
        vc = await client.channel.connect()
        vc.play(discord.FFmpegPCMAudio('aaa.mp3'), after=lambda e: print('done', e))

    if message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("Unconneted.")
            return
        await message.guild.voice_client.disconnect()
        await message.channel.send("Disconnected.")

client.run(TOKEN)