import re
import json
from .exceptions import InvalidID

__all__ = (

)


FILENAME = 'data.json'
REGEX = re.compile(r'[0-9]+')


class Guild:
    def __init__(self, guild_id: int):
        guild_id = str(guild_id)
        if (not len(guild_id) == 18) or (not re.match(REGEX, guild_id)):
            raise InvalidID()

        data = json.load(open(FILENAME))

        if not data.get(guild_id):
            raise InvalidID()

        # attrs
        self.data = data
        self.money_symbol: str = data.get('money_symbol')
        self.rates: float = data.get('rates')
