import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OTPConfig:
    """Configuration class for OTP authentication system"""
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    
    # Admin Configuration
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@waskita.com')
    ADMIN_EMAILS = [
        email.strip() 
        for email in os.environ.get('ADMIN_EMAILS', ADMIN_EMAIL).split(',')
        if email.strip()
    ]
    
    # OTP Configuration
    OTP_LENGTH = int(os.environ.get('OTP_LENGTH', 6))
    OTP_EXPIRY_MINUTES = int(os.environ.get('OTP_EXPIRY_MINUTES', 30))
    OTP_EXPIRY_DELTA = timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    # Registration Configuration
    REGISTRATION_ENABLED = os.environ.get('REGISTRATION_ENABLED', 'True').lower() == 'true'
    AUTO_APPROVE_REGISTRATION = os.environ.get('AUTO_APPROVE_REGISTRATION', 'False').lower() == 'true'
    
    # Security Configuration
    MAX_OTP_ATTEMPTS = int(os.environ.get('MAX_OTP_ATTEMPTS', 3))
    LOCKOUT_DURATION_MINUTES = int(os.environ.get('LOCKOUT_DURATION_MINUTES', 15))
    
    # Email Templates Configuration
    EMAIL_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates', 'email')
    
    # Application URLs
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    REGISTRATION_STATUS_URL = f"{BASE_URL}/otp/registration-status"
    ADMIN_PANEL_URL = f"{BASE_URL}/otp/admin/pending"
    
    # Notification Settings
    SEND_EMAIL_NOTIFICATIONS = os.environ.get('SEND_EMAIL_NOTIFICATIONS', 'True').lower() == 'true'
    EMAIL_RETRY_ATTEMPTS = int(os.environ.get('EMAIL_RETRY_ATTEMPTS', 3))
    EMAIL_RETRY_DELAY_SECONDS = int(os.environ.get('EMAIL_RETRY_DELAY_SECONDS', 5))
    
    # Database Configuration
    CLEANUP_EXPIRED_REQUESTS_HOURS = int(os.environ.get('CLEANUP_EXPIRED_REQUESTS_HOURS', 24))
    KEEP_COMPLETED_REQUESTS_DAYS = int(os.environ.get('KEEP_COMPLETED_REQUESTS_DAYS', 7))
    
    @classmethod
    def validate_config(cls):
        """Validate OTP configuration"""
        errors = []
        
        if not cls.MAIL_USERNAME:
            errors.append("MAIL_USERNAME is required for email functionality")
        
        if not cls.MAIL_PASSWORD:
            errors.append("MAIL_PASSWORD is required for email functionality")
        
        if not cls.ADMIN_EMAILS:
            errors.append("At least one ADMIN_EMAIL is required")
        
        if cls.OTP_LENGTH < 4 or cls.OTP_LENGTH > 8:
            errors.append("OTP_LENGTH must be between 4 and 8")
        
        if cls.OTP_EXPIRY_MINUTES < 5 or cls.OTP_EXPIRY_MINUTES > 120:
            errors.append("OTP_EXPIRY_MINUTES must be between 5 and 120")
        
        return errors
    
    @classmethod
    def get_email_config(cls):
        """Get email configuration dictionary"""
        return {
            'MAIL_SERVER': cls.MAIL_SERVER,
            'MAIL_PORT': cls.MAIL_PORT,
            'MAIL_USE_TLS': cls.MAIL_USE_TLS,
            'MAIL_USE_SSL': cls.MAIL_USE_SSL,
            'MAIL_USERNAME': cls.MAIL_USERNAME,
            'MAIL_PASSWORD': cls.MAIL_PASSWORD,
            'MAIL_DEFAULT_SENDER': cls.MAIL_DEFAULT_SENDER,
        }
    
    @classmethod
    def is_admin_email(cls, email):
        """Check if email is an admin email"""
        return email.lower() in [admin_email.lower() for admin_email in cls.ADMIN_EMAILS]
    
    @classmethod
    def get_primary_admin_email(cls):
        """Get the primary admin email"""
        return cls.ADMIN_EMAILS[0] if cls.ADMIN_EMAILS else cls.ADMIN_EMAIL