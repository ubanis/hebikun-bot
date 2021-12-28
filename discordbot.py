""" Hebikun Discord bot py-cord version """
import os
from discord.ext import commands

import hebicm as hebi_commands
import hebilistener as hebi_listener
import games as hebi_games

client = commands.Bot(command_prefix='!')
client.remove_command('help')

client.add_cog(hebi_commands.Hebi(client))
client.add_cog(hebi_listener.HebiListener(client))
client.add_cog(hebi_games.Games(client))


TOKEN = os.environ.get("DISCORDBOT_API_TOKEN")
client.run(TOKEN)