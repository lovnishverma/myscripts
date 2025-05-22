import os
from PIL import Image

def compress_image(input_path, output_path, target_kb=200, step=5, min_quality=10):
    """
    Compresses the image to be under target_kb size.
    """
    img = Image.open(input_path)
    quality = 95
    ext = input_path.split(".")[-1].lower()

    if ext in ['jpg', 'jpeg']:
        while True:
            img.save(output_path, format="JPEG", quality=quality)
            size_kb = os.path.getsize(output_path) // 1024
            if size_kb <= target_kb or quality < min_quality:
                break
            quality -= step
        print(f"[✓] Compressed JPEG to {size_kb} KB (quality={quality})")

    elif ext == 'png':
        img.save(output_path, format="PNG", optimize=True)
        size_kb = os.path.getsize(output_path) // 1024
        print(f"[✓] Compressed PNG to {size_kb} KB (lossless)")

    else:
        print("[✗] Unsupported file type:", ext)

def compress_folder(folder_path, target_kb=200):
    output_dir = os.path.join(folder_path, "compressed")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            in_path = os.path.join(folder_path, filename)
            out_path = os.path.join(output_dir, filename)
            compress_image(in_path, out_path, target_kb)

if __name__ == "__main__":
    folder = input("Enter folder path: ").strip('"')
    target = int(input("Enter target size in KB (default 200): ") or 200)
    compress_folder(folder, target)
