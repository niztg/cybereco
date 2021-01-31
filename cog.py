from discord.ext import commands
import discord
import cybereco
import json
import random
import asyncio



rarities = {
    0: "Common",
    1: "Rare",
    2: "Legendary"
}

items = {
    1: {"rarity": 0, "name": "Common Gun"},
    2: {"rarity": 1, "name": "Rare Sword"},
    3: {"rarity": 2, "name": "Legendary Fist"}
}

class Weapon:
    def __init__(self, item: int):
        info = items.get(item)
        self.rarity_raw = info.get("rarity")
        self.rarity = rarities.get(self.rarity_raw)
        self.name = info.get("name")

all_weapons = [Weapon(b) for b in items.keys()]
commons = random.choices([w for w in all_weapons if w.rarity_raw == 0], k=100)
rares = random.choices([w for w in all_weapons if w.rarity_raw == 1], k=25)
legendaries = random.choices([w for w in all_weapons if w.rarity_raw == 2], k=3)
total_chances = len(commons) + len(rares) + len(legendaries)
chooser = commons + rares + legendaries


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ppl = {} # {id: {0: []}, total_cases: 0}

    @commands.command()
    async def ppl(self, ctx):
        await ctx.send(str(self.ppl))

    @commands.group(aliases=['c'], invoke_without_command=True)
    async def case(self, ctx):
        await ctx.send(f"Percentage of common: {(len(commons)/total_chances)*100}%\nPercentage of Rare: {(len(rares)/total_chances)*100}%\nPercentage of legendaries: {(len(legendaries)/total_chances)*100}%")
        choice = random.choice(chooser)
        await asyncio.sleep(2)
        await ctx.send(f"{choice.name} - {choice.rarity}")
        id = ctx.author.id
        if id in self.ppl:
            self.ppl[id]['total_cases'] += 1
            try:
                self.ppl[id][choice.rarity_raw].append(choice)
            except:
                self.ppl[id][choice.rarity_raw] = [choice]
        else:
            self.ppl[id] = {choice.rarity_raw: [choice]}
            self.ppl[id]['total_cases'] = 1

    @case.command(aliases=['inv'])
    async def inventory(self, ctx):
        try:
            data = self.ppl[ctx.author.id]
        except:
            return await ctx.send("open some cases bruhv")
        common = f"Commons ({len(data[0])}):\n{', '.join([n.name for n in data[0]][:5])}..." if data.get(0) else None
        rare = f"Rares ({len(data[1])}):\n{', '.join([n.name for n in data[1]][:5])}..." if data.get(1) else None
        legendarie = f"Legendaries ({len(data[2])}):\n{', '.join([n.name for n in data[2]][:5])}..." if data.get(2) else None
        message = f"Total Cases opened: {data['total_cases']}\n\n"
        for x in [common, rare, legendarie]:
            if x:
                message += f"{x}\n"
            else:
                continue
        await ctx.send(message)



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
