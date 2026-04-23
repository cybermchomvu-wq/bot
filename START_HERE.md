# START HERE 👇

## Football News Website - Getting Started

Welcome! You now have a complete, professional football news website ready to use.

### Quick Start (2 minutes)

1. **Install and Setup** (first time only)
   ```bash
   # Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   
   # Windows
   setup.bat
   ```

2. **Run the Server**
   ```bash
   python main.py
   ```

3. **Open in Browser**
   ```
   http://localhost:5000
   ```

4. **Create Admin Account** (when prompted during setup)
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: Choose something secure

5. **Login and Start Posting!**
   - Go to http://localhost:5000
   - Click "Admin" in top right
   - Click "New Article" to create your first post

---

## 📚 Documentation

- **[README.md](README.md)** - Full documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup guide
- **[PROJECT.md](PROJECT.md)** - Project overview
- **[CONFIG.md](CONFIG.md)** - Configuration & advanced features

---

## 🎯 What This Website Includes

✅ **User Management**
- User registration
- Login/logout
- User authentication

✅ **Article Management**
- Create articles
- Edit articles
- Delete articles
- Add images & videos

✅ **Content Organization**
- Categories (Premier League, Champions League, etc.)
- Article search
- Category filtering
- Pagination

✅ **User Interaction**
- Comments on articles
- Comment system
- User profiles

✅ **Admin Panel**
- Dashboard with statistics
- Article management
- Category management
- User monitoring

---

## 🔧 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Authentication:** Flask-Login

---

## 📁 Project Files

```
app.py                 ← Main application code
main.py                ← Entry point (what runs)
requirements.txt       ← Python dependencies
templates/             ← HTML templates
└── admin/            ← Admin pages
```

---

## 🚀 First Article Tutorial

1. **Run** `python main.py`
2. **Login** with your admin credentials
3. **Go to** Admin Dashboard → New Article
4. **Fill in:**
   - Title: "Title of your article"
   - Category: Choose from dropdown
   - Content: Write your article
   - Image URL: (optional) Link to a football image
   - Video URL: (optional) YouTube embed link
5. **Click** "Publish Article"
6. **View** on home page!

---

## ❓ Help

### Virtual Environment Error?
```bash
# Make sure to activate first
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### Port Already in Use?
Edit `app.py` and change `port=5000` to `port=8000`

### Need to Reset?
Delete `football_news.db` and run setup again

---

## 💡 Pro Tips

- Add multiple categories before posting
- Use high-quality image URLs
- For videos, use YouTube embed links
- Admins can edit/delete any article
- Users can only comment if logged in

---

## 📖 Full Documentation

For detailed information, see:
- **[README.md](README.md)** - Everything explained
- **[CONFIG.md](CONFIG.md)** - Advanced setup

---

## ✨ Features Overview

| Feature | Available |
|---------|-----------|
| Article Creation | ✅ |
| Article Editing | ✅ |
| Article Deletion | ✅ |
| Comments | ✅ |
| Search | ✅ |
| Categories | ✅ |
| User Registration | ✅ |
| Admin Panel | ✅ |
| Mobile Responsive | ✅ |
| Database | ✅ |

---

## 🎬 Next Steps

1. ✅ Setup complete
2. 👉 Run `python main.py`
3. 👉 Login to admin panel
4. 👉 Create first article
5. 👉 View website
6. 👉 Share with friends!

---

**You're all set! Start creating your football news website now!** ⚽

Questions? Check out [PROJECT.md](PROJECT.md) or [QUICKSTART.md](QUICKSTART.md)
