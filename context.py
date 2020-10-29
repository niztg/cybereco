from discord.ext import commands
import cybereco


class Context(commands.Context):
    @property
    def eco_guild(self) -> cybereco.Guild:
        return cybereco.Guild(self.guild.id)
