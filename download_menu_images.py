import sqlite3
import os
import urllib.request
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Curated high quality food photography matching Sweets Lab visual aesthetic
IMAGE_MAP = {
    # Crepe & Pancake
    'كريب / بان كيك': 'https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80',
    # Brownies & Chocolate Salads
    'براونيز / سلطات شوكولا': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80',
    # Waffles & Fondant
    'وافل / فوندون': 'https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80',
    # Specific Cakes
    'تشيز كيك': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=600&q=80',
    'تيراميسو': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&q=80',
    'كوكيز كيك': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80',
    'سان سباستيان': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80',
    'رد فيلفت': 'https://images.unsplash.com/photo-1616541823729-00fe0aacd32c?w=600&q=80',
    'كيك شوكولا': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80',
    'كيك دبي / كيك لوتس': 'https://images.unsplash.com/photo-1588195538326-c5b1e9f80a1b?w=600&q=80',
    'معمول بجينة / كنافة بجينة': 'https://images.unsplash.com/photo-1514517604298-cf80e0fb7f1e?w=600&q=80',
    'كريم كراميل': 'https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=600&q=80',
    'انغليش كيك': 'https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=600&q=80',

    # Ice Coffee
    'لاتيه مثلج': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80',
    'سبانيش لاتيه مثلج': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80',
    'سبانيش لاتيه بندق': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80',
    'سبانيش لاتيه كراميل': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80',
    'سبانيش لاتيه فانيليا': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80',
    'آيس تي دراق': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80',
    'فرابيه (بندق - كراميل)': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80',

    # Smoothies
    'سموزي كوكتيل': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80',
    'سموزي تمر ولوز': 'https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=600&q=80',
    'سموزي أناناس': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80',
    'سموزي بولو (ليمون ونعناع)': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&q=80',
    'سموزي فراولة': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80',
    'سموزي مانجو': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80',
    'سموزي موز': 'https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=600&q=80',

    # Milkshakes
    'ميلك شيك شوكولا': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80',
    'ميلك شيك أوريو': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80',
    'ميلك شيك (فراولة - مانجو)': 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=600&q=80',
    'ميلك شيك سبيشال': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600&q=80',

    # Hot Drinks
    'إسبريسو': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600&q=80',
    'ماكياتو': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600&q=80',
    'كورتادو': 'https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80',
    'سبانيش لاتيه ساخن': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&q=80',
    'لوتس لاتيه': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&q=80',
    'بستاشيو لاتيه': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&q=80',
    'فلات وايت': 'https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80',
    'كابتشينو': 'https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80',
    'ميلو': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600&q=80',
    'هوت شوكلت': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600&q=80',
    '3 في 1 (3in1)': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80',
    'قهوة فرنسية': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80',
    'موكا ساخنة': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600&q=80',
    'أمريكانو': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80',
    'نسكافيه خلطة': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80',
}

# Default fallbacks per category
DEFAULT_DRINK_IMG = 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80'
DEFAULT_DESSERT_IMG = 'https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80'

cache = {}

def get_webp_image(name_key, url):
    if name_key in cache:
        return cache[name_key]
    
    clean_name = "".join([c if c.isalnum() else '_' for c in name_key]).strip('_')
    temp_jpg = os.path.join(UPLOAD_FOLDER, f"temp_{clean_name}.jpg")
    webp_filename = f"{clean_name}.webp"
    final_webp = os.path.join(UPLOAD_FOLDER, webp_filename)
    
    try:
        urllib.request.urlretrieve(url, temp_jpg)
        img = Image.open(temp_jpg)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(final_webp, 'WEBP', quality=80)
        if os.path.exists(temp_jpg):
            os.remove(temp_jpg)
        web_path = f"/static/uploads/{webp_filename}"
        cache[name_key] = web_path
        return web_path
    except Exception as e:
        print(f"Error processing {name_key}: {e}")
        return None

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    items = cursor.execute('SELECT * FROM menu_items').fetchall()
    
    updated_count = 0
    for item in items:
        item_id = item['id']
        name_ar = item['name_ar']
        category = item['category']
        
        # Match image URL
        matched_url = None
        for key, url in IMAGE_MAP.items():
            if key in name_ar or name_ar in key:
                matched_url = url
                break
                
        if not matched_url:
            matched_url = DEFAULT_DESSERT_IMG if category == 'dessert' else DEFAULT_DRINK_IMG
            
        key_name = name_ar.split('(')[0].strip() if '(' in name_ar else name_ar
        webp_path = get_webp_image(key_name, matched_url)
        
        if webp_path:
            cursor.execute('UPDATE menu_items SET image_path = ? WHERE id = ?', (webp_path, item_id))
            updated_count += 1
            
    conn.commit()
    conn.close()
    print(f"Successfully processed and updated {updated_count} items with WebP images!")

if __name__ == '__main__':
    main()
