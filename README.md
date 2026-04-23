# Football News Website

A modern, feature-rich web application for posting and sharing football news, highlights, and information built with Flask and SQLAlchemy.

## Features

✨ **Core Features:**
- 📰 News feed with article browsing and search functionality
- 👤 User registration and authentication system
- 💬 Comments system on articles
- 📂 Category-based article organization and filtering
- 🎥 Support for video/highlights embedding
- 🖼️ Featured images for articles
- 📱 Fully responsive design

✨ **Admin Panel:**
- 📝 Create, edit, and delete articles
- 🏷️ Manage categories
- 👥 Monitor users and comments
- 📊 Dashboard with statistics

## Technology Stack

- **Backend:** Flask 2.3.2
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login
- **Security:** Werkzeug password hashing

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone/Download the project**
   ```bash
   cd bot
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```
   
   Or use the CLI command:
   ```bash
   flask init-db
   ```

5. **Create admin user**
   ```bash
   flask create-admin
   ```
   Follow the prompts to enter admin credentials.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the website**
   - Open your browser and navigate to `http://localhost:5000`
   - Admin panel: Login with admin credentials and click the Admin link

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── football_news.db       # SQLite database (auto-created)
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── article.html      # Article detail page
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── 404.html          # 404 error page
    ├── 500.html          # 500 error page
    └── admin/
        ├── dashboard.html # Admin dashboard
        ├── post.html     # Create article page
        └── edit.html     # Edit article page
```

## Usage

### For Users

1. **Register/Login**
   - Click "Register" to create a new account
   - Login with your credentials

2. **Browse Articles**
   - View latest football news on the home page
   - Filter by categories using the dropdown
   - Search articles using the search bar

3. **Read Articles**
   - Click "Read More" to view full article
   - Watch embedded videos/highlights
   - Leave comments on articles

### For Admins

1. **Access Admin Panel**
   - Login with admin account
   - Click "Admin" in the navigation bar

2. **Create Articles**
   - Click "New Article" button
   - Fill in title, content, category, and images
   - Optionally add video URLs
   - Click "Publish Article"

3. **Manage Content**
   - Edit or delete existing articles
   - Manage categories
   - Monitor user comments
   - View statistics

## Database Models

### User
- id, username, email, password, is_admin
- Relationships: articles, comments

### Category
- id, name
- Relationships: articles

### Article
- id, title, content, excerpt, image_url, video_url
- author_id, category_id, created_at, updated_at
- Relationships: author (User), category, comments

### Comment
- id, content, author_id, article_id, created_at
- Relationships: author (User), article

## Configuration

Edit these settings in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football_news.db'
```

⚠️ **Important:** Change the SECRET_KEY before deploying to production!

## Default Categories

The following categories are created on first initialization:
- Premier League
- Champions League
- International
- Transfers
- Highlights
- Other

## Contributing

Feel free to fork, modify, and improve this project!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the code comments or modify as needed for your requirements.

---

**Happy blogging with your Football News site!** ⚽