from discord.ext import commands
import traceback
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


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    bot = Discord_bot(command_prefix="!")
    bot.run(TOKEN)
