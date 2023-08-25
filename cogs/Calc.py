# Calc.py located in .cogs\Calc.py

import nextcord
from nextcord.ext import commands

class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, input_value: str, z: int):
        try:
            # Split the input_value into x and y
            if '/' in input_value:
                x_str, y_str = input_value.split('/')
                x = int(x_str)
                y = int(y_str)
                if y == 0:
                    await ctx.send("Försöker du döda mig??")
                    return
            else:
                await ctx.send("Error Error, Matte är inte din starka sida?")
                return

            # Calculate the drop rate using the formula
            drop_rate = 1 - (1 - x/y) ** z
            dry_rate = (1 - drop_rate)
            expected = z / y

            # Format the response as a code block
            response = f"Med en drop rate på '{x}/{y}' och med '{z}' kills är oddsen:\n"
            response += f"🥄Drop: {drop_rate:.2%}\n"
            response += f"🌵Dry: {dry_rate:.2%}\n"
            response += f"📊On-rate: {expected:.2f} drops"

            # Send the response as a code block
            await ctx.send(f"```\n{response}\n```")
        except Exception as e:
            await ctx.send(f"Matte är inte din starka sida? !drop DROPRATE KILLS")

def setup(bot):
    bot.add_cog(Calc(bot))