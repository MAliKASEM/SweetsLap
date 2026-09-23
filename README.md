# Sweet Creams Cafe - Website & Admin Panel

A fast, lightweight, and premium responsive web application for a coffee and dessert shop. Designed with strict performance optimizations for slow internet connections, featuring server-side rendered text, native and progressive image lazy-loading, shimmer skeleton cards, and local image compression.

## Technology Stack
- **Backend**: Python 3, Flask, SQLite3
- **Frontend**: Vanilla HTML5, Vanilla CSS3 (Custom Glassmorphism, Google Fonts), Vanilla JavaScript (no external libraries/frameworks)
- **Image Processing**: Pillow (automatic conversion to optimized WebP format with 75% quality compression and size limiting)

---

## Local Setup & Installation

Follow these quick steps to get the app running locally on your machine:

### 1. Prerequisites
Ensure you have **Python 3.8+** installed. You can check your version by running:
```bash
python --version
```

### 2. Clone/Open the Project Directory
Navigate into the workspace folder containing the code:
```bash
cd coffee_shop
```

### 3. Create and Activate a Virtual Environment (Recommended)
Creating a virtual environment isolates dependencies:
- **Windows**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install Flask and Pillow using the requirements file:
```bash
pip install -r requirements.txt
```

### 5. Initialize the Database
Run the setup script to build the SQLite database structure (`database.db`) and seed it with initial drink and dessert items:
```bash
python init_db.py
```
*Note: This script will create a `static/uploads` directory where all future uploaded menu photos will be stored.*

### 6. Run the Development Server
Launch the Flask development server:
```bash
python app.py
```
The application will boot up at **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**.

---

## Features & Key Highlights

### 🚀 Slow-Internet Optimization
1. **Instant Text Rendering (SSR)**: The menu text (names, prices, ingredients) is rendered directly inside the HTML server-side. It displays instantly without waiting for any JavaScript or asynchronous API responses.
2. **Skeleton Shimmer Placeholders**: While the images are downloading, beautiful CSS-only shimmer boxes act as placeholders. This ensures **Zero Cumulative Layout Shift (CLS)**, making the site feel fast and stable.
3. **Lazy Image Loading**: Images only load when they scroll into the viewport using the browser's `IntersectionObserver` with a fallback to native browser lazy loading.
4. **Admin Image Auto-Compression**: When an admin uploads a new food/drink photo, Pillow automatically resizes the image (max width 600px) and converts it to the lightweight **WebP** format. This compresses a typical 5MB smartphone photo down to roughly **30KB** without visible quality loss.

### 🌐 GitHub Pages Deployment

This project includes an automated static builder and GitHub Actions workflow for deployment to **GitHub Pages**.

#### 1. Build Static Output Locally
To generate the static HTML files locally inside `dist/`:
```bash
python build.py
```
You can test the static site locally with:
```bash
python -m http.server 8000 --directory dist
```
Then visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

#### 2. Deploy to GitHub Pages (Automated via GitHub Actions)
1. Push your repository to GitHub (`main` or `master` branch).
2. On GitHub, go to your repository **Settings** -> **Pages**.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions**.
4. GitHub Actions will automatically run `.github/workflows/deploy.yml`, build the static site via `build.py`, and deploy it live to your GitHub Pages URL!

