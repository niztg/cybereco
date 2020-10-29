import json

FILENAME = 'data.json'

__all__ = (
    'guild_exists',
    'create_guild'
)


def guild_exists(guild_id: int):
    data = json.load(open(FILENAME))
    return data.get(str(guild_id))


def create_guild(guild_id: int):
    data = json.load(open(FILENAME))
    data[str(guild_id)] = {
        "rates": 1.00,
        "money_symbol": "❄️",
        "users": [

        ]
    }
    json.dump(data, open(FILENAME, 'w'), indent=4)
