#!/usr/bin/env python3
"""
Waskita Database Setup Script
Script untuk setup database PostgreSQL dan membuat user admin default
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash
import getpass

def create_database_and_user():
    """Membuat database dan user PostgreSQL"""
    print("🔧 Setup Database PostgreSQL untuk Waskita")
    print("=" * 50)
    
    # Input konfigurasi database
    print("\n📋 Konfigurasi Database:")
    db_host = input("Host PostgreSQL (default: [host]): ").strip() or "[host]"
    db_port = input("Port PostgreSQL (default: [port]): ").strip() or "[port]"
    
    # Kredensial admin PostgreSQL
    print("\n🔐 Kredensial Admin PostgreSQL:")
    admin_user = input("Username admin PostgreSQL (default: [admin_user]): ").strip() or "[admin_user]"
    admin_password = getpass.getpass("Password admin PostgreSQL: ")
    
    # Kredensial database Waskita
    print("\n🏗️ Konfigurasi Database Waskita:")
    db_name = input("Nama database (default: [database_name]): ").strip() or "[database_name]"
    db_test_name = input("Nama database test (default: [test_database_name]): ").strip() or "[test_database_name]"
    db_user = input("Username database (default: [db_username]): ").strip() or "[db_username]"
    db_password = getpass.getpass("Password database (default: [db_password]): ") or "[db_password]"
    
    try:
        # Koneksi ke PostgreSQL sebagai admin
        print(f"\n🔌 Menghubungkan ke PostgreSQL di {db_host}:{db_port}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=admin_user,
            password=admin_password,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Buat user database jika belum ada
        print(f"👤 Membuat user database '{db_user}'...")
        try:
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
            print(f"✅ User '{db_user}' berhasil dibuat")
        except psycopg2.errors.DuplicateObject:
            print(f"ℹ️ User '{db_user}' sudah ada")
        
        # Buat database development
        print(f"🗄️ Membuat database '{db_name}'...")
        try:
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            print(f"✅ Database '{db_name}' berhasil dibuat")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ℹ️ Database '{db_name}' sudah ada")
        
        # Buat database test
        print(f"🧪 Membuat database test '{db_test_name}'...")
        try:
            cursor.execute(f"CREATE DATABASE {db_test_name} OWNER {db_user};")
            print(f"✅ Database test '{db_test_name}' berhasil dibuat")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ℹ️ Database test '{db_test_name}' sudah ada")
        
        # Grant privileges
        print("🔑 Memberikan privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_test_name} TO {db_user};")
        
        cursor.close()
        conn.close()
        
        return {
            'host': db_host,
            'port': db_port,
            'db_name': db_name,
            'db_test_name': db_test_name,
            'db_user': db_user,
            'db_password': db_password
        }
        
    except Exception as e:
        print(f"❌ Error saat setup database: {e}")
        return None

def create_tables_and_admin(db_config):
    """Membuat tabel dan user admin default"""
    try:
        # Koneksi ke database Waskita
        print(f"\n🔌 Menghubungkan ke database '{db_config['db_name']}'...")
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            database=db_config['db_name']
        )
        cursor = conn.cursor()
        
        # Baca dan eksekusi schema SQL
        print("📋 Membuat tabel dari schema...")
        schema_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
        
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Eksekusi schema (skip jika tabel sudah ada)
            try:
                cursor.execute(schema_sql)
                print("✅ Schema database berhasil dibuat")
            except psycopg2.errors.DuplicateTable:
                print("ℹ️ Tabel sudah ada, melanjutkan...")
            except Exception as e:
                print(f"⚠️ Warning saat membuat schema: {e}")
        else:
            print("❌ File database_schema.sql tidak ditemukan")
            return False
        
        # Buat user admin default
        print("\n👑 Membuat user admin default...")
        # Default admin credentials - CHANGE IN PRODUCTION!
        admin_username = "[admin_username]"
        admin_email = "[admin@example.com]"
        admin_password = input("Masukkan password untuk admin (default: [admin_password]): ") or "[admin_password]"
        admin_fullname = "[Administrator Name]"
        
        # Hash password dengan benar
        password_hash = generate_password_hash(admin_password)
        
        # Insert admin user dengan ON CONFLICT untuk update password jika user sudah ada
        insert_admin_sql = """
        INSERT INTO users (username, email, password_hash, role, full_name, is_active, theme_preference) 
        VALUES (%s, %s, %s, 'admin', %s, TRUE, 'dark')
        ON CONFLICT (username) DO UPDATE SET
            password_hash = EXCLUDED.password_hash,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        cursor.execute(insert_admin_sql, (admin_username, admin_email, password_hash, admin_fullname))
        
        print(f"✅ User admin '{admin_username}' berhasil dibuat/diperbarui dengan password yang benar")
        
        # Commit perubahan
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Setup database berhasil!")
        print(f"📊 Database: {db_config['db_name']}")
        print(f"👤 Admin: {admin_username}")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: [HIDDEN FOR SECURITY]")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saat membuat tabel dan admin: {e}")
        return False

