import nextcord
from nextcord.ext import commands

class List(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boss_mapping = {
            "abyssal sire": "Abyssal Sire",
            "hydra": "Alchemical Hydra",
            "barrows": "Barrows Chests",
            "bryophyta": "Bryophyta",
            "callisto": "Callisto",
            "artio": "Artio",
            "cerberus": "Cerberus",
            "chaos elemental": "Chaos Elemental",
            "chaos fanatic": "Chaos Fanatic",
            "zilyana": "Commander Zilyana",
            "corp": "Corporeal Beast",
            "crazy archaeologist": "Crazy Archaeologist",
            "rex": "Dagannoth Kings",
            "duke": "Duke Sucellus",
            "bandos": "General Graardor",
            "mole": "Giant Mole",
            "guardians": "Grotesque Guardians",
            "hespori": "Hespori",
            "kq": "Kalphite Queen",
            "kbd": "King Black Dragon",
            "kraken": "Kraken",
            "armadyl": "Kree'arra",
            "zamorak": "K'ril Tsutsaroth",
            "nex": "Nex",
            "obor": "Obor",
            "phantom muspah": "Phantom Muspah",
            "muspah": "Phantom Muspah",
            "sarachnis": "Sarachnis",
            "scorpia": "Scorpia",
            "skotizo": "Skotizo",
            "tempoross": "Tempoross",
            "jad": "The Fight Caves",
            "cg": "The Gauntlet",
            "inferno": "The Inferno",
            "leviathan": "The Leviathan",
            "nightmare": "The Nightmare",
            "smoke devil": "Thermonuclear Smoke Devil",
            "whisperer": "The Whisperer",
            "vardorvis": "Vardorvis",
            "spindel": "Spindel",
            "venenatis": "Venenatis",
            "vetion": "Vet'ion",
            "calvarion": "Calvar'ion",
            "vorkath": "Vorkath",
            "wt": "Wintertodt",
            "zalcano": "Zalcano",
            "zulrah": "Zulrah"
        }

    @commands.command()
    async def list(self, ctx):
        formatted_bosses = "\n".join([f"{self.boss_mapping[alias]} / {alias}" for alias in self.boss_mapping])
        
        embed = nextcord.Embed(title="Available Bosses", color=0x00ff00, description=formatted_bosses)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(List(bot))