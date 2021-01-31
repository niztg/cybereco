from discord.ext import commands
import discord
import cybereco
import json
import aiohttp
import random
import asyncio
from aiotrivia import TriviaClient
from contextlib import suppress
from async_timeout import timeout

HANGMAN_STATES = {
    0: '''```
  +---+
  |   |
      |
      |
      |
      |
=========```''',
    1: '''```
  +---+
  |   |
  O   |
      |
      |
      |
=========```''',
    2: '''```
  +---+
  |   |
  O   |
  |   |
      |
      |
=========```''',
    3: '''```
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========```''',
    4: '''```
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========```''',
    5: '''```
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========```''',
    6: '''```
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========```'''
}

WEAPONS = [
    " Sword of Mega Doom",
    " Epic Gun",
    " Mega Epic Gun",
    " Grenade",
    " Amazing Bruh Machine",
    " Gun Lmao",
    " Hyper Epic Gun",
    " 'Not even trying at this point' Rifle",
    " Grand Sword of Chaos",
    " Excalibur",
    " Master Sword",
    " Storm Pegasus",
    " Rock Leone",
    " Lightning L-Drago"
]

QUIPS = ["What two words would passengers never want to hear a pilot say?",
         "You would never go on a roller coaster called _____",
         "The secret to a happy life",
         "If a winning coach gets Gatorade dumped on his head, what should get dumped on the losing coach?",
         "Name a candle scent designed specifically for Kim Kardashian",
         "You should never give alcohol to ______",
         "Everyone knows that monkeys hate ______",
         "The biggest downside to living in Hell",
         "Jesus's REAL last words",
         "The worst thing for an evil witch to turn you into",
         "The Skittles flavor that just missed the cut",
         "On your wedding night, it would be horrible to find out that the person you married is ____",
         "A name for a really bad Broadway musical",
         "The first thing you would do after winning the lottery",
         "Why ducks really fly south in the winter",
         "America's energy crisis would be over if we made cars that ran on ______",
         "It's incredibly rude to ____ with your mouth open"
         "What's actually causing global warming?",
         "A name for a brand of designer adult diapers",
         "Name a TV drama that's about a vampire doctor",
         "Something squirrels probably do when no one is looking",
         "The crime you would commit if you could get away with it",
         "Come up with a great title for the next awkward teen sex movie",
         "What's the Mona Lisa smiling about?",
         "A terrible name for a cruise ship",
         "What FDR meant to say was We have nothing to fear, but _____",
         "Come up with a title for an adult version of any classic video game",
         "The name of a font nobody would ever use",
         "Something you should never put on an open wound"
         "Scientists say erosion, but we all know the Grand Canyon was actually made by _____",
         "The real reason the dinosaurs died"
         "Come up with the name of a country that doesn't exist",
         "The best way to keep warm on a cold winter night",
         "A college major you don't see at many universities",
         "What would make baseball more entertaining to watch?",
         "The best thing about going to prison",
         "The best title for a new national anthem for the USA",
         "Come up with the name of book that would sell a million copies, immediately",
         "What would you do if you were left alone in the White House for an hour?",
         "Invent a family-friendly replacement word that you could say instead of an actual curse word",
         "A better name for testicles",
         "The name of the reindeer Santa didn't pick to pull his sleigh",
         "What's the first thing you would do if you could time travel?",
         "The name of a pizza place you should never order from",
         "A not-very-scary name for a pirate",
         "Come up with a name for a beer made especially for monkeys",
         "The best thing about living in an igloo",
         "The worst way to be murdered",
         "Something you shouldn't get your significant other for Valentine's Day",
         "A dangerous thing to do while driving",
         "Something you shouldn't wear to a job interview",
         "The #1 reason penguins can't fly",
         "Using only two words, a new state motto for Texas",
         "The hardest thing about being Batman",
         "A great way to kill time at work",
         "Come up with a really bad TV show that starts with Baby",
         "Why does the Tower of Pisa lean?",
         "What's wrong with these kids today?",
         "A great new invention that starts with Automatic",
         "Come up with a really bad football penalty that begins with Intentional",
         "A Starbucks coffee that should never exist",
         "There's Gryffindor, Ravenclaw, Slytherin, and Hufflepuff, but what's the Hogwarts house few "
         "have ever heard of?",
         "The worst words to say for the opening of a eulogy at a funeral",
         "Something you should never use as a scarf",
         "Invent a holiday that you think everyone would enjoy",
         "The best news you could get today",
         "Usually, it's bacon,lettuce and tomato, but come up with a BLT you wouldn't want to eat",
         "The worst thing you could stuff a bed mattress with",
         "A great opening line to start a conversation with a stranger at a party",
         "Something you would like to fill a swimming pool with",
         "Miley Cyrus' Wi-Fi password, possibly",
         "If you were allowed to name someone else's baby any weird thing you wanted, "
         "what would you name it?",
         "A fun thing to think about during mediocre sex",
         "You know you're in for a bad taxi ride when _____",
         "Where do babies come from?",
         "The terrible fate of the snowman Olaf in a director's cut of 'Frozen'",
         "Sometimes, after a long day, you just need to ______",
         "The worst way to spell Mississippi",
         "Give me one good reason why I shouldn't spank you right now",
         "The best pick-up line for an elderly singles mixer",
         "A good stage name for a chimpanzee stripper",
         "The best place to bury all those bodies",
         "One place a finger shouldn't go",
         "Come up with a name for the most difficult yoga pose known to mankind",
         "What's lurking under your bed when you sleep?",
         "The name of a canine comedy club with puppy stand-up comedians",
         "A great name for a nude beach in Alaska",
         "Make up the title of a movie that is based on the first time you had sex",
         "A vanity license plate a jerk in an expensive car would get",
         "A good fake name to use when checking into a hotel",
         "A good catchphrase to yell every time you finish pooping",
         "Your personal catchphrase if you were on one of those 'Real Housewives' shows",
         "The Katy Perry Super Bowl halftime show would have been better with _____",
         "Okay... fine! What do YOU want to talk about then?!!!",
         "Miller Lite beer would make a lot of money if they came up with a beer called Miller Lite _____",
         "Something you should never stick up your butt",
         "A terrible name for a clown",
         "An inappropriate thing to do at a cemetery"]


class Fighter:
    def __init__(self, member: discord.Member):
        self.name = member.display_name
        self.health = 100
        self.self = member

    def update_heath(self, amt: int):
        self.health += amt
        return amt

    @property
    def dead(self):
        return self.health <= 0

    def heal(self):
        if self.health == 100:
            raise ValueError("You are already at max health, you can't heal now.")
        else:
            amt = 100 - self.health
            heal = random.randint(1, amt)
            self.update_heath(heal)
            return heal

    def __repr__(self):
        return "{0.name} ♥️ **{0.health}**".format(self)

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
