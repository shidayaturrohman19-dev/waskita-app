#!/usr/bin/env python3
"""
Script untuk membuat user admin otomatis di aplikasi Waskita
Mendukung environment-based configuration untuk development dan production
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from models import db, User, Dataset, RawData

def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    return app

def should_create_sample_data():
    """Cek apakah harus membuat sample data berdasarkan environment"""
    flask_env = os.getenv('FLASK_ENV', 'production')
    create_sample = os.getenv('CREATE_SAMPLE_DATA', 'false').lower() == 'true'
    
    return flask_env == 'development' or create_sample

def create_sample_datasets():
    """Membuat sample datasets untuk development/testing"""
    if not should_create_sample_data():
        return []
    
    print("\n3. Membuat Sample Datasets untuk Development...")
    
    sample_datasets = [
        {
            'name': 'Sample Twitter Data',
            'description': 'Dataset contoh dari Twitter untuk testing klasifikasi',
            'source': 'twitter',
            'total_data': 50
        },
        {
            'name': 'Sample Facebook Data', 
            'description': 'Dataset contoh dari Facebook untuk testing',
            'source': 'facebook',
            'total_data': 30
        },
        {
            'name': 'Sample Instagram Data',
            'description': 'Dataset contoh dari Instagram untuk testing',
            'source': 'instagram', 
            'total_data': 25
        }
    ]
    
    created_datasets = []
    
    try:
        for dataset_info in sample_datasets:
            # Cek apakah dataset sudah ada
            existing = Dataset.query.filter_by(name=dataset_info['name']).first()
            if existing:
                print(f"  ✓ Dataset '{dataset_info['name']}' sudah ada")
                created_datasets.append(existing)
                continue
            
            # Buat dataset baru
            dataset = Dataset(
                name=dataset_info['name'],
                description=dataset_info['description'],
                source=dataset_info['source'],
                total_data=dataset_info['total_data'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(dataset)
            db.session.flush()  # Untuk mendapatkan ID
            
            # Buat sample raw data
            create_sample_raw_data(dataset.id, dataset_info['total_data'], dataset_info['source'])
            
            created_datasets.append(dataset)
            print(f"  ✓ Dataset '{dataset_info['name']}' berhasil dibuat dengan {dataset_info['total_data']} data")
        
        db.session.commit()
        print(f"✓ {len(created_datasets)} sample datasets berhasil dibuat!")
        return created_datasets
        
    except Exception as e:
        print(f"✗ Error membuat sample datasets: {str(e)}")
        db.session.rollback()
        return []

def create_sample_raw_data(dataset_id, count, source):
    """Membuat sample raw data untuk dataset"""
    from utils import generate_sample_data
    
    sample_data = generate_sample_data(count, source)
    
    for data in sample_data:
        raw_data = RawData(
            dataset_id=dataset_id,
            content=data['content'],
            username=data['username'],
            timestamp=data['timestamp'],
            platform=source,
            engagement_count=data.get('engagement_count', 0),
            created_at=datetime.utcnow()
        )
        db.session.add(raw_data)

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
    
    # Create Flask app and application context
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        flask_env = os.getenv('FLASK_ENV', 'production')
        create_sample = should_create_sample_data()
        
        print(f"Environment: {flask_env}")
        print(f"Create Sample Data: {'Ya' if create_sample else 'Tidak'}")
        
        # Buat admin user
        print("\n1. Membuat User Admin...")
        admin = create_admin_user()
        
        # Buat test user
        print("\n2. Membuat User Test...")
        test_user = create_test_user()
        
        # Buat sample datasets jika dalam mode development
        sample_datasets = []
        if create_sample:
            sample_datasets = create_sample_datasets()
        
        print("\n" + "=" * 50)
        if admin and test_user:
            print("✓ Setup berhasil! Anda dapat login dengan:")
            print("\nAdmin:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\nTest User:")
            print("  Username: testuser")
            print("  Password: testuser123")
            
            if sample_datasets:
                print(f"\n✓ {len(sample_datasets)} sample datasets telah dibuat untuk development")
                total_sample_data = sum(ds.total_data for ds in sample_datasets)
                print(f"  Total sample data: {total_sample_data} records")
        else:
            print("✗ Setup gagal! Periksa error di atas.")
        print("=" * 50)

if __name__ == '__main__':
    main()