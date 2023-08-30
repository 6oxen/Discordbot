# Log.py located in .cogs\Log.py

import nextcord
from nextcord.ext import commands
import requests
import os
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont
from io import BytesIO

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boss_mapping = {
            "abyssal sire": "Abyssal Sire",
            "alchemical hydra": "Alchemical Hydra",
            "hydra": "Alchemical Hydra",
            "barrows": "Barrows Chests",
            "bryophyta": "Bryophyta",
            "callisto": "Callisto and Artio",
            "artio": "Callisto and Artio",
            "cerberus": "Cerberus",
            "chaos elemental": "Chaos Elemental",
            "chaos fanatic": "Chaos Fanatic",
            "commander zilyana": "Commander Zilyana",
            "zilyana": "Commander Zilyana",
            "corporeal beast": "Corporeal Beast",
            "corp": "Corporeal Beast",
            "crazy archaeologist": "Crazy Archaeologist",
            "dagannoth kings": "Dagannoth Kings",
            "rex": "Dagannoth Kings",
            "duke sucellus": "Duke Sucellus",
            "duke": "Duke Sucellus",
            "general graardor": "General Graardor",
            "bandos": "General Graardor",
            "giant mole": "Giant Mole",
            "mole": "Giant Mole",
            "grotesque guardians": "Grotesque Guardians",
            "guardians": "Grotesque Guardians",
            "hespori": "Hespori",
            "kalphite queen": "Kalphite Queen",
            "kq": "Kalphite Queen",
            "king black dragon": "King Black Dragon",
            "kbd": "King Black Dragon",
            "kraken": "Kraken",
            "kree'arra": "Kree'arra",
            "kreearra": "Kree'arra",
            "armadyl": "Kree'arra",
            "k'ril tsutsaroth": "K'ril Tsutsaroth",
            "kril": "K'ril Tsutsaroth",
            "zamorak": "K'ril Tsutsaroth",
            "nex": "Nex",
            "obor": "Obor",
            "phantom muspah": "Phantom Muspah",
            "muspah": "Phantom Muspah",
            "sarachnis": "Sarachnis",
            "scorpia": "Scorpia",
            "skotizo": "Skotizo",
            "tempoross": "Tempoross",
            "the fight caves": "The Fight Caves",
            "jad": "The Fight Caves",
            "the gauntlet": "The Gauntlet",
            "gauntlet": "The Gauntlet",
            "cg": "The Gauntlet",
            "the inferno": "The Inferno",
            "inferno": "The Inferno",
            "the leviathan": "The Leviathan",
            "leviathan": "The Leviathan",
            "the nightmare": "The Nightmare",
            "nightmare": "The Nightmare",
            "thermonuclear smoke devil": "Thermonuclear Smoke Devil",
            "smoke devil": "Thermonuclear Smoke Devil",
            "the whisperer": "The Whisperer",
            "whisperer": "The Whisperer",
            "whisp": "The Whisperer",
            "vardorvis": "Vardorvis",
            "spindel": "Venenatis and Spindel",
            "venenatis": "Venenatis and Spindel",
            "vet'ion": "Vet'ion and Calvar'ion",
            "calvar'ion": "Vet'ion and Calvar'ion",
            "vetion": "Vet'ion and Calvar'ion",
            "calvarion": "Vet'ion and Calvar'ion",
            "vorkath": "Vorkath",
            "wintertodt": "Wintertodt",
            "wt": "Wintertodt",
            "zalcano": "Zalcano",
            "zulrah": "Zulrah"
        }
        self.boss_location_mapping = {
            "abyssal sire": ("Bosses", "Abyssal Sire"),
            "alchemical hydra": ("Bosses", "Alchemical Hydra"),
            "hydra": ("Bosses", "Alchemical Hydra"),
            "barrows": ("Bosses", "Barrows Chests"),
            "bryophyta": ("Bosses", "Bryophyta"),
            "callisto": ("Bosses", "Callisto and Artio"),
            "artio": ("Bosses", "Callisto and Artio"),
            "cerberus": ("Bosses", "Cerberus"),
            "chaos elemental": ("Bosses", "Chaos Elemental"),
            "chaos fanatic": ("Bosses", "Chaos Fanatic"),
            "commander zilyana": ("Bosses", "Commander Zilyana"),
            "zilyana": ("Bosses", "Commander Zilyana"),
            "corporeal beast": ("Bosses", "Corporeal Beast"),
            "corp": ("Bosses", "Corporeal Beast"),
            "crazy archaeologist": ("Bosses", "Crazy Archaeologist"),
            "dagannoth kings": ("Bosses", "Dagannoth Kings"),
            "rex": ("Bosses", "Dagannoth Kings"),
            "duke sucellus": ("Bosses", "Duke Sucellus"),
            "duke": ("Bosses", "Duke Sucellus"),
            "general graardor": ("Bosses", "General Graardor"),
            "bandos": ("Bosses", "General Graardor"),
            "giant mole": ("Bosses", "Giant Mole"),
            "mole": ("Bosses", "Giant Mole"),
            "grotesque guardians": ("Bosses", "Grotesque Guardians"),
            "guardians": ("Bosses", "Grotesque Guardians"),
            "hespori": ("Bosses", "Hespori"),
            "kalphite queen": ("Bosses", "Kalphite Queen"),
            "kq": ("Bosses", "Kalphite Queen"),
            "king black dragon": ("Bosses", "King Black Dragon"),
            "kbd": ("Bosses", "King Black Dragon"),
            "kraken": ("Bosses", "Kraken"),
            "kree'arra": ("Bosses", "Kree'arra"),
            "kreearra": ("Bosses", "Kree'arra"),
            "armadyl": ("Bosses", "Kree'arra"),
            "k'ril tsutsaroth": ("Bosses", "K'ril Tsutsaroth"),
            "kril": ("Bosses", "K'ril Tsutsaroth"),
            "zamorak": ("Bosses", "K'ril Tsutsaroth"),
            "nex": ("Bosses", "Nex"),
            "obor": ("Bosses", "Obor"),
            "phantom muspah": ("Bosses", "Phantom Muspah"),
            "muspah": ("Bosses", "Phantom Muspah"),
            "sarachnis": ("Bosses", "Sarachnis"),
            "scorpia": ("Bosses", "Scorpia"),
            "skotizo": ("Bosses", "Skotizo"),
            "tempoross": ("Bosses", "Tempoross"),
            "the fight caves": ("Bosses", "The Fight Caves"),
            "jad": ("Bosses", "The Fight Caves"),
            "the gauntlet": ("Bosses", "The Gauntlet"),
            "gauntlet": ("Bosses", "The Gauntlet"),
            "cg": ("Bosses", "The Gauntlet"),
            "the inferno": ("Bosses", "The Inferno"),
            "inferno": ("Bosses", "The Inferno"),
            "the leviathan": ("Bosses", "The Leviathan"),
            "leviathan": ("Bosses", "The Leviathan"),
            "the nightmare": ("Bosses", "The Nightmare"),
            "nightmare": ("Bosses", "The Nightmare"),
            "thermonuclear smoke devil": ("Bosses", "Thermonuclear Smoke Devil"),
            "smoke devil": ("Bosses", "Thermonuclear Smoke Devil"),
            "the whisperer": ("Bosses", "The Whisperer"),
            "whisperer": ("Bosses", "The Whisperer"),
            "whisp": ("Bosses", "The Whisperer"),
            "vardorvis": ("Bosses", "Vardorvis"),
            "spindel": ("Bosses", "Venenatis and Spindel"),
            "venenatis": ("Bosses", "Venenatis and Spindel"),
            "vet'ion": ("Bosses", "Vet'ion and Calvar'ion"),
            "calvar'ion": ("Bosses", "Vet'ion and Calvar'ion"),
            "vetion": ("Bosses", "Vet'ion and Calvar'ion"),
            "calvarion": ("Bosses", "Vet'ion and Calvar'ion"),
            "vorkath": ("Bosses", "Vorkath"),
            "wintertodt": ("Bosses", "Wintertodt"),
            "wt": ("Bosses", "Wintertodt"),
            "zalcano": ("Bosses", "Zalcano"),
            "zulrah": ("Bosses", "Zulrah"),
            "beginner": ("Clues", "Beginner Treasure Trails"),
            "easy": ("Clues", "Easy Treasure Trails"),
            "medium": ("Clues", "Medium Treasure Trails"),
            "hard": ("Clues", "Hard Treasure Trails"),
            "elite": ("Clues", "Elite Treasure Trails"),
            "master": ("Clues", "Master Treasure Trails"),
            "hard rare": ("Clues", "Hard Treasure Trails (Rare)"),
            "elite rare": ("Clues", "Elite Treasure Trails (Rare)"),
            "master rare": ("Clues", "Master Treasure Trails (Rare)"),
            "barbarian assult": ("Minigames", "Barbarian Assault"),
            "agility arena": ("Minigames", "Brimhaven Agility Arena"),
            "castle wars": ("Minigames", "Castle Wars"),
            "fishing trawler": ("Minigames", "Fishing Trawler"),
            "giants foundry": ("Minigames", "Giants' Foundry"),
            "gnome restaurant": ("Minigames", "Gnome Restaurant"),
            "gotr": ("Minigames", "Guardians of the Rift"),
            "guardians of the rift": ("Minigames", "Guardians of the Rift"),
            "hallowed": ("Minigames", "Hallowed Sepulchre"),
            "hs": ("Minigames", "Hallowed Sepulchre"),
            "hallowed sepulchre": ("Minigames", "Hallowed Sepulchre"),
            "lms": ("Minigames", "Last Man Standing"),
            "last man standing": ("Minigames", "Last Man Standing"),
            "magic training arena": ("Minigames", "Magic Training Arena"),
            "mta": ("Minigames", "Magic Training Arena"),
            "mahogany homes": ("Minigames", "Mahogany Homes"),
            "pest control": ("Minigames", "Pest Control"),
            "rouges den": ("Minigames", "Rogues' Den"),
            "shades fo morton": ("Minigames", "Shades of Mort'ton"),
            "sould wars": ("Minigames", "Soul Wars"),
            "temple trekking": ("Minigames", "Temple Trekking"),
            "tithe farm": ("Minigames", "Tithe Farm"),
            "trouble brewing": ("Minigames", "Trouble Brewing"),
            "volcanic mine": ("Minigames", "Volcanic Mine"),
            "aerial fishing": ("Other", "Aerial Fishing"),
            "pets": ("Other", "All Pets"),
            "camdozaal": ("Other", "Camdozaal"),
            "champions challange": ("Other", "Champion's Challenge"),
            "chaos druids": ("Other", "Chaos Druids"),
            "chompy bird hunting": ("Other", "Chompy Bird Hunting"),
            "creature creation": ("Other", "Creature Creation"),
            "cyclopes": ("Other", "Cyclopes"),
            "forestry": ("Other", "Forestry"),
            "fossil island notes": ("Other", "Fossil Island Notes"),
            "glough": ("Other", "Glough's Experiments"),
            "gloughs experiments": ("Other", "Glough's Experiments"),
            "miscellaneous": ("Other", "Miscellaneous"),
            "misc": ("Other", "Miscellaneous"),
            "monkey backpacks": ("Other", "Monkey Backpacks"),
            "motherload mine": ("Other", "Motherlode Mine"),
            "my notes": ("Other", "My Notes"),
            "random events": ("Other", "Random Events"),
            "random event": ("Other", "Random Events"),
            "reventants": ("Other", "Revenants"),
            "rooftop agility": ("Other", "Rooftop Agility"),
            "agility": ("Other", "Rooftop Agility"),
            "shayzien armour": ("Other", "Shayzien Armour"),
            "shooting stars": ("Other", "Shooting Stars"),
            "pets skilling": ("Other", "Skilling Pets"),
            "skilling pets": ("Other", "Skilling Pets"),
            "slayer": ("Other", "Slayer"),
            "tzhaar": ("Other", "TzHaar"),
            "cox": ("Raids", "Chambers of Xeric"),
            "chambers of xeric": ("Raids", "Chambers of Xeric"),
            "tob": ("Raids", "Theatre of Blood"),
            "theatre of blood": ("Raids", "Theatre of Blood"),
            "toa": ("Raids", "Tombs of Amascut"),
            "tombs of amascut": ("Raids", "Tombs of Amascut")            
        }



    async def generate_boss_image(self, obtained, item_id, quantity):
        # Construct the path to the image file
        image_path = os.path.join("assets/item-icons", f"{item_id}.png")

        # Check if the image file exists
        if os.path.exists(image_path):
            # Open and process the image
            with Image.open(image_path) as img:
                img_copy = img.copy()  # Make a copy of the image to preserve original
                if not obtained:
                    # Create a separate mask for transparency
                    mask = img_copy.convert("L")  # Grayscale mask
                    mask = ImageEnhance.Brightness(mask).enhance(0.8)  # Adjust transparency

                    # Apply the mask to the copy's alpha channel
                    img_copy.putalpha(mask)

                # Add text with quantity on the image (same as before)
                draw = ImageDraw.Draw(img_copy)
                font_path = os.path.join("assets", "font", "runescape_uf.ttf")
                font = ImageFont.truetype(font_path, 12)  # Specify the font and size
                text = str(quantity)
                text_color = "yellow"
                border_color = "black"
                border_size = 1

                # Draw black borders around the text
                for dx in range(-border_size, border_size + 1):
                    for dy in range(-border_size, border_size + 1):
                        draw.text((5 + dx, 1 + dy), text, fill=border_color, font=font)
                # Draw the actual text in white
                draw.text((5, 1), text, fill=text_color, font=font)

                return img_copy

        return None

        
    @commands.command()
    async def log(self, ctx, username: str = None, *, user_input: str = None):
        if username is None or user_input is None:
            response = "**```\n"
            response += f"!log hämtar hela cloggen från kategorin 'boss' från collectionlog.net\n"
            response += f"För att kommandot ska fungera måste kontots loggar vara uppladdat till collectionlog.net (runlite plugin)\n"
            response += f"För att se alla möjliga bossar skriv: !list\n\n"
            response += f"Exempel: !log USERNAME BOSSNAMN"
            response += f"\nDu skrev: !log {username} {user_friendly_boss_name}"
            response += "```**"
            await ctx.send(response)
            return
        try:
            url = f'https://api.collectionlog.net/collectionlog/user/{username}'
            response = requests.get(url).json()

            boss_location = self.boss_location_mapping.get(user_input.lower(), None)

            if not boss_location:
                await ctx.send(f"**```[Hittar inte platsen/data för '{user_input}'. !list för alla mjöliga cloggar\n[Kontrollera också att datan för '{username}' är uppladdat hos collectionlog.net]```**")
                return

            boss_name = self.boss_location_mapping[user_input][1]
            tabs_data = response.get("collectionLog", {}).get("tabs", {})
            tab_name, sub_tab_name = boss_location
            boss_data = tabs_data.get(tab_name, {}).get(sub_tab_name, None)

            if not boss_data:
                await ctx.send(f"**```[Hittar inte bossdata för '{user_input}'.]\n[Kontrollera att datan för '{username}' är uppladdat hos collectionlog.net]```**")
                return

            # Calculate the number of obtained items and total items
            total_items = len(boss_data.get("items", []))
            obtained_items = sum(1 for item in boss_data.get("items", []) if item.get("obtained"))

            # Create the obtained/total items string
            obtained_string = f"Obtained: {obtained_items}/{total_items}"


            # Prepare a list to store processed images
            image_paths = []

            # Attach item images to the list based on item id
            for item in boss_data.get("items", []):
                item_id = item.get("id", None)
                obtained = item.get("obtained", False)
                quantity = item.get("quantity", 0)

                # Generate the boss image
                boss_image = await self.generate_boss_image(obtained, item_id, quantity)

                if boss_image:
                    image_paths.append(boss_image)

            # Combine the images in a grid
            grid_width = 6
            image_width, image_height = image_paths[0].size  # Assuming all images have the same dimensions
            grid_height = -(-len(image_paths) // grid_width)  # Calculate rows needed

            # Create an empty image for the combined grid
            combined_image = Image.new('RGBA', (image_width * grid_width, image_height * grid_height))

            # Paste each image into the combined grid
            for i, img in enumerate(image_paths):
                row = i // grid_width
                col = i % grid_width
                combined_image.paste(img, (col * image_width, row * image_height))

            # Scale the combined image to double its size
            scaled_image = combined_image.resize((combined_image.width * 2, combined_image.height * 2))

            # Save the scaled image to a BytesIO object
            img_bytes_io = BytesIO()
            scaled_image.save(img_bytes_io, format="PNG")
            img_bytes_io.seek(0)


            # Calculate the size of the final image based on the scaled image dimensions
            final_image_size = (scaled_image.width, scaled_image.height)

            # Create a new background image with the specified color and size
            background = Image.new('RGBA', final_image_size, (72, 64, 53, 255))

            # Paste the scaled image onto the background
            background.paste(scaled_image, (0, 0), scaled_image)

            # Save the final image to a BytesIO object
            final_img_bytes_io = BytesIO()
            background.save(final_img_bytes_io, format="PNG")
            final_img_bytes_io.seek(0)

            # Create a nextcord.File from the BytesIO object
            final_image_file = nextcord.File(final_img_bytes_io, filename="final_image.png")

            ##
            killcount_message = None
            try:
                killcount_data = boss_data.get("killCount", [])
                if killcount_data:
                    # Extract "name" and "amount" values from the first entry in the list (assuming there's only one)
                    killcount_name = killcount_data[0].get("name", "Unknown Name")
                    killcount_amount = killcount_data[0].get("amount", 0)

                    # Create a text message that includes the "killcount" information
                    killcount_message = f"{killcount_name}: {killcount_amount}"

                ##    # ... (rest of your code)
                else:
                    killcount_message = None
            except Exception as e:
                killcount_message = None
            

            # Create an info image with the specified text
            info_image = Image.new('RGBA', (final_image_size[0], 60), (72, 64, 53, 255))
            draw = ImageDraw.Draw(info_image)
        
            font_path = os.path.join("assets", "font", "runescape_uf.ttf")
            font = ImageFont.truetype(font_path, 22)

            info_text = None
            if killcount_message != None:
                info_text = f"{killcount_message}\n{obtained_string}"
            else:
                info_text = f"{boss_name} (User: {username})\n{obtained_string}"
        
            draw.text((10, 5), info_text, fill="yellow", font=font)
        
            info_img_bytes_io = BytesIO()
            info_image.save(info_img_bytes_io, format="PNG")
            info_img_bytes_io.seek(0)
        
            info_image_file = nextcord.File(info_img_bytes_io, filename="info_image.png")


            # Combine final_image_file and info_image_file vertically
            combined_image = Image.new('RGBA', (final_image_size[0], final_image_size[1] + 60))
            combined_image.paste(info_image, (0, 0))  # Paste info_image at the top
            combined_image.paste(background, (0, 60))  # Paste final_image below info_image

            # Save the combined image to a BytesIO object
            combined_img_bytes_io = BytesIO()
            combined_image.save(combined_img_bytes_io, format="PNG")
            combined_img_bytes_io.seek(0)

            combined_image_file = nextcord.File(combined_img_bytes_io, filename="combined_image.png")

            #await ctx.send(content=killcount_message, file=combined_image_file)
            await ctx.send(file=combined_image_file)

            img_bytes_io.close()
            info_img_bytes_io.close()
            combined_img_bytes_io.close()

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Log(bot))