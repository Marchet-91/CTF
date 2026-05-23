from PIL import Image

# Replace 'Path to Image' with the actual path to your image file.
image_path = 'Path to Image'

# Open the image and convert it to 'RGB' mode.
with Image.open(image_path) as img:
    img = img.convert('RGB')

    # Retrieve the width and height of the image.
    width, height = img.size

    # Initialize a list to store RGB values.
    rgb_values = []

    # Use a list comprehension to populate the list with RGB values of each pixel.
    rgb_values = [img.getpixel((x, y)) for y in range(height) for x in range(width)]

# Print the RGB value of the first pixel.
print("RGB value of the first pixel:", rgb_values[0])