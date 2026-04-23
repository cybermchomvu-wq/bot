from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football_news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    articles = db.relationship('Article', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category', lazy=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comments = db.relationship('Comment', backref='article', lazy=True, cascade='all, delete-orphan')

    def get_snippet(self):
        return self.excerpt or self.content[:150] + '...'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== ROUTES ====================

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', '')

    query = Article.query.order_by(Article.created_at.desc())

    if category:
        query = query.filter_by(category_id=category)

    if search:
        query = query.filter(Article.title.ilike(f'%{search}%') | Article.content.ilike(f'%{search}%'))

    articles = query.paginate(page=page, per_page=10)
    categories = Category.query.all()

    return render_template('index.html', articles=articles, categories=categories, search=search, selected_category=category)


@app.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.created_at.desc()).all()
    return render_template('article.html', article=article, comments=comments)


@app.route('/article/<int:article_id>/comment', methods=['POST'])
@login_required
def add_comment(article_id):
    article = Article.query.get_or_404(article_id)
    content = request.form.get('content', '').strip()

    if not content:
        flash('Comment cannot be empty!', 'warning')
        return redirect(url_for('view_article', article_id=article_id))

    comment = Comment(content=content, author_id=current_user.id, article_id=article_id)
    db.session.add(comment)
    db.session.commit()

    flash('Comment added successfully!', 'success')
    return redirect(url_for('view_article', article_id=article_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied! Admin rights required.', 'danger')
        return redirect(url_for('index'))

    articles = Article.query.all()
    comments = Comment.query.all()
    users = User.query.all()
    categories = Category.query.all()

    return render_template('admin/dashboard.html', 
                         articles=articles, 
                         comments=comments, 
                         users=users,
                         categories=categories)


@app.route('/admin/post', methods=['GET', 'POST'])
@login_required
def admin_post():
    if not current_user.is_admin:
        flash('Access denied! Admin rights required.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        image_url = request.form.get('image_url', '').strip()
        video_url = request.form.get('video_url', '').strip()
        category_id = request.form.get('category_id', type=int)

        if not title or not content or not category_id:
            flash('Title, content, and category are required!', 'warning')
            return redirect(url_for('admin_post'))

        article = Article(
            title=title,
            content=content,
            excerpt=excerpt,
            image_url=image_url,
            video_url=video_url,
            author_id=current_user.id,
            category_id=category_id
        )
        db.session.add(article)
        db.session.commit()

        flash('Article posted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    categories = Category.query.all()
    return render_template('admin/post.html', categories=categories)


@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def admin_edit(article_id):
    article = Article.query.get_or_404(article_id)

    if not current_user.is_admin and article.author_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        article.title = request.form.get('title', '').strip()
        article.content = request.form.get('content', '').strip()
        article.excerpt = request.form.get('excerpt', '').strip()
        article.image_url = request.form.get('image_url', '').strip()
        article.video_url = request.form.get('video_url', '').strip()
        article.category_id = request.form.get('category_id', type=int)
        article.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Article updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    categories = Category.query.all()
    return render_template('admin/edit.html', article=article, categories=categories)


@app.route('/admin/delete/<int:article_id>', methods=['POST'])
@login_required
def admin_delete(article_id):
    article = Article.query.get_or_404(article_id)

    if not current_user.is_admin and article.author_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    db.session.delete(article)
    db.session.commit()
    flash('Article deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/category', methods=['POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    if name and not Category.query.filter_by(name=name).first():
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== CLI COMMANDS ====================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    
    # Create default categories
    if Category.query.count() == 0:
        categories = [
            Category(name='Premier League'),
            Category(name='Champions League'),
            Category(name='International'),
            Category(name='Transfers'),
            Category(name='Highlights'),
            Category(name='Other')
        ]
        db.session.add_all(categories)
        db.session.commit()
        print('Database initialized with default categories.')


@app.cli.command()
def create_admin():
    """Create an admin user."""
    username = input('Enter admin username: ')
    email = input('Enter admin email: ')
    password = input('Enter admin password: ')

    if User.query.filter_by(username=username).first():
        print('Username already exists!')
        return

    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user "{username}" created successfully!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
