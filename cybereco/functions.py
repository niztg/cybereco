import json

FILENAME = 'data.json'

def exists(guild_id: int)
    data = json.load(open(FILENAME))
    return data.get(str(guild_id))