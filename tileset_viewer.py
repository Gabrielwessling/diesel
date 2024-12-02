import tcod

# Define the path to your image (ensure the file exists)
image_path = "tilesets/frogblock.png"

# Load the tileset image
tileset = tcod.tileset.load_tilesheet(image_path, 16, 16, tcod.tileset.CHARMAP_CP437)

# Function to retrieve a tile character by its codepoint
def get_tile_char(codepoint):
    # Get the character corresponding to the codepoint using the charmaps
    # CP437 character map provides access to codepoint mappings
    return chr(codepoint)

# Example: Get the character at codepoint index 23 (just after 'z')
for i in range(16*16):
    tile_char = get_tile_char(i)
    print(f"{i} : {tile_char}")
