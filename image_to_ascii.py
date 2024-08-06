from ascii_magic import AsciiArt

# Define the path to the image file
image_path = r"C:\Users\jacobs\Pictures\snake.jpg"

# Create an AsciiArt object from the image file
my_art = AsciiArt.from_image(image_path)

# Display the ASCII art in the terminal
my_art.to_terminal()
