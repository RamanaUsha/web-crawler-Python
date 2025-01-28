import os
import csv
import requests
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin
from threading import Thread
from werkzeug.security import check_password_hash
from database_module import get_user_data, validate_password
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from models import User  # Assuming you have a User model in a separate file or database
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_login import current_user
from flask import render_template, request, flash, redirect, url_for
from flask_mail import Message
from flask_migrate import Migrate
from models import db, User
import hashlib
import bcrypt
import base64
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import logging
import asyncio
import aiohttp
from datetime import datetime
import json
from flask import jsonify
from flask import send_file
import csv
import io
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from extensions import mail  # Importing from the new file
from flask_mail import Message


app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'crawl_database.db'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Or your email provider's SMTP server
app.config['MAIL_PORT'] = 587 # Use 465 for SSL, 587 for TLS
app.config['MAIL_USE_TLS'] = True  # True if using port 587
app.config['MAIL_USE_SSL'] = False  # True if using port 465
app.config['MAIL_USERNAME'] = 'rusha71771@gmail.com'
app.config['MAIL_PASSWORD'] = 'vyhx vuoa kajb mygc'
app.config['MAIL_DEFAULT_SENDER'] = 'rusha71771@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
mail.init_app(app)


# Database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crawl_database.db'  # Use a relative path for SQLite, or a full URI for other databases
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, but recommended to turn off track modifications to save memory

app.config['SECRET_KEY'] = 'your_secret_key_here'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.route('/send_test_email')
def send_test_email():
    try:
        msg = Message('Test Email', recipients=['rusha71771@gmail.com'])
        msg.body = 'This is a test email from Flask-Mail.'
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f'Error sending email: {str(e)}'

# For generating reset tokens
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set the login view for redirects when not logged in

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



