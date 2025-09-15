import os
import logging
import locale
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('waskita.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Load configuration from config.py
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Set Indonesian locale as default
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Indonesian_Indonesia.1252')
    except locale.Error:
        logger.warning('Could not set Indonesian locale, using default')
        pass

# Use PostgreSQL as the primary database
print(f"Using PostgreSQL database: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize extensions
from models import db
from flask_migrate import Migrate
from scheduler import cleanup_scheduler

db.init_app(app)
migrate = Migrate(app, db)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize scheduler
cleanup_scheduler.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()

# Initialize model variables
word2vec_model = None
naive_bayes_models = {}

# Function to load models within app context
def load_models():
    global word2vec_model, naive_bayes_models
    with app.app_context():
        print("Loading AI models...")
        try:
            from utils import load_word2vec_model, load_naive_bayes_models
            word2vec_model = load_word2vec_model()
            naive_bayes_models = load_naive_bayes_models()
            print("AI models loaded successfully")
        except Exception as e:
            print(f"Error loading AI models: {e}")
            # Set empty models if loading fails
            word2vec_model = None
            naive_bayes_models = {}

# Models already imported above

# Register template filters with error handling
try:
    from utils import format_datetime
    app.jinja_env.filters['format_datetime'] = format_datetime
    logger.info("Template filter 'format_datetime' registered successfully")
except ImportError as e:
    logger.error(f"Failed to import format_datetime: {e}")
    # Fallback filter
    def fallback_format_datetime(dt, format_type='default'):
        try:
            if not dt:
                return '-'
            return str(dt)
        except:
            return '-'
    app.jinja_env.filters['format_datetime'] = fallback_format_datetime
    logger.info("Fallback format_datetime filter registered")
except Exception as e:
    logger.error(f"Error registering format_datetime filter: {e}")

# Add global error handler for template rendering
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"Page not found: {request.url}")
    return render_template('errors/404.html'), 404

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    load_models()
    # Initialize routes with loaded models
    from routes import init_routes
    init_routes(app, word2vec_model, naive_bayes_models)
    
    # Start automatic cleanup scheduler
    cleanup_scheduler.start_scheduler()
    logger.info("Automatic data cleanup scheduler started")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        logger.info("Shutting down application...")
        cleanup_scheduler.stop_scheduler()
        logger.info("Cleanup scheduler stopped")