#!/usr/bin/env python3
"""
Script untuk membuat user admin otomatis di aplikasi Waskita
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from models import db, User

def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    return app

def create_admin_user():
    """Membuat user admin dengan kredensial default"""
    
    # Konfigurasi admin default
    admin_config = {
        'username': 'admin',
        'email': 'admin@waskita.com',
        'password': 'admin123',
        'full_name': 'Administrator Waskita',
        'role': 'admin'
    }
    
    app = create_app()
    
    with app.app_context():
        try:
            # Cek apakah admin sudah ada
            existing_admin = User.query.filter_by(username=admin_config['username']).first()
            if existing_admin:
                print(f"✓ User admin '{admin_config['username']}' sudah ada!")
                print(f"  Email: {existing_admin.email}")
                print(f"  Role: {existing_admin.role}")
                return existing_admin
            
            # Buat user admin baru
            admin_user = User(
                username=admin_config['username'],
                email=admin_config['email'],
                full_name=admin_config['full_name'],
                role=admin_config['role'],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Set password
            admin_user.set_password(admin_config['password'])
            
            # Set preferences default untuk admin
            admin_preferences = {
                'language': 'id',
                'timezone': 'Asia/Jakarta',
                'items_per_page': 50,
                'email_notifications': True,
                'auto_refresh': True,
                'dark_mode': True,  # Default dark mode sesuai user rules
                'compact_view': False
            }
            admin_user.preferences = admin_preferences
            
            # Simpan ke database
            db.session.add(admin_user)
            db.session.commit()
            
            print("✓ User admin berhasil dibuat!")
            print(f"  Username: {admin_config['username']}")
            print(f"  Email: {admin_config['email']}")
            print(f"  Password: {admin_config['password']}")
            print(f"  Role: {admin_config['role']}")
            print(f"  ID: {admin_user.id}")
            
            return admin_user
            
        except Exception as e:
            print(f"✗ Error membuat user admin: {str(e)}")
            db.session.rollback()
            return None

def create_test_user():
    """Membuat user biasa untuk testing"""
    
    user_config = {
        'username': 'testuser',
        'email': 'test@waskita.com',
        'password': 'test123',
        'full_name': 'Test User',
        'role': 'user'
    }
    
    app = create_app()
    
    with app.app_context():
        try:
            # Cek apakah user test sudah ada
            existing_user = User.query.filter_by(username=user_config['username']).first()
            if existing_user:
                print(f"✓ User test '{user_config['username']}' sudah ada!")
                return existing_user
            
            # Buat user test baru
            test_user = User(
                username=user_config['username'],
                email=user_config['email'],
                full_name=user_config['full_name'],
                role=user_config['role'],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Set password
            test_user.set_password(user_config['password'])
            
            # Set preferences default
            test_preferences = {
                'language': 'id',
                'timezone': 'Asia/Jakarta',
                'items_per_page': 25,
                'email_notifications': True,
                'auto_refresh': False,
                'dark_mode': True,  # Default dark mode sesuai user rules
                'compact_view': False
            }
            test_user.preferences = test_preferences
            
            # Simpan ke database
            db.session.add(test_user)
            db.session.commit()
            
            print("✓ User test berhasil dibuat!")
            print(f"  Username: {user_config['username']}")
            print(f"  Email: {user_config['email']}")
            print(f"  Password: {user_config['password']}")
            print(f"  Role: {user_config['role']}")
            print(f"  ID: {test_user.id}")
            
            return test_user
            
        except Exception as e:
            print(f"✗ Error membuat user test: {str(e)}")
            db.session.rollback()
            return None

def main():
    """Main function"""
    print("=" * 50)
    print("WASKITA - Setup User Admin & Test")
    print("=" * 50)
    
    # Buat admin user
    print("\n1. Membuat User Admin...")
    admin = create_admin_user()
    
    # Buat test user
    print("\n2. Membuat User Test...")
    test_user = create_test_user()
    
    print("\n" + "=" * 50)
    if admin and test_user:
        print("✓ Setup berhasil! Anda dapat login dengan:")
        print("\nAdmin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nTest User:")
        print("  Username: testuser")
        print("  Password: test123")
    else:
        print("✗ Setup gagal! Periksa error di atas.")
    print("=" * 50)

if __name__ == '__main__':
    main()