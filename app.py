import os
import logging
import locale
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
from dotenv import load_dotenv
from flask_talisman import Talisman

# Load environment variables from .env file
load_dotenv(override=True)  # Use override=True to ensure .env values take precedence

# Routes will be initialized using init_routes function
from models import db, User
from models_otp import RegistrationRequest, AdminNotification, OTPEmailLog
from otp_routes import otp_bp
from config import Config

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
app.config.from_object(Config)

# Configure JSON to handle Unicode properly
app.json.ensure_ascii = False
app.json.sort_keys = False

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
pass

# Initialize extensions
from models import db
from flask_migrate import Migrate
from scheduler import cleanup_scheduler
from security_middleware import SecurityMiddleware

db.init_app(app)
migrate = Migrate(app, db)

# Initialize security middleware
security_middleware = SecurityMiddleware(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Talisman for SSL security
if app.config.get('SSL_ENABLED', False):
    # Configure Talisman with settings from environment variables
    talisman = Talisman(
        app,
        force_https=True,
        strict_transport_security=app.config.get('HSTS_ENABLED', True),
        strict_transport_security_max_age=app.config.get('HSTS_SECONDS', 31536000),
        strict_transport_security_include_subdomains=app.config.get('HSTS_INCLUDE_SUBDOMAINS', True),
        strict_transport_security_preload=app.config.get('HSTS_PRELOAD', False),
        content_security_policy={
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'code.jquery.com'],
            'style-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'fonts.googleapis.com'],
            'font-src': ["'self'", 'fonts.gstatic.com'],
            'img-src': ["'self'", 'data:'],
        },
        content_security_policy_nonce_in=['script-src', 'style-src'],
        feature_policy={
            'geolocation': "'none'",
            'camera': "'none'",
            'microphone': "'none'"
        }
    )
else:
    # In development mode, initialize Talisman but disable most security features
    talisman = Talisman(
        app,
        force_https=False,
        content_security_policy=None,
    )

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["500 per day", "200 per hour"],
    storage_uri="memory://"
)

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
    """Load Word2Vec dan Naive Bayes models"""
    global word2vec_model, naive_bayes_models
    with app.app_context():
        try:
            from utils import load_word2vec_model, load_naive_bayes_models
            
            # Load Word2Vec model
            word2vec_model = load_word2vec_model()
            if word2vec_model is None:
                app.logger.error("Failed to load Word2Vec model")
            else:
                app.logger.info("Word2Vec model loaded successfully")
            
            # Load Naive Bayes models
            naive_bayes_models = load_naive_bayes_models()
            if not naive_bayes_models:
                app.logger.error("Failed to load Naive Bayes models")
            else:
                app.logger.info(f"Loaded {len(naive_bayes_models)} Naive Bayes models")
                
            # Set models in app config for global access
            app.config['WORD2VEC_MODEL'] = word2vec_model
            app.config['NAIVE_BAYES_MODELS'] = naive_bayes_models
            
        except Exception as e:
            app.logger.error(f"Error loading models: {str(e)}")
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

@app.errorhandler(415)
def unsupported_media_type(error):
    logger.error(f"Unsupported Media Type error: {error}")
    return render_template('errors/404.html'), 415

@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"Page not found: {error}")
    return render_template('errors/404.html'), 404

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Load models and initialize routes
load_models()
from routes import init_routes
init_routes(app, word2vec_model, naive_bayes_models)

# Register OTP blueprint
app.register_blueprint(otp_bp, url_prefix='/otp')

logger.info("OTP authentication blueprint registered with rate limiting")

if __name__ == '__main__':
    
    # Start automatic cleanup scheduler
    cleanup_scheduler.start_scheduler()
    logger.info("Automatic data cleanup scheduler started")
    
    try:
        # Use debug mode from environment variable
        debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
        
        # Baca konfigurasi SSL dari .env
        # Reload .env untuk memastikan nilai terbaru terbaca
        from dotenv import load_dotenv, dotenv_values
        
        # Muat ulang .env dengan override
        load_dotenv(override=True)
        
        # Baca langsung dari file .env sebagai backup
        env_values = dotenv_values('.env')
        
        # Baca nilai SSL_ENABLED dengan fallback ke file langsung
        ssl_enabled_value = os.environ.get('SSL_ENABLED') or env_values.get('SSL_ENABLED', 'False')
        ssl_mode_value = os.environ.get('SSL_MODE') or env_values.get('SSL_MODE', 'adhoc')
        
        logger.info(f"SSL_ENABLED value from environment: {os.environ.get('SSL_ENABLED')}")
        logger.info(f"SSL_ENABLED value from .env file: {env_values.get('SSL_ENABLED')}")
        logger.info(f"Final SSL_ENABLED value: {ssl_enabled_value}")
        
        # Konversi string ke boolean
        ssl_enabled = ssl_enabled_value.lower() in ('true', '1', 't', 'yes') if ssl_enabled_value else False
        ssl_mode = ssl_mode_value
        
        # Log konfigurasi SSL
        logger.info(f"SSL Configuration - Enabled: {ssl_enabled}, Mode: {ssl_mode}")
        
        # Konfigurasi SSL berdasarkan mode yang dipilih
        ssl_context = None
        
        if ssl_enabled:
            if ssl_mode == 'adhoc':
                try:
                    import ssl
                    from OpenSSL import SSL
                    ssl_context = 'adhoc'
                    logger.info("Starting server with adhoc SSL certificate")
                except ImportError:
                    logger.warning("pyOpenSSL not installed. Installing it now...")
                    import subprocess
                    subprocess.check_call(['pip', 'install', 'pyopenssl'])
                    ssl_context = 'adhoc'
                    logger.info("pyOpenSSL installed. Starting server with adhoc SSL certificate")
            
            elif ssl_mode == 'self-signed' or ssl_mode == 'custom':
                cert_path = os.environ.get('SSL_CERT_PATH', '')
                key_path = os.environ.get('SSL_KEY_PATH', '')
                
                if os.path.exists(cert_path) and os.path.exists(key_path):
                    ssl_context = (cert_path, key_path)
                    logger.info(f"Starting server with {ssl_mode} SSL certificate")
                else:
                    logger.warning(f"SSL certificate files not found at {cert_path} and {key_path}. Falling back to HTTP.")
                    ssl_context = None
            
            elif ssl_mode == 'letsencrypt':
                domain = os.environ.get('LETSENCRYPT_DOMAIN', '')
                cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
                key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"
                
                if os.path.exists(cert_path) and os.path.exists(key_path):
                    ssl_context = (cert_path, key_path)
                    logger.info("Starting server with Let's Encrypt SSL certificate")
                else:
                    logger.warning(f"Let's Encrypt certificate files not found for domain {domain}. Falling back to HTTP.")
                    ssl_context = None
            
            else:  # ssl_mode == 'disabled' or any other value
                ssl_context = None
                logger.info("SSL mode not recognized or disabled. Starting server without SSL")
        else:
            logger.info("SSL disabled in configuration. Starting server without SSL")
        
        # Run the app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=debug_mode,
            ssl_context=ssl_context
        )
    except KeyboardInterrupt:
        logger.info("Shutting down application...")
        cleanup_scheduler.stop_scheduler()
        logger.info("Cleanup scheduler stopped")