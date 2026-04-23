# Quick Start Guide - Football News Website

## 1. Installation (First Time Only)

```bash
# Navigate to the project directory
cd /home/cyber/Downloads/bot

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask init-db

# Create an admin user
flask create-admin
# Follow the prompts to create your admin account
```

## 2. Run the Website

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the Flask server
python main.py

# Or directly:
python app.py
```

The website will be available at: **http://localhost:5000**

## 3. First Use

1. **Create Admin Account** (first time setup)
   - Use `flask create-admin` command
   - You'll need username, email, and password

2. **Login**
   - Go to http://localhost:5000
   - Click "Login"
   - Enter your admin credentials

3. **Create Article Categories** (recommended)
   - Go to Admin Dashboard
   - Navigate to "Categories" tab
   - Add your first category (e.g., "Premier League")

4. **Post Your First Article**
   - Click "New Article" button
   - Fill in the form with article details
   - Optionally add an image URL and video URL
   - Click "Publish Article"

5. **Browse the Website**
   - Non-logged users can view all articles
   - Logged-in users can comment on articles
   - Admin users have access to the admin panel

## 4. File Structure Overview

```
bot/
├── app.py                  # Main Flask application (START HERE)
├── main.py                 # Entry point script
├── requirements.txt        # Python dependencies
├── football_news.db        # Database (auto-created)
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── article.html       # Article detail
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── admin/             # Admin templates
│   │   ├── dashboard.html # Admin dashboard
│   │   ├── post.html      # Create article
│   │   └── edit.html      # Edit article
│   ├── 404.html           # Not found page
│   └── 500.html           # Server error page
```

## 5. Common Commands

### Database Management
```bash
# Initialize database (creates tables)
flask init-db

# Reset database (WARNING: deletes all data!)
python
>>> from app import app, db
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
```

### User Management
```bash
# Create a new admin user
flask create-admin

# Create a regular user (through the website)
# Go to http://localhost:5000/register
```

### Development Server
```bash
# Run with debug mode (auto-reload on code changes)
python main.py

# Run with Gunicorn (production-like)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 6. Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
- Make sure your virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Cannot connect to database"
- Database is created automatically when you run the app
- If issues persist, delete `football_news.db` and restart

### Port 5000 Already in Use
- Edit `app.py` and change `port=5000` to another number (e.g., `port=8000`)

### Articles not showing
- Make sure you've created at least one category
- Create an article and assign it to a category
- Check the database is initialized with `flask init-db`

## 7. Deployment Considerations

For production use:

1. **Change SECRET_KEY** in `app.py`
2. **Use a production database** (PostgreSQL recommended)
3. **Use a production WSGI server** (Gunicorn, uWSGI)
4. **Set DEBUG = False** in configuration
5. **Use environment variables** for sensitive data
6. **Add SSL/HTTPS** with a reverse proxy (Nginx, Apache)

## 8. Adding More Features

To extend the website:
- Add new routes in `app.py`
- Create new HTML templates in `templates/`
- Add new database models following the existing pattern
- Use Bootstrap classes for consistent styling

Happy blogging! ⚽
