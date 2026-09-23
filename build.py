#!/usr/bin/env python3
"""
build.py - Sweets Lab Static Exporter for GitHub Pages

Renders the Flask app's routes into static HTML files in the `dist/` directory,
adjusts asset paths to be relative for GitHub Pages subpath compatibility,
and copies all static assets.
"""

import os
import shutil
import re
from app import app, get_db_connection

DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')

def prepare_dist():
    """Clean and create dist directory."""
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)

def copy_static():
    """Copy static files to dist/static."""
    src_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    dst_static = os.path.join(DIST_DIR, 'static')
    shutil.copytree(src_static, dst_static)
    print("✓ Copied static assets to dist/static")

def fix_paths_for_gh_pages(html_content, is_subfolder=False):
    """
    Adjust paths to relative for GitHub Pages compatibility:
    - /static/ -> static/ (or ../static/ if in subfolder)
    - /set-lang/ar -> ar.html
    - /set-lang/en -> index.html
    - href="/" -> href="index.html"
    - href="/admin" -> href="login.html"
    """
    prefix = "../" if is_subfolder else "./"
    
    # Replace static links
    html_content = re.sub(r'href="/static/', f'href="{prefix}static/', html_content)
    html_content = re.sub(r'src="/static/', f'src="{prefix}static/', html_content)
    html_content = re.sub(r'data-src="/static/', f'data-src="{prefix}static/', html_content)
    
    # Replace language toggle links
    html_content = html_content.replace('/set-lang/ar', f'{prefix}ar.html')
    html_content = html_content.replace('/set-lang/en', f'{prefix}index.html')
    
    # Replace root links
    html_content = re.sub(r'href="/"', f'href="{prefix}index.html"', html_content)
    html_content = re.sub(r'href="/admin"', f'href="{prefix}login.html"', html_content)
    html_content = re.sub(r'href="/admin/login"', f'href="{prefix}login.html"', html_content)
    html_content = re.sub(r'href="/admin/logout"', f'href="{prefix}index.html"', html_content)
    
    return html_content

def build_pages():
    """Render routes using Flask test_client."""
    client = app.test_client()
    
    # 1. English Homepage (index.html)
    with client.session_transaction() as sess:
        sess['lang'] = 'en'
    res_en = client.get('/')
    html_en = fix_paths_for_gh_pages(res_en.get_data(as_text=True))
    with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_en)
    print("✓ Rendered dist/index.html (English)")
    
    # 2. Arabic Homepage (ar.html)
    with client.session_transaction() as sess:
        sess['lang'] = 'ar'
    res_ar = client.get('/')
    html_ar = fix_paths_for_gh_pages(res_ar.get_data(as_text=True))
    with open(os.path.join(DIST_DIR, 'ar.html'), 'w', encoding='utf-8') as f:
        f.write(html_ar)
    print("✓ Rendered dist/ar.html (Arabic)")

    # 3. Login Page (login.html)
    res_login = client.get('/admin/login')
    html_login = fix_paths_for_gh_pages(res_login.get_data(as_text=True))
    with open(os.path.join(DIST_DIR, 'login.html'), 'w', encoding='utf-8') as f:
        f.write(html_login)
    print("✓ Rendered dist/login.html")

    # 4. Create .nojekyll to prevent GitHub Pages from ignoring files starting with _
    with open(os.path.join(DIST_DIR, '.nojekyll'), 'w', encoding='utf-8') as f:
        f.write('')
    print("✓ Created dist/.nojekyll")

def main():
    print("Building static site for GitHub Pages...")
    prepare_dist()
    copy_static()
    build_pages()
    print("\n✓ Build completed successfully! Files generated in dist/")

if __name__ == '__main__':
    main()
