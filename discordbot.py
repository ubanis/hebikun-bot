""" Hebikun Discord bot """
import os
from discord.ext import commands

import hebicm as hebi_commands
import hebilistener as hebi_listener
import games as hebi_games

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

bot.add_cog(hebi_commands.Hebi(bot))
bot.add_cog(hebi_listener.HebiListener(bot))
bot.add_cog(hebi_games.Games(bot))

TOKEN = os.environ.get("DISCORDBOT_API_TOKEN")
bot.run(TOKEN)
