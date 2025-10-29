# SECURITY UTILITIES FOR WASKITA APPLICATION
# Modul keamanan untuk validasi file dan sanitasi input

import bleach
import logging
import os
import uuid
import re
import mimetypes
from functools import wraps
from flask import request, abort, current_app
from werkzeug.utils import secure_filename

# Setup security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# File handler untuk security logs
if not security_logger.handlers:
    handler = logging.FileHandler('logs/security.log')
    formatter = logging.Formatter(
        '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    security_logger.addHandler(handler)

class SecurityValidator:
    """Class untuk validasi keamanan yang komprehensif"""
    
    @staticmethod
    def validate_file_upload(file):
        """
        Validasi file upload yang aman dengan MIME type checking
        Returns: (is_valid: bool, message: str, file_info: dict)
        """
        if not file or not file.filename:
            return False, "Tidak ada file yang dipilih", {}
        
        filename = file.filename
        file_info = {
            'original_filename': filename,
            'secure_filename': secure_filename(filename),
            'file_size': 0,
            'mime_type': None
        }
        
        # 1. Validasi ekstensi file
        allowed_extensions = {'csv', 'xlsx', 'xls'}
        if not ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            security_logger.warning(f"Invalid file extension attempted: {filename}")
            return False, "Format file tidak didukung. Hanya CSV, XLSX, dan XLS yang diizinkan.", file_info
        
        # 2. Validasi ukuran file
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        file_info['file_size'] = file_size
        
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16MB default
        if file_size > max_size:
            security_logger.warning(f"File too large attempted: {filename} ({file_size} bytes)")
            return False, f"Ukuran file terlalu besar (maksimal {max_size // (1024*1024)}MB)", file_info
        
        if file_size == 0:
            return False, "File kosong tidak diizinkan", file_info
        
        # 3. Validasi MIME type
        try:
            # Use mimetypes to get MIME type
            mime_type, _ = mimetypes.guess_type(filename)
            file_info['mime_type'] = mime_type
            
            # Allowed MIME types untuk CSV dan Excel
            allowed_mimes = {
                'text/csv', 
                'text/plain',  # CSV bisa terdeteksi sebagai text/plain
                'application/csv',
                'application/vnd.ms-excel',  # .xls
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # .xlsx
            }
            
            if mime_type and mime_type not in allowed_mimes:
                security_logger.warning(f"Invalid MIME type attempted: {filename} ({mime_type})")
                return False, f"Tipe file tidak valid. Terdeteksi: {mime_type}", file_info
                
        except Exception as e:
            security_logger.error(f"Error validating file MIME type: {filename} - {str(e)}")
            return False, f"Error validasi file: {str(e)}", file_info
        
        # 4. Validasi nama file (mencegah path traversal)
        if '..' in filename or '/' in filename or '\\' in filename:
            security_logger.warning(f"Path traversal attempt: {filename}")
            return False, "Nama file tidak valid", file_info
        
        security_logger.info(f"File upload validated successfully: {filename} ({mime_type}, {file_size} bytes)")
        return True, "File valid", file_info
    
    @staticmethod
    def sanitize_input(text, max_length=None, allow_html=False):
        """
        Sanitasi input untuk mencegah XSS dan injection
        """
        if not text:
            return ""
        
        # Remove null bytes dan karakter kontrol
        text = text.replace('\x00', '').replace('\r', '').strip()
        
        if not allow_html:
            # Sanitize HTML tags
            text = bleach.clean(text, tags=[], attributes={}, strip=True)
        else:
            # Allow only safe HTML tags
            allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
            text = bleach.clean(text, tags=allowed_tags, attributes={}, strip=True)
        
        # Limit length
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    @staticmethod
    def validate_username(username):
        """Validasi username"""
        if not username:
            return False, "Username tidak boleh kosong"
        
        username = SecurityValidator.sanitize_input(username, max_length=50)
        
        if len(username) < 3:
            return False, "Username minimal 3 karakter"
        
        if len(username) > 50:
            return False, "Username maksimal 50 karakter"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username hanya boleh huruf, angka, dan underscore"
        
        return True, username
    
    @staticmethod
    def validate_email(email):
        """Validasi email"""
        if not email:
            return False, "Email tidak boleh kosong"
        
        email = SecurityValidator.sanitize_input(email, max_length=254)
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Format email tidak valid"
        
        if len(email) > 254:
            return False, "Email terlalu panjang"
        
        return True, email
    
    @staticmethod
    def validate_password(password):
        """Validasi password yang kuat"""
        if not password:
            return False, "Password tidak boleh kosong"
        
        if len(password) < 8:
            return False, "Password minimal 8 karakter"
        
        if len(password) > 128:
            return False, "Password maksimal 128 karakter"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password harus mengandung huruf besar"
        
        if not re.search(r'[a-z]', password):
            return False, "Password harus mengandung huruf kecil"
        
        if not re.search(r'\d', password):
            return False, "Password harus mengandung angka"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password harus mengandung karakter khusus"
        
        return True, "Password valid"

def generate_secure_filename(original_filename, upload_folder):
    """
    Generate secure file path untuk upload dengan UUID prefix
    """
    # Sanitize filename
    filename = secure_filename(original_filename)
    
    if not filename:
        filename = "upload_file"
    
    # Add UUID prefix untuk mencegah collision dan predictable filenames
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Pastikan path tidak keluar dari upload folder
    filepath = os.path.join(upload_folder, unique_filename)
    filepath = os.path.abspath(filepath)
    
    if not filepath.startswith(os.path.abspath(upload_folder)):
        raise ValueError("Invalid file path - path traversal detected")
    
    return filepath, unique_filename

def log_security_event(event_type, message, user_id=None, ip_address=None):
    """
    Log security events untuk monitoring
    """
    log_message = f"{event_type}: {message}"
    if user_id:
        log_message += f" | User: {user_id}"
    if ip_address:
        log_message += f" | IP: {ip_address}"
    
    security_logger.info(log_message)

def rate_limit_by_user(max_requests=10, window=3600):
    """
    Rate limiting decorator per user untuk endpoint sensitif
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implementasi rate limiting bisa ditambahkan di sini
            # Untuk saat ini, kita log saja
            if hasattr(request, 'user') and request.user:
                log_security_event(
                    "RATE_LIMIT_CHECK", 
                    f"Access to {f.__name__}", 
                    user_id=request.user.id,
                    ip_address=request.remote_addr
                )
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Security headers yang akan ditambahkan ke response
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.datatables.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.datatables.net; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data:; connect-src 'self' https://cdn.jsdelivr.net",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
}

def add_security_headers(response):
    """
    Tambahkan security headers ke response
    """
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response