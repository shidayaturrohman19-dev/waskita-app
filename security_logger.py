import logging
import os
from datetime import datetime
from flask import request
from flask_login import current_user
from functools import wraps

# Setup security logger
security_logger = logging.getLogger('security')
security_handler = logging.FileHandler('security.log')
security_formatter = logging.Formatter(
    '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
)
security_handler.setFormatter(security_formatter)
security_logger.addHandler(security_handler)
security_logger.setLevel(logging.INFO)

def log_security_event(event_type, details=None, user_id=None, ip_address=None):
    """
    Log security-related events
    
    Args:
        event_type (str): Type of security event
        details (str): Additional details about the event
        user_id (int): User ID if applicable
        ip_address (str): IP address of the request
    """
    if not ip_address:
        ip_address = request.remote_addr if request else 'Unknown'
    
    if not user_id and current_user and hasattr(current_user, 'id'):
        user_id = current_user.id
    
    log_message = f"Event: {event_type} | IP: {ip_address}"
    
    if user_id:
        log_message += f" | User ID: {user_id}"
    
    if details:
        log_message += f" | Details: {details}"
    
    security_logger.info(log_message)

def log_failed_login(username, ip_address=None):
    """Log failed login attempts"""
    log_security_event(
        'FAILED_LOGIN',
        f'Username: {username}',
        ip_address=ip_address
    )

def log_registration_attempt(username, email, ip_address=None):
    """Log registration attempts"""
    log_security_event(
        'REGISTRATION_ATTEMPT',
        f'Username: {username}, Email: {email}',
        ip_address=ip_address
    )

def log_admin_action(action, details=None, user_id=None, ip_address=None):
    """Log admin actions"""
    log_security_event(
        f'ADMIN_ACTION_{action}',
        details,
        user_id=user_id,
        ip_address=ip_address
    )

def log_rate_limit_exceeded(endpoint, ip_address=None):
    """Log rate limit violations"""
    log_security_event(
        'RATE_LIMIT_EXCEEDED',
        f'Endpoint: {endpoint}',
        ip_address=ip_address
    )

def security_monitor(event_type):
    """
    Decorator to monitor security events
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                log_security_event(f'{event_type}_SUCCESS')
                return result
            except Exception as e:
                log_security_event(f'{event_type}_ERROR', str(e))
                raise
        return decorated_function
    return decorator