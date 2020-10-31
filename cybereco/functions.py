import json

FILENAME = 'data.json'
NEW_USER = {
    "balance": 0,
    "tools": ['21522']
}
NEW_GUILD = {
        "money_rates": 1.00,
        "money_symbol": "❄️",
        "users": []
    }

__all__ = (
    'guild_exists',
    'create_guild',
    'user_exists',
    'create_user'
)


def guild_exists(guild_id: int):
    data = json.load(open(FILENAME))
    return bool(data.get(str(guild_id)))


def create_guild(guild_id: int):
    data = json.load(open(FILENAME))
    data[str(guild_id)] = NEW_GUILD
    json.dump(data, open(FILENAME, 'w'), indent=4)
    return NEW_GUILD


def user_exists(user_id: int, guild_id: int):
    if not guild_exists(guild_id):
        create_guild(guild_id)
        return False

    data = json.load(open(FILENAME))
    data = data[str(guild_id)]
    try:
        [u['id'] for u in data['users']].index(user_id)
        return True
    except ValueError:
        return False


def create_user(user_id: int, guild_id: int):
    if not guild_exists(guild_id):
        create_guild(guild_id)

    data = json.load(open(FILENAME))
    user = NEW_USER
    user['id'] = user_id
    data[str(guild_id)]['users'].append(user)
    json.dump(data, open(FILENAME, 'w'), indent=4)
    return user