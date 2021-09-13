import discord
import pytube
import os

TOKEN=os.getenv("TOKEN")

test_url="https://www.youtube.com/watch?v=WWB01IuMvzA"

client = discord.Client()

def youtube_dl(url):
    yt = pytube.YouTube(url)
    stream = yt.streams.get_by_itag(251).download(None, "aaa.webm")


@client.event
async def on_ready():
    print('Logged in.')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if "!join" in message.content:
        print("start processing")
        if message.author.voice is None:
            await message.channel.send("You aren't currently connected to a Voice Channel.")
            return
        videoId = message.content.replace("!join ", "")
        youtube_dl(f"https://www.youtube.com/watch?v={videoId}")
        await message.author.voice.channel.connect()
        await message.channel.send("Connected.")
        message.author.guild.voice_client.play(discord.FFmpegPCMAudio('/home/ubuntu/python-rhythm-like/aaa.webm'), after=lambda e: print('done', e))

    if message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("Unconneted.")
            return
        await message.guild.voice_client.disconnect()
        await message.channel.send("Disconnected.")

client.run(TOKEN)