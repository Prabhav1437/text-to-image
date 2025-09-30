import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import random

def generate_image_with_text():
    text = text_entry.get()

    if not text:
        return

    # Create an image with a random RGB background
    width, height = 400 , 400
    background = Image.new('RGB', (width, height), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    draw = ImageDraw.Draw(background)

    text_color = (255, 255, 255)
    font = ImageFont.load_default()

    text_position = (50, 50)

    draw.text(text_position, text, fill=text_color, font=font)

    background.show()

root = tk.Tk()
root.title("Random RGB Background Text Generator")

text_label = tk.Label(root, text="Enter Text:")
text_label.pack()
text_entry = tk.Entry(root)
text_entry.pack()

generate_button = tk.Button(root, text="Generate Image", command=generate_image_with_text)
generate_button.pack()

root.mainloop()