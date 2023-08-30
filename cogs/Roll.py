import nextcord
from nextcord.ext import commands
import random

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, drop_rate: str = None, x: str = None):
        if drop_rate is None:
            await ctx.send("**```Användning: !roll <drop rate> <antal itirationer [1-100]>\nExempel: !roll 1/250 | !roll 1/250 10```**")
            return

        try:
            numerator, denominator = map(int, drop_rate.split("/"))
            if numerator <= 0 or denominator <=  0 or denominator > 25000:
                raise ValueError
        except ValueError:
            await ctx.send("**```Ogiltig inmatning. Använd formatet 'x/y' där x och y är positiva heltal.\n'y' får som högst ha ett värde på '25000', alltså !roll 1/25000```**")
            return

        if x is not None:
            try:
                x = int(x)
                if x < 1 or x > 100:
                    raise ValueError
            except ValueError:
                await ctx.send("**```Ogiltigt antal itirationer. Ange ett heltal mellan 1 och 100.```**")
                return
        else:
            x = 1  # Default value if x is not provided

        success_chance = numerator / denominator
        max_attempts = 100000
        results = []

        for _ in range(x):
            current_attempts = 0
            while random.random() > success_chance and current_attempts < max_attempts:
                current_attempts += 1
            results.append(current_attempts)

        if x > 1:
            valid_results = [attempt for attempt in results if attempt > 0]
            avg_attempts = sum(valid_results) / len(valid_results)
            rounded_avg_attempts = round(avg_attempts)
            min_attempts = min(valid_results)
            max_attempts = max(results)
    
            await ctx.send(f"**```Resultat för '{x}' iterationer med en chans på {numerator}/{denominator} ({success_chance * 100:.3f}%):\n"
                        f"{results}\n\n"
                        f"🥄Minsta antal: {min_attempts} KC\n"
                        f"🌵Högsta antal: {max_attempts} KC\n"
                        f"📊Genomsnitt för '{x}' itirationer: {rounded_avg_attempts} KC```**")
        else:
            if max(results) == max_attempts:
                await ctx.send(f"**```Jag lyckades inte få det önskade droppet på totalt 100,000 försök.. "
                            f"Droppet har en chans på {numerator}/{denominator} ({success_chance * 100:.3f}%).```**")
            else:
                await ctx.send(f"**```Det tog mig '{max(results)}' försök att få det önskade droppet med en chans på {numerator}/{denominator} ({success_chance * 100:.3f}%).```**")

def setup(bot):
    bot.add_cog(Roll(bot))