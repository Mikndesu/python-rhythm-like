import discord
import pytube
import glob
import requests
import json
import os


class Discord_bot:

    TOKEN = os.getenv("TOKEN")
    YOUTUBE_APIKEY = os.getenv("YOUTUBE_APIKEY")
    isPlaying = False
    isJoined = False

    client = discord.Client()


    def youtube_dl(self, url, title):
        yt = pytube.YouTube(url)
        yt.streams.get_by_itag(251).download(None, f"{title}.webm")


    def search(self, search_query):
        result_amount = 5
        api_response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&maxResults={result_amount}&key={self.YOUTUBE_APIKEY}").text
        jsonObj = json.loads(api_response)
        title_and_id = ()
        for i in jsonObj["items"]:
            print(i["snippet"]["title"])
            title_and_id = (i["snippet"]["title"], i["id"]["videoId"])
            break
        return title_and_id


    @client.event
    async def on_ready(self):
        print('Logged in.')


    @client.event
    async def on_message(self, message):
        if message.author.bot:
            return

        if "!join" in message.content:
            print("start processing")
            if message.author.voice is None:
                await message.channel.send("You aren't currently connected to a Voice Channel.")
                return
            title, id = self.search(message.content.replace("!join ", ""))
            await message.channel.send(f"Currently Playing: {title}")
            self.youtube_dl(f"https://www.youtube.com/watch?v={id}", title)
            await message.author.voice.channel.connect()
            isJoined = True
            message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
                f"/home/ubuntu/python-rhythm-like/{title}.webm"), after=lambda e: print('done', e))

        if "!play" in message.content:
            if isJoined is False:
                message.channel.send(
                    "You have to join any channels to execute this command")
            print("start processing")
            if message.author.voice is None:
                await message.channel.send("You aren't currently connected to a Voice Channel.")
                return
            title, id = self.search(message.content.replace("!join ", ""))
            await message.channel.send(f"Currently Playing: {title}")
            self.youtube_dl(f"https://www.youtube.com/watch?v={id}", title)
            message.author.guild.voice_client.play(discord.FFmpegPCMAudio(
                f"/home/ubuntu/python-rhythm-like/{title}.webm"), after=lambda e: print('done', e))

        if message.content == "!stop":
            if self.isJoined is False:
                message.channel.send(
                    "You have to join any channels to execute this command")
            if self.isPlaying is False:
                message.channel.send(
                    "Music isn't now playing")
            self.isPlaying=False
            message.author.guild.voice_client.stop()

        if message.content == "!pause":
            if self.isJoined is False:
                message.channel.send(
                    "You have to join any channels to execute this command")
            if self.isPlaying is False:
                message.channel.send(
                    "Music isn't now playing")
            message.author.guild.voice_client.pause()

        if message.content == "!resume":
            if self.isJoined is False:
                message.channel.send(
                    "You have to join any channels to execute this command")
            if self.isPlaying is False:
                message.channel.send(
                    "Music isn't now playing")
            message.author.guild.voice_client.resume()

        if message.content == "!leave":
            if message.guild.voice_client is None:
                await message.channel.send("Unconneted.")
                return
            await message.guild.voice_client.disconnect()
            await message.channel.send("Disconnected.")

        if message.content == "!clean":
            file = glob.glob('*.webm')
            for i in file:
                os.remove(i)


if __name__ == "__main__":
    bot = Discord_bot()
    bot.client.run(bot.TOKEN)

