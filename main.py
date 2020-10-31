from discord.ext import commands
from discord import Intents
from config import token
from context import Context

import os

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

EXTENSIONS = ['cog', 'jishaku']


class Bot(commands.Bot):
    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def on_ready(self):
        for ext in EXTENSIONS:
            self.load_extension(ext)
        print("AAA")

    def run(self, *args, **kwargs):
        super().run(token)


Bot(command_prefix=";", intents=Intents.all()).run()
