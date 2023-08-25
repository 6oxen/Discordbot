import nextcord
from nextcord.ext import commands

import requests
import os

from datetime import datetime
from io import BytesIO
from PIL import Image


class Recent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recent(self, ctx, *, user_input):
        url = f'https://api.collectionlog.net/items/recent/{user_input}'
        response = requests.get(url).json()
        items = response.get("items", [])  # Get the list of items from the response

        recent_collection_logs = []
        for item in items:
            item_id = item["id"]
            item_name = item["name"]
            item_obtained_at = item["obtainedAt"]

            obtained_date = datetime.strptime(item_obtained_at, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

            recent_collection_logs.append({
                "item_id": item_id,
                "item_name": item_name,
                "obtained_date": obtained_date
            })

        try:
            # Create a list to store item info
            item_info_list = []

            # Calculate the total width of the combined image
            total_width = 36 * len(recent_collection_logs) + 5 * (len(recent_collection_logs) - 1)

            # Create an image object to combine item icons
            combined_image = Image.new('RGBA', (total_width, 32))

            x_offset = 0  # Initial x-offset for placing images side by side
        
            # Iterate through recent_collection_logs and prepare images and item info
            for item in recent_collection_logs:
                item_id = item["item_id"]
                item_name = item["item_name"]
                obtained_date = item["obtained_date"]

                # Construct the path to the image file
                image_path = os.path.join("assets/item-icons", f"{item_id}.png")

                # Check if the image file exists
                if os.path.exists(image_path):
                    icon = Image.open(image_path).resize((36, 32))
                    combined_image.paste(icon, (x_offset, 0))
                    x_offset += 36 + 5  # Increment the x-offset for the next image (+5 for spacing)
                    item_info_list.append(f"{item_name} [{obtained_date}]")
                else:
                    await ctx.send(f"Image not found for item ID {item_id}")

            # Convert the combined image to bytes
            combined_image_bytes = BytesIO()
            combined_image.save(combined_image_bytes, format='PNG')
            combined_image_bytes.seek(0)

            # Create a discord.File from the combined image bytes
            combined_image_file = nextcord.File(combined_image_bytes, filename="combined_image.png")

            # Concatenate item info and join with newline characters
            item_info_text = "\n".join(item_info_list)

            # Construct the response text
            #response_text = f"**{user_input}**\n"

            # Create a properly formatted code block
            code_block = f"```\n{item_info_text}\n```"

            # Create an embed with image attachment and code block in the description
            embed = nextcord.Embed(title=f"{user_input}'s senaste cloggar:", description=code_block)
            embed.set_image(url="attachment://combined_image.png")  # Set the image attachment

            # Send the combined image and item info as attachments
            await ctx.send(file=combined_image_file, embed=embed)
        except Exception as e:
            await ctx.send(f"**```[Kunde inte hitta '{user_input}' hos collectionlog.net]```**")


def setup(bot):
    bot.add_cog(Recent(bot))