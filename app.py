import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'sweets_lab_secret_key_2026'

# ╔══════════════════════════════════════════════════════════════════╗
# ║              ADMIN CREDENTIALS — CHANGE THESE HERE              ║
# ║   To update: edit ADMIN_USERNAME and ADMIN_PASSWORD below,      ║
# ║   then restart the server (Ctrl+C then run app.py again).       ║
# ╚══════════════════════════════════════════════════════════════════╝
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'sweetlab2026'

# ── Language context processor ──────────────────────────────────────
@app.context_processor
def inject_lang():
    """Make `lang` and `admin_logged_in` available in every template."""
    return {
        'lang': session.get('lang', 'en'),
        'admin_logged_in': session.get('admin_logged_in', False)
    }

# ── Auth decorator ───────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Limit upload size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_and_save_image(file, filename):
    """
    Saves the image by compressing it and converting to WebP for high performance.
    Resizes image to a max width of 600px while keeping aspect ratio.
    """
    img = Image.open(file)
    
    # Convert RGBA to RGB if saving as WebP/JPEG to avoid transparency issues
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Resize image if too large
    max_width = 600
    if img.width > max_width:
        w_percent = (max_width / float(img.width))
        h_size = int((float(img.height) * float(w_percent)))
        img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
        
    # Generate webp filename
    name_without_ext = os.path.splitext(secure_filename(filename))[0]
    webp_filename = f"{name_without_ext}_{int(os.path.getmtime(DATABASE) if os.path.exists(DATABASE) else 0) or 1}.webp"
    # Ensure name uniqueness
    counter = 1
    dest_path = os.path.join(app.config['UPLOAD_FOLDER'], webp_filename)
    while os.path.exists(dest_path):
        webp_filename = f"{name_without_ext}_{counter}.webp"
        dest_path = os.path.join(app.config['UPLOAD_FOLDER'], webp_filename)
        counter += 1
        
    # Save optimized webp image
    img.save(dest_path, 'WEBP', quality=75)
    return f"/static/uploads/{webp_filename}"

# ── Public Pages ─────────────────────────────────────────────────────

@app.route('/set-lang/<lang_code>')
def set_lang(lang_code):
    """Store language preference in session and redirect back."""
    if lang_code in ('en', 'ar'):
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu_items ORDER BY name ASC').fetchall()
    conn.close()
    drinks = [dict(item) for item in items if item['category'] == 'drink']
    desserts = [dict(item) for item in items if item['category'] == 'dessert']
    return render_template('index.html', drinks=drinks, desserts=desserts)

# ── Admin Auth ───────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Incorrect username or password. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu_items ORDER BY name ASC').fetchall()
    conn.close()
    return render_template('admin.html', items=items)

# ── API Endpoints (write operations protected) ───────────────────────

@app.route('/api/menu', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu_items ORDER BY name ASC').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/menu', methods=['POST'])
@api_login_required
def add_item():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        ingredients = request.form.get('ingredients')
        name_ar = request.form.get('name_ar', '')
        ingredients_ar = request.form.get('ingredients_ar', '')
        
        if not name or not price or not category or not ingredients:
            return jsonify({'error': 'Missing required fields'}), 400
            
        try:
            price = float(price)
        except ValueError:
            return jsonify({'error': 'Price must be a valid number'}), 400
            
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                image_path = compress_and_save_image(file, file.filename)
                
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO menu_items (name, price, category, ingredients, image_path, name_ar, ingredients_ar) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, price, category, ingredients, image_path, name_ar, ingredients_ar)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Item added successfully',
            'item': {
                'id': new_id,
                'name': name,
                'price': price,
                'category': category,
                'ingredients': ingredients,
                'image_path': image_path,
                'name_ar': name_ar,
                'ingredients_ar': ingredients_ar
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu/<int:item_id>', methods=['POST', 'PUT'])
@api_login_required
def update_item(item_id):
    try:
        conn = get_db_connection()
        item = conn.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,)).fetchone()
        
        if not item:
            conn.close()
            return jsonify({'error': 'Item not found'}), 404
            
        name = request.form.get('name', item['name'])
        price = request.form.get('price', item['price'])
        category = request.form.get('category', item['category'])
        ingredients = request.form.get('ingredients', item['ingredients'])
        name_ar = request.form.get('name_ar', item['name_ar'] or '')
        ingredients_ar = request.form.get('ingredients_ar', item['ingredients_ar'] or '')
        
        try:
            price = float(price)
        except ValueError:
            conn.close()
            return jsonify({'error': 'Price must be a valid number'}), 400
            
        image_path = item['image_path']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                if image_path and '/static/uploads/' in image_path:
                    old_file_path = os.path.join(BASE_DIR, image_path.lstrip('/'))
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except Exception as e:
                            print(f"Error removing old file: {e}")
                image_path = compress_and_save_image(file, file.filename)
                
        conn.execute('''
            UPDATE menu_items 
            SET name = ?, price = ?, category = ?, ingredients = ?, image_path = ?, name_ar = ?, ingredients_ar = ?
            WHERE id = ?
        ''', (name, price, category, ingredients, image_path, name_ar, ingredients_ar, item_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Item updated successfully',
            'item': {
                'id': item_id,
                'name': name,
                'price': price,
                'category': category,
                'ingredients': ingredients,
                'image_path': image_path,
                'name_ar': name_ar,
                'ingredients_ar': ingredients_ar
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu/<int:item_id>', methods=['DELETE'])
@api_login_required
def delete_item(item_id):
    try:
        conn = get_db_connection()
        item = conn.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,)).fetchone()
        
        if not item:
            conn.close()
            return jsonify({'error': 'Item not found'}), 404
            
        image_path = item['image_path']
        if image_path and '/static/uploads/' in image_path:
            file_path = os.path.join(BASE_DIR, image_path.lstrip('/'))
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing file: {e}")
                    
        conn.execute('DELETE FROM menu_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
