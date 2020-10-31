from discord.ext import commands
import cybereco


class Context(commands.Context):
    @property
    def eco_guild(self) -> cybereco.Guild:
        return cybereco.Guild(self.guild.id)

    @property
    def eco_author(self):
        return cybereco.Member(user_id=self.author.id, guild_id=self.guild.id)
