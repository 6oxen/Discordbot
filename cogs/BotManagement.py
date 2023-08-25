# BotManagement.py located in .cogs\BotManagement.py

import nextcord
from nextcord.ext import commands
import os
import random

class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()  # Make sure only the bot owner can use this command
    async def update(self, ctx):
        try:
            # Unload all loaded cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')

            # Load all cogs again
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.load_extension(f'cogs.{filename[:-3]}')

            # List of possible random responses
            responses = [
                "ok.",
                "dejavuuuuuuu",
                "💩"
            ]

            # Select a random response
            random_response = random.choice(responses)

            await ctx.send(random_response)  # Send the random response
        except Exception as e:
            await ctx.send(f"Fel: {e}")

def setup(bot):
    bot.add_cog(BotManagement(bot))