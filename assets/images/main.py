from PIL import Image
import numpy as np


png = Image.open("icons-refresh-64.png")

pix = np.array(png)

# pix += np.uint8([255, 0, 0, 0])

fc = [20,20,20]

pix = np.array([[[fc[0], fc[1], fc[1], pix[-1]] if pix[-1] > 0 else pix for pix in row ] for row in pix], dtype=np.uint8)

png = Image.fromarray(pix) 

print(pix.shape)

bg = (255, 255, 255, 255)
bg = bg[:3]

img = Image.new("RGB", png.size, bg)
img.paste(png, mask=png.split()[3])

img.show("icon")
