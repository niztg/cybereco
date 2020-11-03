import json
from .exceptions import InvalidID
from .functions import *

__all__ = (
    'Guild',
    'Member',
    'Tool'
)

FILENAME = 'data.json'
INFO = 'info.json'


class Guild:
    def __init__(self, guild_id: int):

        guild_id = str(guild_id)
        if (not len(guild_id) == 18) or (not guild_id.isdigit()):
            raise InvalidID()

        if not guild_exists(int(guild_id)):
            data = create_guild(int(guild_id))
        else:
            data = json.load(open(FILENAME))

        guild = data.get(guild_id)

        if not guild:
            raise InvalidID()

        # attrs
        self.data = data
        self.guild = guild
        self.g_id = guild_id
        self.money_symbol: str = guild.get('money_symbol')
        self.money_rates: float = guild.get('money_rates')

    def __repr__(self):
        return "<Guild {0.g_id} money_symbol={0.money_symbol} money_rates={0.money_rates}>".format(self)

    def update_rates(self, rates: float):
        data = self.data
        data[self.g_id]['money_rates'] = rates
        json.dump(data, open(FILENAME, 'w'), indent=4)
        return rates

    def update_symbol(self, symbol: str):
        data = self.data
        data[self.g_id]['money_symbol'] = symbol
        json.dump(data, open(FILENAME, 'w'), indent=4)
        return symbol

    @property
    def users(self):
        data = [x['id'] for x in self.guild.get('users')]
        return [Member(user_id=_id, guild_id=int(self.g_id)) for _id in data]

    @property
    def members(self):
        return self.users


class Member:
    def __init__(self, user_id: int, guild_id: int):
        self.u_id = str(user_id)
        self.g_id = str(guild_id)
        if not user_exists(user_id=user_id, guild_id=guild_id):
            data = create_user(user_id=user_id, guild_id=guild_id)
            raw = json.load(open(FILENAME))
            index = [u['id'] for u in raw[self.g_id]['users']].index(user_id)
        else:
            raw = json.load(open(FILENAME))
            index = [u['id'] for u in raw[self.g_id]['users']].index(user_id)
            data = raw[self.g_id]['users'][index]

        self.raw = raw
        self.data = data
        self.index = index

        # attrs
        self.balance = data.get('balance')

    @property
    def tools(self):
        return [Tool(int(tool)) for tool in self.data.get('tools')]

    @property
    def guild(self):
        return Guild(int(self.g_id))

    def __repr__(self):
        return "<User {0.u_id} guild={0.guild} balance={0.balance} tools={0.tools}>".format(self)

    def update_balance(self, amount: int):
        self.balance += amount
        self.data['balance'] = self.balance
        data = self.raw[self.g_id]['users']
        data.pop(self.index)
        data.append(self.data)
        self.raw[self.g_id]['users'] = data
        json.dump(self.raw, open(FILENAME, 'w'), indent=4)
        return amount


class User(Member):
    pass


class Tool:
    def __init__(self, id: int):
        if not len(str(id)) == 5:
            raise InvalidID("That tool doesn't exist!")

        data = json.load(open(INFO))
        data = data['Tools']
        try:
            index = [x['id'] for x in data].index(id)
        except ValueError:
            raise InvalidID("That tool doesn't exist!")
        stats = data[index]
        self.name = stats.get('name')
        self.power = stats.get('power')
        self.price = stats.get('price')
        self.id = stats.get('id')

    def __repr__(self):
        return str(self.id)
