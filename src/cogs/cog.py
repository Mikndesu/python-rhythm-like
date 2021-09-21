from discord.ext import commands
import discord
import pytube
import requests
import json
import os
import glob
import time

current_path = "/home/ubuntu/python-rhythm-like/"
# "/home/ubuntu/python-rhythm-like/"


class Cog_Rhythm_like(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_APIKEY = os.getenv("YOUTUBE_APIKEY")
        self.isJoined = False
        self.isPlaying = False

    def youtube_dl(self, id):
        ut = int(time.time())
        yt = pytube.YouTube(f"https://www.youtube.com/watch?v={id}")
        yt.streams.get_by_itag(251).download(None, f"{ut}.webm")
        return ut

    def search(self, search_query):
        result_amount = 5
        api_response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&maxResults={result_amount}&key={self.YOUTUBE_APIKEY}"
        ).text
        jsonObj = json.loads(api_response)
        title_and_id = ()
        for i in jsonObj["items"]:
            title_and_id = (i["snippet"]["title"], i["id"]["videoId"])
            break
        return title_and_id

    @commands.command()
    async def join(self, ctx, args=None):
        if self.isJoined is True:
            await ctx.send("This Bot is Joined already!")
        if args is None:
            await ctx.send("Joined without playing music.")
            await ctx.message.author.voice.channel.connect()
            self.isJoined = True
            return
        music_name = ctx.message.content.replace("!join ", "")
        title, id = self.search(music_name)
        file_name = self.youtube_dl(id)
        await ctx.message.author.voice.channel.connect()
        self.isJoined = True
        ctx.message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
            f"{current_path}/{file_name}.webm"), after=lambda e: print('done', e))
        print(title)

    @commands.command()
    async def play(self, ctx, args=None):
        if args is None:
            await ctx.send("This command requires a music name.")
            return
        music_name = ctx.message.content.replace("!play ", "")
        title, id = self.search(music_name)
        file_name = self.youtube_dl(id)
        if self.isJoined is False:
            await ctx.message.author.voice.channel.connect()
            self.isJoined = True
        ctx.message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
            f"{current_path}/{file_name}.webm"), after=lambda e: print('done', e))
        print(title)


    @commands.command()
    async def clean(self, ctx):
        file = glob.glob('*.webm')
        for i in file:
            os.remove(i)
        print("clean")

    
    @commands.command()
    async def leave(self, ctx, args=None):
        if ctx.message.guild.voice_client is None:
                await ctx.message.channel.send("Unconneted.")
                return
        await ctx.message.guild.voice_client.disconnect()
        await ctx.message.channel.send("Disconnected.")
        self.isJoined = False
        self.isPlaying = False


    @commands.command()
    async def stop(self, ctx):
        if self.isJoined is False:
            ctx.message.channel.send(
                "You have to join any channels to execute this command")
            return
        if self.isPlaying is False:
            ctx.message.channel.send(
                "Music isn't now playing")
            self.isPlaying = False
            ctx.message.author.guild.voice_client.stop()


    @commands.command()
    async def pause(self, ctx):
        if self.isJoined is False:
            ctx.message.channel.send(
                "You have to join any channels to execute this command")
            return
        if self.isPlaying is False:
            ctx.message.channel.send(
                "Music isn't now playing")
            ctx.message.author.guild.voice_client.pause()


    @commands.command()
    async def resume(self, ctx):
        if self.isJoined is False:
            ctx.message.channel.send(
                "You have to join any channels to execute this command")
        if self.isPlaying is False:
            ctx.message.channel.send(
                "Music isn't now playing")
        ctx.message.author.guild.voice_client.resume()
        self.isPlaying = False


def setup(bot):
    bot.add_cog(Cog_Rhythm_like(bot))
