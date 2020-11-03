from discord.ext import commands
import discord
import cybereco
import json


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
        await ctx.send(
            f"Success! Users will now gain `{rates}` {guild.money_symbol} for every 1 {guild.money_symbol} they find!")

    @guild.command(aliases=['um'])
    async def update_money(self, ctx, symbol: str = "😳"):
        guild = ctx.eco_guild
        guild.update_symbol(symbol=symbol)
        await ctx.send(f"Success! The money symbol for {ctx.guild} has been changed to `{symbol}`!")

    @commands.command()
    async def tools(self, ctx):
        embed = discord.Embed(title="Tools")
        embed.set_footer(text=f"Use {ctx.prefix}purchase tool [Ship ID] to purchase new ships!")
        data = json.load(open('info.json'))
        for x in data['Tools']:
            embed.add_field(name=f"__{x['name']}__", value=f"**Power:** {x['power']}\n**ID:** `{x['id']}`")
        await ctx.send(embed=embed)

    @commands.command()
    async def member(self, ctx, user: discord.Member = None):
        if not user:
            return await ctx.send(f"{ctx.eco_author}")
        else:
            return await ctx.send(f"{cybereco.Member(user_id=user.id, guild_id=ctx.guild.id)}")

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        embed = discord.Embed(title='Leaderboard')
        guild = ctx.eco_guild
        for member in sorted(guild.members, key=lambda x: x.balance, reverse=True):
            real = discord.utils.find(lambda x: str(x.id) == member.u_id, ctx.guild.members)
            embed.add_field(name=f"{real}", value=f"**{member.balance:,}** {guild.money_symbol}", inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def work(self, ctx):
        balance = ctx.eco_author.update_balance(100)
        await ctx.send(f"**{ctx.author}**, you just gained **{balance}** {ctx.eco_guild.money_symbol}!")



def setup(bot):
    bot.add_cog(Cog(bot))
