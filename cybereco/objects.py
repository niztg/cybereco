import re
import json
from .exceptions import InvalidID
from .functions import *

__all__ = (
    'Guild'
)


FILENAME = 'data.json'
REGEX = re.compile(r'[0-9]+')


class Guild:
    def __init__(self, guild_id: int):
        if not guild_exists(guild_id):
            create_guild(guild_id)

        guild_id = str(guild_id)
        if (not len(guild_id) == 18) or (not re.match(REGEX, guild_id)):
            raise InvalidID()

        data = json.load(open(FILENAME))
        guild = data.get(guild_id)

        if not guild:
            raise InvalidID()

        # attrs
        self.data = data
        self.g_id = guild_id
        self.money_symbol: str = guild.get('money_symbol')
        self.rates: float = guild.get('rates')

    def update_rates(self, rates: float):
        data = self.data
        data[self.g_id]['rates'] = rates
        json.dump(data, open(FILENAME, 'w'), indent=4)

    def update_symbol(self, symbol: str):
        data = self.data
        data[self.g_id]['money_symbol'] = symbol
        json.dump(data, open(FILENAME, 'w'), indent=4)

