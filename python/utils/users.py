import discord
from python.utils import database
import json

def username(discordid):
    database.execute(f"SELECT username FROM players WHERE discord_id='{discordid}';")
    return database.fetchone()[0]

def player_elo(discordid):
    database.execute(f"SELECT elo FROM players WHERE discord_id='{discordid}';")
    return database.fetchone()[0]
