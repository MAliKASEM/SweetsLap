import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db(force_reseed=True):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if force_reseed:
        cursor.execute('DROP TABLE IF EXISTS menu_items')
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            image_path TEXT,
            name_ar TEXT DEFAULT '',
            ingredients_ar TEXT DEFAULT ''
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM menu_items')
    if cursor.fetchone()[0] == 0:
        initial_items = [
            # ─────────────────────────────────────────────────────────────
            # DESSERTS / الحلويات
            # ─────────────────────────────────────────────────────────────
            # Crepe & Pancake / كريب - بان كيك
            ('Crepe / Pancake (Sweets Lab Chocolate)', 0.0, 'dessert', 'Sweets Lab Chocolate', None, 'كريب / بان كيك (شوكولا سويتس لاب)', 'شوكولا سويتس لاب'),
            ('Crepe / Pancake (Mars - Twix)', 0.0, 'dessert', 'Mars - Twix', None, 'كريب / بان كيك (مارس - تويكس)', 'مارس - تويكس'),
            ('Crepe / Pancake (Snickers - Crunch)', 0.0, 'dessert', 'Snickers - Crunch', None, 'كريب / بان كيك (سنيكرز - كرانش)', 'سنيكرز - كرانش'),
            ('Crepe / Pancake (Lotus - Bubbly)', 0.0, 'dessert', 'Lotus - Bubbly', None, 'كريب / بان كيك (لوتس - بابلي)', 'لوتس - بابلي'),
            ('Crepe / Pancake (Kinder - Kinder Bueno)', 0.0, 'dessert', 'Kinder - Kinder Bueno', None, 'كريب / بان كيك (كيندر - كيندر بوينو)', 'كيندر - كيندر بوينو'),
            ('Crepe / Pancake (Dubai - Pistachio - Milka)', 0.0, 'dessert', 'Dubai - Pistachio - Milka', None, 'كريب / بان كيك (دبي - بستاشيو - ميلكا)', 'دبي - بستاشيو - ميلكا'),
            ('Crepe / Pancake (Nutella - Maltesers)', 0.0, 'dessert', 'Nutella - Maltesers', None, 'كريب / بان كيك (نوتيلا - مالتيزرز)', 'نوتيلا - مالتيزرز'),

            # Brownies & Chocolate Salads / براونيز - سلطات شوكولا
            ('Brownies / Chocolate Salad (Sweets Lab Chocolate)', 0.0, 'dessert', 'Sweets Lab Chocolate', None, 'براونيز / سلطات شوكولا (شوكولا سويتس لاب)', 'شوكولا سويتس لاب'),
            ('Brownies / Chocolate Salad (Mars - Twix)', 0.0, 'dessert', 'Mars - Twix', None, 'براونيز / سلطات شوكولا (مارس - تويكس)', 'مارس - تويكس'),
            ('Brownies / Chocolate Salad (Bubbly - Snickers)', 0.0, 'dessert', 'Bubbly - Snickers', None, 'براونيز / سلطات شوكولا (بابلي - سنيكرز)', 'بابلي - سنيكرز'),
            ('Brownies / Chocolate Salad (Crunch - Lotus)', 0.0, 'dessert', 'Crunch - Lotus', None, 'براونيز / سلطات شوكولا (كرانش - لوتس)', 'كرانش - لوتس'),
            ('Brownies / Chocolate Salad (Kinder - Kinder Bueno)', 0.0, 'dessert', 'Kinder - Kinder Bueno', None, 'براونيز / سلطات شوكولا (كيندر - كيندر بوينو)', 'كيندر - كيندر بوينو'),
            ('Brownies / Chocolate Salad (Nutella - Pistachio)', 0.0, 'dessert', 'Nutella - Pistachio', None, 'براونيز / سلطات شوكولا (نوتيلا - بستاشيو)', 'نوتيلا - بستاشيو'),
            ('Brownies / Chocolate Salad (Dubai - Maltesers - Milka)', 0.0, 'dessert', 'Dubai - Maltesers - Milka', None, 'براونيز / سلطات شوكولا (دبي - مالتيزر - ميلكا)', 'دبي - مالتيزر - ميلكا'),

            # Fondant & Waffle / وافل - فوندون
            ('Waffle / Fondant (Sweets Lab Chocolate)', 0.0, 'dessert', 'Sweets Lab Chocolate', None, 'وافل / فوندون (شوكولا سويتس لاب)', 'شوكولا سويتس لاب'),
            ('Waffle / Fondant (Mars - Twix)', 0.0, 'dessert', 'Mars - Twix', None, 'وافل / فوندون (مارس - تويكس)', 'مارس - تويكس'),
            ('Waffle / Fondant (Snickers - Crunch)', 0.0, 'dessert', 'Snickers - Crunch', None, 'وافل / فوندون (سنيكرز - كرانش)', 'سنيكرز - كرانش'),
            ('Waffle / Fondant (Lotus - Bubbly)', 0.0, 'dessert', 'Lotus - Bubbly', None, 'وافل / فوندون (لوتس - بابلي)', 'لوتس - بابلي'),
            ('Waffle / Fondant (Kinder - Kinder Bueno)', 0.0, 'dessert', 'Kinder - Kinder Bueno', None, 'وافل / فوندون (كيندر - كيندر بوينو)', 'كيندر - كيندر بوينو'),
            ('Waffle / Fondant (Dubai - Pistachio - Milka)', 0.0, 'dessert', 'Dubai - Pistachio - Milka', None, 'وافل / فوندون (دبي - بستاشيو - ميلكا)', 'دبي - بستاشيو - ميلكا'),
            ('Waffle / Fondant (Nutella - Maltesers)', 0.0, 'dessert', 'Nutella - Maltesers', None, 'وافل / فوندون (نوتيلا - مالتيزرز)', 'نوتيلا - مالتيزرز'),

            # Cakes / كيك
            ('Cheesecake', 0.0, 'dessert', 'Strawberry, Blueberry, Cherry, Lotus, Pistachio, Chocolate, Kinder', None, 'تشيز كيك', 'فريز - توت - كرز - لوتس - بستاشيو - شوكولا - كيندر'),
            ('Tiramisu', 0.0, 'dessert', 'Classic Italian Tiramisu', None, 'تيراميسو', 'تيراميسو إيطالي فاخر'),
            ('Cookies Cake', 0.0, 'dessert', 'Rich Chocolate Chips Cookies Cake', None, 'كوكيز كيك', 'كيك الكوكيز الغني بالشوكولاتة'),
            ('San Sebastian Cheesecake', 0.0, 'dessert', 'Burnt San Sebastian Cheesecake', None, 'سان سباستيان', 'تشيز كيك سان سباستيان المحروق'),
            ('Red Velvet Cake', 0.0, 'dessert', 'Classic Red Velvet Cake', None, 'رد فيلفت', 'كيك الرد فيلفت الكلاسيكي'),
            ('Chocolate Cake', 0.0, 'dessert', 'Rich Chocolate Cake', None, 'كيك شوكولا', 'كيك الشوكولا الغنية'),
            ('Dubai Cake / Lotus Cake', 0.0, 'dessert', 'Special Dubai Cake or Lotus Cake', None, 'كيك دبي / كيك لوتس', 'كيك دبي المميز أو كيك اللوتس'),
            ('Cheese Maamoul / Cheese Kunafa', 0.0, 'dessert', 'Cheese Maamoul or Sweet Cheese Kunafa', None, 'معمول بجينة / كنافة بجينة', 'معمول بالجبنة أو كنافة ناعمة بالجبنة'),
            ('Creme Caramel', 0.0, 'dessert', 'Smooth Caramel Custard', None, 'كريم كراميل', 'كريم كراميل ناعم وغني'),
            ('English Cake', 0.0, 'dessert', 'Classic English Cake', None, 'انغليش كيك', 'انغليش كيك كلاسيكي'),

            # ─────────────────────────────────────────────────────────────
            # DRINKS / المشروبات
            # ─────────────────────────────────────────────────────────────
            # Ice Coffee / ايس كوفي
            ('Iced Latte', 0.0, 'drink', 'Espresso with cold milk & ice', None, 'لاتيه مثلج', 'قهوة اسبريسو مع حليب بارد ومثلج'),
            ('Iced Spanish Latte', 0.0, 'drink', 'Espresso with condensed milk & ice', None, 'سبانيش لاتيه مثلج', 'اسبريسو مع حليب مكثف ومثلج'),
            ('Hazelnut Spanish Latte', 0.0, 'drink', 'Spanish latte with hazelnut flavor', None, 'سبانيش لاتيه بندق', 'سبانيش لاتيه بنكهة البندق'),
            ('Caramel Spanish Latte', 0.0, 'drink', 'Spanish latte with caramel flavor', None, 'سبانيش لاتيه كراميل', 'سبانيش لاتيه بنكهة الكراميل'),
            ('Vanilla Spanish Latte', 0.0, 'drink', 'Spanish latte with vanilla flavor', None, 'سبانيش لاتيه فانيليا', 'سبانيش لاتيه بنكهة الفانيليا'),
            ('Peach Iced Tea', 0.0, 'drink', 'Refreshing peach flavored iced tea', None, 'آيس تي دراق', 'شاي مثلج بنكهة الخوخ المنعش'),
            ('Frappe (Hazelnut - Caramel)', 0.0, 'drink', 'Iced frappe with hazelnut or caramel', None, 'فرابيه (بندق - كراميل)', 'فرابيه مثلج بنكهة البندق أو الكراميل'),

            # Smoothies / سموزي
            ('Cocktail Smoothie', 0.0, 'drink', 'Fresh mixed fruits blend', None, 'سموزي كوكتيل', 'مزيج الفواكه الطازجة المنعش'),
            ('Date & Almond Smoothie', 0.0, 'drink', 'Natural dates with almond & milk', None, 'سموزي تمر ولوز', 'تمر طبيعي مع اللوز والحليب'),
            ('Pineapple Smoothie', 0.0, 'drink', 'Fresh refreshing pineapple', None, 'سموزي أناناس', 'أناناس طازج منعش'),
            ('Polo Smoothie (Lemon & Mint)', 0.0, 'drink', 'Iced lemon & mint', None, 'سموزي بولو (ليمون ونعناع)', 'ليمون ونعناع مثلج'),
            ('Strawberry Smoothie', 0.0, 'drink', 'Fresh iced strawberries', None, 'سموزي فراولة', 'فراولة طازجة مثلجة'),
            ('Mango Smoothie', 0.0, 'drink', 'Fresh tropical mango', None, 'سموزي مانجو', 'مانجو استوائية منعشة'),
            ('Banana Smoothie', 0.0, 'drink', 'Fresh banana with milk', None, 'سموزي موز', 'موز طازج مع الحليب'),

            # Milkshakes / ميلك شيك
            ('Chocolate Milkshake', 0.0, 'drink', 'Rich chocolate milkshake', None, 'ميلك شيك شوكولا', 'ميلك شيك الشوكولاتة الغنية'),
            ('Oreo Milkshake', 0.0, 'drink', 'Milkshake blended with Oreo cookies', None, 'ميلك شيك أوريو', 'ميلك شيك مع قطع الأوريو'),
            ('Strawberry / Mango Milkshake', 0.0, 'drink', 'Fresh strawberry or mango flavor', None, 'ميلك شيك (فراولة - مانجو)', 'بنكهة الفراولة الطازجة أو المانجو'),
            ('Special Chocolate Milkshake', 0.0, 'drink', 'Twix, Mars, Snickers, Crunch, Galaxy, Bubbly, Kinder, Kinder Bueno, Cookies, Brownies', None, 'ميلك شيك سبيشال', 'تويكس - مارس - سنيكرز - كرانش - جالكسي - بابلي - كيندر - كيندر بوينو - كوكيز - براونيز'),

            # Hot Drinks / ساخن
            ('Espresso', 0.0, 'drink', 'Single / Double shot espresso', None, 'إسبريسو', 'جرعة إسبريسو مركزة'),
            ('Macchiato', 0.0, 'drink', 'Espresso marked with foamed milk', None, 'ماكياتو', 'إسبريسو مع رغوة الحليب'),
            ('Cortado', 0.0, 'drink', 'Equal parts espresso & steamed milk', None, 'كورتادو', 'إسبريسو متساوي مع حليب مبخر'),
            ('Hot Spanish Latte', 0.0, 'drink', 'Espresso with steamed condensed milk', None, 'سبانيش لاتيه ساخن', 'إسبريسو مع حليب مكثف ومبخر'),
            ('Lotus Latte', 0.0, 'drink', 'Latte with rich Lotus Biscoff paste', None, 'لوتس لاتيه', 'لاتيه بنكهة زبدة اللوتس'),
            ('Pistachio Latte', 0.0, 'drink', 'Latte infused with pistachio cream', None, 'بستاشيو لاتيه', 'لاتيه بنكهة الفستق الحلبي'),
            ('Flat White', 0.0, 'drink', 'Double shot espresso with microfoam', None, 'فلات وايت', 'إسبريسو مزدوج مع طبقة رقيقة من الحليب'),
            ('Cappuccino', 0.0, 'drink', 'Espresso, steamed milk & thick foam', None, 'كابتشينو', 'إسبريسو مع حليب كثيف ورغوة غنية'),
            ('Milo', 0.0, 'drink', 'Hot chocolate malt Milo drink', None, 'ميلو', 'مشروب الميلو بالشوكولاتة والكاكاو'),
            ('Hot Chocolate', 0.0, 'drink', 'Rich creamy hot chocolate', None, 'هوت شوكلت', 'شوكولاتة ساخنة غنية'),
            ('3 in 1 Coffee', 0.0, 'drink', 'Instant coffee with creamer & sugar', None, '3 في 1 (3in1)', 'قهوة سريعة التحضير مع مبيض وسكر'),
            ('French Coffee', 0.0, 'drink', 'French coffee with hazelnut milk', None, 'قهوة فرنسية', 'قهوة فرنسية بالحليب والبندق'),
            ('Hot Mocha', 0.0, 'drink', 'Espresso, cocoa & steamed milk', None, 'موكا ساخنة', 'إسبريسو مع كاكاو وحليب مبخر'),
            ('Americano', 0.0, 'drink', 'Espresso diluted with hot water', None, 'أمريكانو', 'إسبريسو مخفف بالماء الساخن'),
            ('Nescafé Special Blend', 0.0, 'drink', 'House special Nescafé blend', None, 'نسكافيه خلطة', 'خلطة نسكافيه الخاصة من سويتس لاب')
        ]
        
        cursor.executemany('''
            INSERT INTO menu_items (name, price, category, ingredients, image_path, name_ar, ingredients_ar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', initial_items)
        
        print(f"Database initialized and seeded successfully with {len(initial_items)} items!")
    else:
        print("Database already contains items. Skipping seeding.")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    init_db(force_reseed=True)
