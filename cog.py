from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def guild(self, ctx):
        await ctx.send(f"{ctx.eco_guild}")

    @guild.command(aliases=['ur'])
    async def update_rates(self, ctx, rates: float = 1.25):
        guild = ctx.eco_guild
        guild.update_rates(rates=rates)
        await ctx.send(f"Success! Users will now gain `{rates}` {guild.money_symbol} for every 1 {guild.money_symbol} they find!")

    @guild.command(aliases=['um'])
    async def update_money(self, ctx, symbol: str = "😳"):
        guild = ctx.eco_guild
        guild.update_symbol(symbol=symbol)
        await ctx.send(f"Success! The money symbol for {ctx.guild} has been changed to `{symbol}`!")


def setup(bot):
    bot.add_cog(Cog(bot))