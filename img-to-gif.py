from PIL import Image, ImageDraw, ImageFont
import os

frames = [
    "training_curves.png",
    "gradcam.png",
    "results.png", 
    "confusion_matrices.png"
]

images = []
for f in frames:
    img = Image.open(f).convert("RGB").resize((900, 500))
    images.append(img)

images[0].save(
    "demo.gif",
    save_all=True,
    append_images=images[1:],
    duration=2000,   # 2 sec per frame
    loop=0
)
print("demo.gif saved!")
