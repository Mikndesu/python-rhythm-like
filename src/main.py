import discord
from discord.ext import commands
import traceback
import pytube
import glob
import requests
import json
import os


INITIAL_EXTENSIONS = [
        "cogs.cog"
    ]

class Discord_bot(commands.Bot):


    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()


    async def on_ready(self):
        print('Logged in.')


    # async def on_message(self, message):
    #     if message.author.bot:
    #         return

    #     if "!join" in message.content:
    #         print("start processing")
    #         if message.author.voice is None:
    #             await message.channel.send("You aren't currently connected to a Voice Channel.")
    #             return
    #         title, id = self.search(message.content.replace("!join ", ""))
    #         await message.channel.send(f"Currently Playing: {title}")
    #         self.youtube_dl(f"https://www.youtube.com/watch?v={id}", title)
    #         await message.author.voice.channel.connect()
    #         isJoined = True
    #         message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
    #             f"/home/ubuntu/python-rhythm-like/{title}.webm"), after=lambda e: print('done', e))

    #     if "!play" in message.content:
    #         if isJoined is False:
    #             message.channel.send(
    #                 "You have to join any channels to execute this command")
    #         print("start processing")
    #         if message.author.voice is None:
    #             await message.channel.send("You aren't currently connected to a Voice Channel.")
    #             return
    #         title, id = self.search(message.content.replace("!join ", ""))
    #         await message.channel.send(f"Currently Playing: {title}")
    #         self.youtube_dl(f"https://www.youtube.com/watch?v={id}", title)
    #         message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
    #             f"/home/ubuntu/python-rhythm-like/{title}.webm"), after=lambda e: print('done', e))

    #     if message.content == "!stop":
    #         if self.isJoined is False:
    #             message.channel.send(
    #                 "You have to join any channels to execute this command")
    #         if self.isPlaying is False:
    #             message.channel.send(
    #                 "Music isn't now playing")
    #         self.isPlaying=False
    #         message.author.guild.voice_client.stop()

    #     if message.content == "!pause":
    #         if self.isJoined is False:
    #             message.channel.send(
    #                 "You have to join any channels to execute this command")
    #         if self.isPlaying is False:
    #             message.channel.send(
    #                 "Music isn't now playing")
    #         message.author.guild.voice_client.pause()

    #     if message.content == "!resume":
    #         if self.isJoined is False:
    #             message.channel.send(
    #                 "You have to join any channels to execute this command")
    #         if self.isPlaying is False:
    #             message.channel.send(
    #                 "Music isn't now playing")
    #         message.author.guild.voice_client.resume()

    #     if message.content == "!leave":
    #         if message.guild.voice_client is None:
    #             await message.channel.send("Unconneted.")
    #             return
    #         await message.guild.voice_client.disconnect()
    #         await message.channel.send("Disconnected.")

    #     if message.content == "!clean":
    #         file = glob.glob('*.webm')
    #         for i in file:
    #             os.remove(i)


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    bot = Discord_bot(command_prefix="!")
    bot.run(TOKEN)
