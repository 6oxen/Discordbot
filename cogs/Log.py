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
    async def log(self, ctx, username: str, *, user_friendly_boss_name: str = None):
        try:
            url = f'https://api.collectionlog.net/collectionlog/user/{username}'
            response = requests.get(url).json()

            boss_name = self.boss_mapping.get(user_friendly_boss_name.lower(), None)

            if not boss_name:
                await ctx.send(f"Hittar inte bossen '{user_friendly_boss_name}' skriv !list för att se lista med alla bossnamn")
                return

            boss_data = response.get("collectionLog", {}).get("tabs", {}).get("Bosses", {}).get(boss_name, None)

            if not boss_data:
                await ctx.send(f"Hittar inte'{boss_name}' för '{username}'.")
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








            # Create an info image with the specified text
            info_image = Image.new('RGBA', (final_image_size[0], 60), (72, 64, 53, 255))
            draw = ImageDraw.Draw(info_image)
        
            font_path = os.path.join("assets", "font", "runescape_uf.ttf")
            font = ImageFont.truetype(font_path, 22)
        
            info_text = f"{boss_name} (User: {username})\n{obtained_string}"
        
            # Calculate the size of the text using the font
            #text_size = draw.textsize(info_text, font=font)
        
            #x_position = (final_image_size[0] - text_size[0]) // 2
            #y_position = (final_image_size[1] - text_size[1]) // 2
        
            draw.text((10, 5), info_text, fill="yellow", font=font)
        
            info_img_bytes_io = BytesIO()
            info_image.save(info_img_bytes_io, format="PNG")
            info_img_bytes_io.seek(0)
        
            info_image_file = nextcord.File(info_img_bytes_io, filename="info_image.png")



            # Create a nextcord.File from the BytesIO object
            #scaled_image_file = nextcord.File(img_bytes_io, filename="final_image_file.png")

            # Combine final_image_file and info_image_file vertically
            combined_image = Image.new('RGBA', (final_image_size[0], final_image_size[1] + 60))
            combined_image.paste(info_image, (0, 0))  # Paste info_image at the top
            combined_image.paste(background, (0, 60))  # Paste final_image below info_image

            # Save the combined image to a BytesIO object
            combined_img_bytes_io = BytesIO()
            combined_image.save(combined_img_bytes_io, format="PNG")
            combined_img_bytes_io.seek(0)

            combined_image_file = nextcord.File(combined_img_bytes_io, filename="combined_image.png")

            # Create an embed with the custom color
            embed = nextcord.Embed(
                title=f"{boss_name} - {username}",
                color=0x484035  # #484035 Set your custom color here (Hex color)
            )

            embed.set_image(url="attachment://combined_image.png")  # Set the image URL within the embed

            await ctx.send(embed=embed, file=combined_image_file)

            img_bytes_io.close()
            info_img_bytes_io.close()
            combined_img_bytes_io.close()

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Log(bot))