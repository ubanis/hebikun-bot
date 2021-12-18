from discord.ext import commands

import os
import hebicm as he
import hebilistener as heli
import games as gm

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

bot.add_cog(he.Hebi(bot))
bot.add_cog(heli.HebiListener(bot))
bot.add_cog(gm.Games(bot))

TOKEN = os.environ.get("DISCORDBOT_API_TOKEN")
bot.run(TOKEN)