# User class for Flask-Login
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)

    def __init__(self, id, username, password, email, profile_picture=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.profile_picture = profile_picture

    # Flask-Login requires a user_loader function for retrieving users by their ID.
    @staticmethod
    def get(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()


def get_user_data(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('crawl_database.db')
    cursor = conn.cursor()

    # Query to fetch the user data by username
    cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    conn.close()

    # If user found, return user data (username and hashed password)
    if user_data:
        return {'username': user_data[0], 'password': user_data[1]}
    return None

# Function to validate the user's password
def validate_password(stored_password_hash, password):
    # Check if the password matches the stored hash
    return check_password_hash(stored_password_hash, password)
# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user_data:
        # Directly access columns instead of using get()
        return User(user_data['id'], user_data['username'], user_data['password'], user_data['email'], user_data['profile_picture'])
    return None



@app.route('/')
def home():
    logged_in = 'username' in session
    return render_template('home.html', logged_in=logged_in)

def ensure_upload_folder_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about_1')
def about_1():
    return render_template('about_1.html')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')




@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            msg = Message(f'Contact from {name}',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['your_email@example.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash('Failed to send message. Please try again.', 'danger')
            print(f"Error: {e}")
        return redirect(url_for('contact'))

    return render_template('contact.html')



@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/documentation_1')
def documentation_1():
    return render_template('documentation_1.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')



def start_crawl_in_thread(start_url, max_pages, max_depth, keyword, user_id):
    crawl_history, pages_crawled = crawl_links(start_url, max_pages, max_depth, keyword)
    save_crawl_history(user_id, crawl_history, 'success', pages_crawled)

def insert_search_history(user_id, url):
    # Assuming you have a connection to your SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    # Insert the crawled URL into the search_history table
    cursor.execute("""
        INSERT INTO search_history (user_id, url)
        VALUES (?, ?)
    """, (user_id, url))
    
    conn.commit()
    conn.close()
def get_search_history(user_id):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    # Fetch the search history for a specific user
    cursor.execute("""
        SELECT url, timestamp 
        FROM search_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))
    
    history = cursor.fetchall()
    conn.close()
    return history



logging.basicConfig(level=logging.INFO)

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

async def crawl_page(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if html:
            return html
        else:
            return None

async def crawl_links(url, max_pages, max_depth, keyword):
    visited = set()
    crawl_history = []
    to_visit = [(url, 0)]  # URL, Depth
    pages_crawled = 0

    while to_visit and len(crawl_history) < max_pages:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth > max_depth:
            continue

        visited.add(current_url)
        html = await crawl_page(current_url)
        
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        meta_data = extract_meta_tags(soup)
        
        if keyword.lower() in title.lower() or not keyword:
            crawl_history.append({
                'title': title,
                'url': current_url,
                'meta': meta_data
            })
            pages_crawled += 1

        for link in soup.find_all('a', href=True):
            full_url = requests.compat.urljoin(current_url, link['href'])
            if full_url not in visited and len(crawl_history) < max_pages:
                to_visit.append((full_url, depth + 1))

        await asyncio.sleep(1)  # Delay to avoid hitting the server too hard

    return crawl_history, pages_crawled

def extract_meta_tags(soup):
    meta_data = {}
    description_tag = soup.find('meta', {'name': 'description'})
    if description_tag:
        meta_data['description'] = description_tag.get('content', '')
    keywords_tag = soup.find('meta', {'name': 'keywords'})
    if keywords_tag:
        meta_data['keywords'] = keywords_tag.get('content', '')
    return meta_data
from datetime import datetime

@app.route('/crawl', methods=['GET', 'POST'])
@login_required
def crawl():
    print(f"Is the user logged in? {current_user.is_authenticated}")
    crawl_history = []  # Initialize as an empty list at the start
    status = 'success'
    pages_crawled = 0
    user_stats = None
    try:
        if current_user.is_authenticated:
            user_id = current_user.id

            # Fetch user statistics
            user_stats = {
                'total_crawls': get_total_crawls_for_user(user_id),
                'favorite_urls': get_favorite_urls_for_user(user_id),
                'recent_crawl': get_recent_crawl_for_user(user_id)
            }

        if request.method == 'POST':
            # Get form data for POST request (crawl submission)
            url = request.form['url']
            max_pages = int(request.form['max_pages'])
            max_depth = int(request.form['max_depth'])
            keyword = request.form['keyword']

            print(f"Received form data - URL: {url}, Max Pages: {max_pages}, Max Depth: {max_depth}, Keyword: {keyword}")

            # Perform the crawl and update the crawl_history
            crawl_history, pages_crawled = crawl_links(url, max_pages, max_depth, keyword)

            # Save the crawl history in the database
            conn = get_db_connection()
            conn.execute('INSERT INTO search_history (user_id, query) VALUES (?, ?)', (user_id, url))
            conn.commit()

            save_crawl_history(user_id, crawl_history, status, pages_crawled)

            # Return JSON response for AJAX request (for front-end update)
            return jsonify({
                'crawl_results': crawl_history,  # The crawl results (list of dicts)
                'pages_crawled': pages_crawled,
                'user_stats': user_stats
            })

        # If it's a GET request (initial page load), render the page with stats
        return render_template('crawl.html', user_stats=user_stats)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the crawl.'})



def get_total_crawls_for_user(user_id):
    # Open a connection to the database
    conn = get_db_connection()
    
    # Query to get the total number of crawls for the user
    cursor = conn.execute('SELECT COUNT(*) FROM crawl_history WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return the count of crawls
    return result[0] if result else 0

def get_favorite_urls_for_user(user_id):
    # Open a connection to the database
    conn = get_db_connection()
    
    # Query to get the favorite URLs for the user
    cursor = conn.execute('SELECT url FROM favorite_urls WHERE user_id = ?', (user_id,))
    result = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return the list of URLs
    return [row[0] for row in result] if result else []

def get_recent_crawl_for_user(user_id):
    # Open a connection to the database
    conn = get_db_connection()
    
    # Query to get the most recent crawl for the user
    cursor = conn.execute('SELECT url, crawl_time FROM crawl_history WHERE user_id = ? ORDER BY crawl_time DESC LIMIT 1', (user_id,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return the URL and crawl time if available
    if result:
        return f"URL: {result[0]}, Time: {result[1]}"
    else:
        return "No recent crawl"
    





@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = current_user.id  # Use Flask-Login's current_user to get the user_id
    
    conn = get_db_connection()

    # Fetch the user details
    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()

    # Fetching the search history for the user
    search_history = conn.execute('SELECT * FROM search_history WHERE user_id=? ORDER BY timestamp DESC', (user_id,)).fetchall()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profile_picture = request.files.get('profile_picture')

        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            # Save the profile picture in the defined UPLOAD_FOLDER
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_picture_path = filename
        else:
            # If no new picture, use the existing one
            profile_picture_path = user['profile_picture']

        if not username or not email:
            return "Invalid input", 400

        # Update the user details in the database
        conn.execute('UPDATE users SET username=?, email=?, profile_picture=? WHERE id=?',
                     (username, email, profile_picture_path, user_id))
        conn.commit()
        
        # After the update, redirect back to the profile page
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user, search_history=search_history)




@app.route('/history')
def history():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Fetch the crawl history for the logged-in user, including the `id`
    conn = get_db_connection()
    crawl_history = conn.execute(
        'SELECT id, title, url, date FROM crawl_history WHERE user_id=? ORDER BY date DESC',
        (current_user.id,)
    ).fetchall()
    conn.close()

    return render_template('history.html', crawl_history=crawl_history)

# Route to delete a specific entry from crawl history
@app.route('/delete_history/<int:entry_id>', methods=['POST'])
def delete_history(entry_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Delete the specified entry for the current user
    conn = get_db_connection()
    conn.execute('DELETE FROM crawl_history WHERE id=? AND user_id=?', (entry_id, current_user.id))
    conn.commit()
    conn.close()

    flash('Crawl entry deleted successfully.', 'success')
    return redirect(url_for('history'))

# Route to clear all crawl history for the logged-in user
@app.route('/clear_history', methods=['POST'])
def clear_history():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Delete all entries for the current user
    conn = get_db_connection()
    conn.execute('DELETE FROM crawl_history WHERE user_id=?', (current_user.id,))
    conn.commit()
    conn.close()

    flash('All crawl history cleared successfully.', 'success')
    return redirect(url_for('history'))

import csv
from io import StringIO
from flask import Response



@app.route('/download_history')
def download_history():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Fetch the crawl history for the logged-in user
    conn = get_db_connection()
    crawl_history = conn.execute(
        'SELECT title, url, crawl_time FROM crawl_history WHERE user_id=? ORDER BY crawl_time DESC',
        (current_user.id,)
    ).fetchall()
    conn.close()

    # Prepare the CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'URL', 'Date'])  # CSV Header

    # Add rows for each history entry
    for entry in crawl_history:
        # Handle the date format and ensure it's in a usable format
        if isinstance(entry['crawl_time'], datetime):  # if it's a datetime object
            formatted_date = entry['crawl_time'].strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
        elif isinstance(entry['crawl_time'], str):  # if it's a string
            # Try to parse the string into a datetime object
            try:
                formatted_date = datetime.strptime(entry['crawl_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = entry['crawl_time']  # If parsing fails, use the raw string
        else:
            formatted_date = 'Unknown Date'  # Fallback if date is not in expected format

        writer.writerow([entry['title'], entry['url'], formatted_date])

    output.seek(0)  # Rewind the StringIO object to the beginning
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=crawl_history.csv'
        }
    )



users_db = {
    'testuser': {
        'username': 'testuser',
        'password': 'pbkdf2:sha256:260000$u1V1L1fM$17be61e0d8d5f5827464e370670ad20d13db3ff38d9dff5e7b01d992e9c685a2'  # Example hashed password
    }
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])







from werkzeug.security import check_password_hash


import bcrypt

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming you're using Flask-WTF for form handling
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database for the user
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user_data:
            # Retrieve the stored password hash
            stored_password_hash = user_data['password']
            print(f"Stored password hash: {stored_password_hash}")
            print(f"Type of stored password hash: {type(stored_password_hash)}")

            # If the stored hash is bcrypt (it's in bytes now), use bcrypt's checkpw to validate
            if isinstance(stored_password_hash, bytes):
                # Compare the entered password with the stored bcrypt hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                    user = User(user_data['id'], user_data['username'], user_data['password'], user_data['email'], user_data['profile_picture'])
                    login_user(user)
                    flash('Login successful!', 'success')
                    return redirect(url_for('crawl'))
                else:
                    flash('Invalid username or password', 'error')
            else:
                # Assuming PBKDF2 or similar hash
                if check_password_hash(stored_password_hash, password):
                    user = User(user_data['id'], user_data['username'], user_data['password'], user_data['email'], user_data['profile_picture'])
                    login_user(user)
                    flash('Login successful!', 'success')
                    return redirect(url_for('crawl'))
                else:
                    flash('Invalid username or password', 'error')

        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


from flask_mail import Message

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Use raw SQL to query the database for the user by email
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user_data:
            # Generate a reset token
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Send the reset link via email
            msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[email])
            msg.body = f'Click the following link to reset your password: {reset_url}'
            try:
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'success')
            except Exception as e:
                flash(f'There was an error sending the email: {str(e)}', 'danger')
        else:
            flash('Email not found in our records.', 'danger')

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Debugging: print the token to see its value
        print(f"Received token: {token}")

        # Decode the email from the token
        email = s.loads(token, salt='password-reset-salt', max_age=3600).strip()  # Strip any spaces
        print(f"Decoded email from token: '{email}'")  # Debugging: print decoded email

    except SignatureExpired:
        flash('The reset link has expired. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))
    except Exception as e:
        flash(f'Invalid or expired token. Error: {str(e)}', 'danger')
        return redirect(url_for('forgot_password'))

    # Check the decoded email, it should match the email in the database
    print(f"Decoded email (after stripping spaces): '{email}'")

    # Use raw SQL to query the database for the user by email
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE email = ?', (email.strip(),)).fetchone()
    print(f"User data from DB: {user_data}")  # Debugging: Check the result from the database
    conn.close()

    if user_data:
        print(f"User found: {user_data[1]}, Email: {user_data[3]}")  # Debugging: Print user data
    else:
        print(f"User not found for email: '{email}'")

    # Proceed if the user was found
    if user_data and request.method == 'POST':
        new_password = request.form['password']

        # Use bcrypt for hashing if you're using bcrypt in your project
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # If the user is found, update the password
        conn = get_db_connection()
        result = conn.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
        conn.commit()
        conn.close()

        if result.rowcount > 0:
            flash('Your password has been successfully reset!', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful password reset
        else:
            flash('User not found. Please try again.', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('reset_password.html', token=token)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not username or not password or not email:
            flash("All fields are required!", 'error')
            return redirect(url_for('signup'))

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        if existing_user:
            flash("Username already taken", 'error')
            return redirect(url_for('signup'))
        
        conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashed, email))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Successfully logged out', 'success')
    return redirect(url_for('home'))
import requests
from bs4 import BeautifulSoup
import time
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crawl_links(start_url, max_pages, max_depth, keyword):
    visited = set()
    crawl_history = []
    to_visit = [(start_url, 0)]
    pages_crawled = 0

    while to_visit and len(crawl_history) < max_pages:
        url, depth = to_visit.pop(0)
        logger.info(f"Crawling {url} at depth {depth}")

        if url in visited or depth > max_depth:
            continue
        
        visited.add(url)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string if soup.title else 'No Title'
            logger.info(f"Found page title: {title}")

            if keyword.lower() in title.lower() or not keyword:
                crawl_history.append({'title': title, 'url': url})
                pages_crawled += 1
            logger.info(f"Current crawl history: {crawl_history}")

            for link in soup.find_all('a', href=True):
                full_url = requests.compat.urljoin(url, link['href'])
                if full_url not in visited and len(crawl_history) < max_pages:
                    to_visit.append((full_url, depth + 1))

            # Random sleep to avoid crawling too fast
            time.sleep(random.uniform(1, 3))  # Adding a randomized sleep to be more polite

        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {url}: {e}")
            continue
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            continue
    
    logger.info(f"Crawl completed. Total pages crawled: {pages_crawled}")
    logger.debug("Crawl history: %s", crawl_history)
    
    return crawl_history, pages_crawled

def save_crawl_history(user_id, crawl_history, status, pages_crawled):
    try:
        conn = get_db_connection()

        for link in crawl_history:
            title = link['title']
            url = link['url']
            date = datetime.now()

            conn.execute(''' 
                INSERT INTO crawl_history (user_id, title, url, date, status, pages_crawled) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, title, url, date, status, pages_crawled))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