def update_env_file(db_config):
    """Update file .env dengan konfigurasi database"""
    try:
        print("\n📝 Mengupdate file .env...")
        
        env_content = f"""# Database Configuration - PostgreSQL Only
# IMPORTANT: Change these credentials in production!
DATABASE_URL=postgresql://{db_config['db_user']}:{db_config['db_password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}
TEST_DATABASE_URL=postgresql://{db_config['db_user']}:{db_config['db_password']}@{db_config['host']}:{db_config['port']}/{db_config['db_test_name']}
DATABASE_HOST={db_config['host']}
DATABASE_PORT={db_config['port']}
DATABASE_NAME={db_config['db_name']}
DATABASE_USER={db_config['db_user']}
DATABASE_PASSWORD={db_config['db_password']}

# Flask Configuration
SECRET_KEY=generate_your_own_secret_key_here_change_in_production
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Model Paths - relative paths for containerization compatibility
WORD2VEC_MODEL_PATH=models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=models/navesbayes/naive_bayes_model3.pkl

# Apify API Configuration
# IMPORTANT: Replace with your actual Apify API token
APIFY_API_TOKEN=your_apify_api_token_here
APIFY_BASE_URL=https://api.apify.com/v2

# Apify Actor IDs for different platforms
APIFY_TWITTER_ACTOR=CJdippxWmn9uRfooo
APIFY_FACEBOOK_ACTOR=apify/facebook-scraper
APIFY_INSTAGRAM_ACTOR=apify/instagram-scraper
APIFY_TIKTOK_ACTOR=clockworks/free-tiktok-scraper

# Social Media API Keys (Optional - untuk scraping)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret

FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_ACCESS_TOKEN=your-facebook-access-token

TIKTOK_API_KEY=your-tiktok-api-key
TIKTOK_API_SECRET=your-tiktok-api-secret

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password

# Redis Configuration (Optional - untuk caching)
REDIS_URL=redis://localhost:6379/0

# Pagination
POSTS_PER_PAGE=25

# Security
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/waskita.log

# API Configuration
WASKITA_API_KEY=generate_your_own_api_key_here
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ File .env berhasil diupdate")
        return True
        
    except Exception as e:
        print(f"❌ Error saat update .env: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Waskita Database Setup")
    print("=" * 50)
    print("Script ini akan:")
    print("1. Membuat database PostgreSQL")
    print("2. Membuat user database")
    print("3. Membuat tabel dari schema")
    print("4. Membuat user admin default")
    print("5. Mengupdate file .env")
    print()
    
    confirm = input("Lanjutkan? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Setup dibatalkan")
        return
    
    # Step 1: Setup database dan user
    db_config = create_database_and_user()
    if not db_config:
        print("❌ Setup database gagal")
        return
    
    # Step 2: Buat tabel dan admin
    if not create_tables_and_admin(db_config):
        print("❌ Setup tabel dan admin gagal")
        return
    
    # Step 3: Update .env
    if not update_env_file(db_config):
        print("❌ Update .env gagal")
        return
    
    print("\n" + "=" * 50)
    print("🎉 SETUP BERHASIL!")
    print("=" * 50)
    print("✅ Database PostgreSQL siap digunakan")
    print("✅ User admin telah dibuat")
    print("✅ File .env telah diupdate")
    print()
    print("📋 Langkah selanjutnya:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Setup Apify API token di .env")
    print("3. Jalankan aplikasi: python app.py")
    print()
    print("🔗 Akses aplikasi di: http://localhost:5000")

if __name__ == "__main__":
    main()