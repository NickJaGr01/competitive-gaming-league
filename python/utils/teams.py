import discord
from python.utils import database
from python.utils import emoji_list
from python.utils import cache
import json
import asyncio

def get_owned_teams(guild_id, user_id):
    database.execute(f"SELECT team_id FROM team_table WHERE owner_id={user_id} AND game=ANY(SELECT UNNEST(games) AS games FROM server_table WHERE server_id={guild_id});")
    teams = database.fetchall()
    r = []
    for t, in teams:
        r.append(t)
    return r

def team_name(team_id):
    database.execute(f"SELECT team_name FROM team_table WHERE team_id={team_id};")
    return database.fetchone()[0]

def team_elo(team_id):
    database.execute(f"SELECT team_elo FROM team_table WHERE team_id={team_id};")
    return database.fetchone()[0]

def team_game(team_id):
    database.execute(f"SELECT game FROM team_table WHERE team_id={team_id};")
    return database.fetchone()[0]

def primary_players(team_id):
    database.execute(f"SELECT primary_players FROM team_table WHERE team_id={team_id};")
    return database.fetchone()[0]

def substitute_players(team_id):
    database.execute(f"SELECT sub_players FROM team_table WHERE team_id={team_id};")
    return database.fetchone()[0]

async def select_team(ctx, user, team_list):
    #send a message to have the user select a team from a list
    #team_list should be a list of tuples: (team_id, team_name, game)
    e = discord.Embed(title='Select Team', description=user.mention, colour=discord.Colour.blue())
    liststr = ""
    count = 0
    tids = []
    for team_id, team_name, game in team_list:
        tids.append(team_id)
        if len(liststr) > 0:
            liststr += '\n'
        liststr += f"{emoji_list[count]} {team_name} **({game})**"
        count += 1
    e.add_field(name='Select a team', value=liststr)
    msg = await ctx.send(embed=e)
    for x in range(count):
        await msg.add_reaction(emoji_list[x])
    selected_team = None
    def done(team):
        nonlocal selected_team
        selected_team = team
    cache.add('select_team', msg.id, {'teams': tids, 'author': user, 'done': done})
    time = 0
    while selected_team == None:
        asyncio.sleep(1)
        time += 1
        #timeout after 60 seconds
        if time >= 60:
            e.clear_fields()
            e.add_field(name='Timed Out', value='Team selection timed out after 60 seconds.\nTry again.')
            await msg.edit(embed=e)
            cache.delete('select_team', msg.id)
            return None
    return selected_team
