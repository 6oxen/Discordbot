# Calc.py located in .cogs\Calc.py

import nextcord
from nextcord.ext import commands

class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, input_value: str = None, z: str = None):
        if input_value is None or z is None:

            response = "**```\n"
            response += f"Du måste ange värden för att !calc ska fungera.\n"
            response += f"Matten: 1 - (1 - (x/y))^z  : Ett mob är förväntad att droppa 'x' items varje 'y' kills, z = antal kills\n\n"
            response += f"Exempel: !calc 1/500 20\n"
            response += f"\nDu skrev: !calc {input_value} {z}"
            response += "```**"
            await ctx.send(response)
            return
        try:
            # Validate input_value format
            if '/' not in input_value:
                await ctx.send(f"**```[[[[Error [[[[Error, M[[[atte ä[[r in8[te din [starka sida?]]\n\nDu skrev: !calc {input_value} {z}\nFungerande exempel: !calc 1/500 20```**")
                return

             # Validate z input
            if not z.isdigit():
                await ctx.send(f"**```[[[[Error [[[[Error, Fel format för antalet. Använd ett heltal]]\n\nDu skrev: !calc {input_value} {z}\nFungerande exempel: !calc {input_value} 20```**")
                return
            z_int = int(z)
            if z_int == 0:
                ##försökte du nyss räkna ut oddsen för ett drop när du har 0 kills?\nKan lova att chansen är 0.\n🌵Du är torrare än sahara
                await ctx.send(f"**```Säg inte att du behöver hjälp för att räkna ut oddsen för ett drop när du har 0 kills?...\nCHANSEN ÄR NOLL!\n\n{ctx.author.display_name} 🐔🧠```**")
                return

            x_str, y_str = input_value.split('/')
            if not x_str.isdigit() or not y_str.isdigit():
                await ctx.send(f"**```[[[[Error [[[[Error, Fel format för x/y. Använd siffror och /]]\n\nDu skrev: !calc {input_value} {z}\nFungerande exempel: !calc 1/500 {z}```**")
                return
            x_int = int(x_str)
            if x_int == 0:
                await ctx.send(f"**```Du vet väl att 0 delat på {y_str} = 0? Ändra nämnaren till 1 🧠\n\nDu skrev: !calc {input_value} {z}\nFungerande exempel: !calc 1/500 {z}```**")
                return
            if x_int != 1:
                await ctx.send(f"**```{x_int}/{y_str} Du borde nog ändra nämnaren till 1 och ingenting annat.\n\nDu skrev: !calc {input_value} {z}\nFungerande exempel: !calc 1/500 {z}```**")
                return
                
            x = int(x_str)
            y = int(y_str)
            if y == 0:
                await ctx.send("Försöker du döda mig??")
                return

            # Calculate the drop rate using the formula
            drop_rate = 1 - (1 - x/y) ** z_int
            dry_rate = (1 - drop_rate)
            expected = z_int / y

            # Format the response as a code block
            response = f"Med en drop rate på '{x}/{y}' och med '{z_int}' kills är oddsen:\n"
            response += f"🥄Drop: {drop_rate:.2%}\n"
            response += f"🌵Dry: {dry_rate:.2%}\n"
            response += f"📊On-rate: {expected:.2f} drop(s)"

            # Send the response as a code block
            await ctx.send(f"```\n{response}\n```")
        except Exception as e:
            await ctx.send(f"```Någonting gick fel :C : {e}```")

def setup(bot):
    bot.add_cog(Calc(bot))