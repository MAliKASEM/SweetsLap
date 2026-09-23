import os
from PIL import Image

ARTIFACTS_DIR = r"C:\Users\Surface Pro\.gemini\antigravity-ide\brain\7b2ce93e-3928-4be5-aa41-c78491d1c725"
DEST_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

os.makedirs(DEST_DIR, exist_ok=True)

# List of generated files in artifacts
image_mapping = {
    "tiramisu_1780695055308.png": "tiramisu.webp",
    "pistachio_croissant_1780695090772.png": "pistachio_croissant.webp",
    "caramel_tart_1780695127105.png": "caramel_tart.webp",
    "matcha_latte_1780695155335.png": "matcha_latte.webp",
    "cold_brew_1780695186034.png": "cold_brew.webp",
    "rosemary_latte_1780695212096.png": "rosemary_latte.webp"
}

def process_and_compress():
    print("Processing generated images and compressing to WebP...")
    for src_name, dest_name in image_mapping.items():
        src_path = os.path.join(ARTIFACTS_DIR, src_name)
        dest_path = os.path.join(DEST_DIR, dest_name)
        
        if os.path.exists(src_path):
            try:
                img = Image.open(src_path)
                
                # Convert RGBA to RGB
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to max width 600px
                max_width = 600
                if img.width > max_width:
                    w_percent = (max_width / float(img.width))
                    h_size = int((float(img.height) * float(w_percent)))
                    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
                
                # Save as webp with 75% quality
                img.save(dest_path, 'WEBP', quality=75)
                print(f"Compressed {src_name} -> {dest_name} (saved to static/uploads)")
            except Exception as e:
                print(f"Error processing {src_name}: {e}")
        else:
            print(f"Source file not found: {src_path}")

if __name__ == '__main__':
    process_and_compress()
