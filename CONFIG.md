# Football News Website - Configuration & Development Guide

## Configuration

### Environment Variables

You can configure the app using environment variables. Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key-change-for-production
FLASK_ENV=development
DEBUG=True
SQLALCHEMY_DATABASE_URI=sqlite:///football_news.db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Database Configuration

#### SQLite (Default)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///football_news.db'
```

#### PostgreSQL
```python
# Install: pip install psycopg2
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/football_news'
```

#### MySQL
```python
# Install: pip install pymysql
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/football_news'
```

## API Routes

### Public Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home page with article list |
| GET | `/article/<id>` | View single article |
| POST | `/article/<id>/comment` | Add comment (requires login) |
| GET | `/login` | Login page |
| GET | `/register` | Registration page |
| POST | `/login` | Process login |
| POST | `/register` | Process registration |
| GET | `/logout` | Logout user |

### Admin Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/admin/dashboard` | Admin dashboard |
| GET | `/admin/post` | Create article page |
| POST | `/admin/post` | Create new article |
| GET | `/admin/edit/<id>` | Edit article page |
| POST | `/admin/edit/<id>` | Update article |
| POST | `/admin/delete/<id>` | Delete article |
| POST | `/admin/category` | Create category |
| POST | `/admin/delete-category/<id>` | Delete category |

### CLI Commands

```bash
# Initialize database with default categories
flask init-db

# Create admin user (interactive)
flask create-admin
```

## Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
```

### Categories Table
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
```

### Articles Table
```sql
CREATE TABLE article (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(300),
    image_url VARCHAR(500),
    video_url VARCHAR(500),
    author_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);
```

### Comments Table
```sql
CREATE TABLE comment (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user(id),
    FOREIGN KEY (article_id) REFERENCES article(id)
);
```

## Development

### Running Tests

Create `test_app.py`:

```python
import unittest
from app import app, db

class TestFootballNews(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_app.py
```

### Debug Mode

For development with auto-reload and interactive debugger:

```bash
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

## Security Best Practices

1. **Change SECRET_KEY**
   ```python
   import secrets
   secrets.token_hex(32)  # Generate a secure key
   ```

2. **HTTPS/SSL**
   - Use a reverse proxy (Nginx, Apache)
   - Get free SSL from Let's Encrypt

3. **SQL Injection Prevention**
   - SQLAlchemy with parameterized queries (already implemented)

4. **CSRF Protection**
   - Flask-WTF csrf tokens (already implemented)

5. **Password Hashing**
   - Werkzeug security (already implemented)

6. **Input Validation**
   - Sanitize user inputs before storing
   - Validate file uploads if implemented

## Performance Optimization

### Database Indexing
```python
# Add indexes for frequently searched columns
class Article(db.Model):
    title = db.Column(db.String(200), index=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
```

### Caching
```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=60)
def index():
    # This will be cached for 60 seconds
    pass
```

### Pagination
- Already implemented in the home page (10 articles per page)
- Adjust `per_page=10` in `app.py` if needed

## Deployment

### Development
```bash
python main.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### With Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t football-news .
docker run -p 5000:5000 football-news
```

## Extending the Application

### Add Email Notifications
```bash
pip install Flask-Mail
```

### Add Image Upload
```bash
pip install Flask-Uploads
```

### Add Search Features
```bash
pip install elasticsearch
```

### Add Social Authentication
```bash
pip install Flask-OAuth
```

## Troubleshooting

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Database Locked
- Close other instances of the app
- Delete `.db-wal` and `.db-shm` files if using SQLite

### Admin Panel Not Accessible
- Verify user `is_admin` is set to `True` in database
- Check login status in browser

### Images Not Loading
- Verify image URLs are correct and publicly accessible
- Use full URLs (https://...) not relative paths

## License

MIT License - Feel free to use and modify!
