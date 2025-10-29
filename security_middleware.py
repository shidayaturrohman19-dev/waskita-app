"""
Security Middleware untuk aplikasi Flask
Menambahkan security headers dan proteksi keamanan lainnya
"""

from flask import request, abort, g, current_app
from functools import wraps
import time
from collections import defaultdict, deque
import re
from security_logger import log_security_event, check_ip_blocked, log_rate_limit_exceeded
from security_utils import add_security_headers

# Rate limiting storage (in production, use Redis)
rate_limit_storage = defaultdict(list)

class SecurityMiddleware:
    """Middleware untuk menangani security headers dan proteksi"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Security checks before processing request"""
        # Log request details for debugging
        current_app.logger.info(f"Request: {request.method} {request.path} - Content-Type: {request.content_type}")
        
        # Check if IP is blocked
        if check_ip_blocked():
            abort(403)
        
        # Rate limiting
        if self.is_rate_limited():
            log_rate_limit_exceeded(request.endpoint or request.path)
            abort(429)
        
        # Check for suspicious patterns
        if self.check_suspicious_requests():
            log_security_event(
                'SUSPICIOUS_REQUEST',
                f'Suspicious pattern detected in request to {request.path}',
                severity='WARNING'
            )
            abort(400)
        
        # Store request start time for performance monitoring
        g.start_time = time.time()
    
    def after_request(self, response):
        """Process response after handling"""
        # Add security headers
        response = add_security_headers(response)
        
        # Log slow requests
        if hasattr(g, 'start_time'):
            request_time = time.time() - g.start_time
            if request_time > 5.0:  # Log requests taking more than 5 seconds
                log_security_event(
                    "SLOW_REQUEST",
                    f"Slow request detected: {request.endpoint} took {request_time:.2f}s",
                    ip_address=request.remote_addr
                )
        
        return response
    
    def is_rate_limited(self):
        """Check if request should be rate limited"""
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old entries (older than 1 minute)
        rate_limit_storage[client_ip] = [
            timestamp for timestamp in rate_limit_storage[client_ip]
            if current_time - timestamp < 60
        ]
        
        # Check if rate limit exceeded (max 100 requests per minute)
        if len(rate_limit_storage[client_ip]) >= 100:
            return True
        
        # Add current request timestamp
        rate_limit_storage[client_ip].append(current_time)
        return False
    
    def check_suspicious_requests(self):
        """Check for suspicious request patterns"""
        # Check for SQL injection patterns
        suspicious_patterns = [
            'union select', 'drop table', 'insert into', 'delete from',
            'script>', '<iframe', 'javascript:', 'vbscript:',
            '../', '..\\', '/etc/passwd', '/proc/version'
        ]
        
        # Check URL and form data
        request_data = str(request.url).lower()
        if request.form:
            request_data += ' ' + ' '.join(request.form.values()).lower()
        # Only check JSON if content-type is application/json
        if request.content_type and 'application/json' in request.content_type:
            try:
                json_data = request.get_json(silent=True)
                if json_data:
                    request_data += ' ' + str(json_data).lower()
            except Exception:
                pass  # Ignore JSON parsing errors
        
        for pattern in suspicious_patterns:
            if pattern in request_data:
                log_security_event(
                    "SUSPICIOUS_REQUEST",
                    f"Suspicious pattern detected: {pattern} in request from {request.remote_addr}",
                    ip_address=request.remote_addr
                )
                return True
        
        return False

def rate_limit(max_requests=60, window=60):
    """
    Decorator untuk rate limiting pada endpoint tertentu
    
    Args:
        max_requests: Maximum number of requests allowed
        window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Create unique key for this endpoint
            endpoint_key = f"{client_ip}:{request.endpoint}"
            
            # Clean old entries
            rate_limit_storage[endpoint_key] = [
                timestamp for timestamp in rate_limit_storage[endpoint_key]
                if current_time - timestamp < window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[endpoint_key]) >= max_requests:
                log_security_event(
                    "ENDPOINT_RATE_LIMIT",
                    f"Rate limit exceeded for endpoint {request.endpoint} from {client_ip}",
                    ip_address=client_ip
                )
                from flask import jsonify
                return jsonify({
                    'success': False, 
                    'message': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            # Add current request
            rate_limit_storage[endpoint_key].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_https():
    """Decorator to require HTTPS for sensitive endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_secure and not request.headers.get('X-Forwarded-Proto') == 'https':
                log_security_event(
                    "INSECURE_REQUEST",
                    f"HTTP request to secure endpoint: {request.endpoint}",
                    ip_address=request.remote_addr
                )
                from flask import redirect, url_for
                return redirect(url_for(request.endpoint, _external=True, _scheme='https'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator