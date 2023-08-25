import os
import json
import base64
from io import BytesIO
from PIL import Image

def save_image(id, image_data):
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image_path = os.path.join("item-icons", f"{id}.png")

    if not os.path.exists("item-icons"):
        os.makedirs("item-icons")

    if not os.path.exists(image_path):
        image.save(image_path)
        print(f"Saved image for ID {id}")
    else:
        print(f"Image for ID {id} already exists")

def main():
    with open("item-icons.json", "r") as json_file:
        data = json.load(json_file)
    
    for item_id, image_data in data.items():
        save_image(item_id, image_data)

if __name__ == "__main__":
    main()