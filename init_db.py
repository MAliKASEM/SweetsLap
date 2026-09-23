import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the menu_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            image_path TEXT
        )
    ''')
    
    # Check if table already contains data to avoid duplication
    cursor.execute('SELECT COUNT(*) FROM menu_items')
    if cursor.fetchone()[0] == 0:
        # Seed initial menu items
        initial_items = [
            # Desserts
            (
                'Classic Tiramisu', 
                6.50, 
                'dessert', 
                'Mascarpone cream, espresso-soaked ladyfingers, dark cocoa powder, marsala wine', 
                '/static/uploads/tiramisu.webp'
            ),
            (
                'Pistachio Croissant', 
                4.75, 
                'dessert', 
                'Butter pastry, sweet pistachio paste filling, toasted slivered pistachios', 
                '/static/uploads/pistachio_croissant.webp'
            ),
            (
                'Salted Caramel Macaron Tart', 
                5.50, 
                'dessert', 
                'Sweet pastry crust, rich caramel filling, sea salt flakes, macaron decoration', 
                '/static/uploads/caramel_tart.webp'
            ),
            # Drinks
            (
                'Ceremonial Matcha Latte', 
                5.25, 
                'drink', 
                'Uji ceremonial matcha green tea, steamed whole milk, touch of organic honey', 
                '/static/uploads/matcha_latte.webp'
            ),
            (
                'Vanilla Sweet Cream Cold Brew', 
                4.95, 
                'drink', 
                '20-hour slow-steeped cold brew coffee, house-made vanilla sweet cream, crushed ice', 
                '/static/uploads/cold_brew.webp'
            ),
            (
                'Smoked Rosemary Latte', 
                5.50, 
                'drink', 
                'Double shot espresso, fresh rosemary syrup, steamed oat milk, sprig of charred rosemary', 
                '/static/uploads/rosemary_latte.webp'
            )
        ]
        
        cursor.executemany('''
            INSERT INTO menu_items (name, price, category, ingredients, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', initial_items)
        
        print("Database initialized and seeded successfully!")
    else:
        print("Database already contains items. Skipping seeding.")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Make sure static/uploads directory exists
    uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    init_db()
