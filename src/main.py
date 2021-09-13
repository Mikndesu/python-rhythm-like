import discord
import pytube
import os

TOKEN=os.getenv("TOKEN")

test_url="https://www.youtube.com/watch?v=WWB01IuMvzA"

client = discord.Client()

def youtube_dl(url):
    youtube = pytube.YouTube(url).streams.first().download("aaa.mp4")


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
        voice_ch = await client.join_voice_channel(client.get_channel("Discord voice channel ID"))
        youtube_dl(test_url)
        player = voice_ch.create_ffmpeg_player("aaa.mp3")
        player.start()

    if message.content == "!leave":
        if message.guild.voice_client is None:
            await message.channel.send("Unconneted.")
            return
        await message.guild.voice_client.disconnect()
        await message.channel.send("Disconnected.")

client.run(TOKEN)