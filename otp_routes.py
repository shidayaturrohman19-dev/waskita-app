# Routes untuk OTP Authentication System
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets
import string
from models import db, User, UserActivity
from models_otp import RegistrationRequest, AdminNotification, OTPEmailLog
from email_service import email_service
from utils import admin_required, log_user_activity
from markupsafe import escape
from security_logger import log_registration_attempt, log_admin_action, log_rate_limit_exceeded

# Import limiter from app
from flask import current_app

# Create blueprint
otp_bp = Blueprint('otp', __name__)

def generate_otp(length=6):
    """Generate random OTP code"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))

@otp_bp.route('/register-request', methods=['GET', 'POST'])
def register_request():
    """
    Form permintaan registrasi yang akan mengirim OTP ke admin
    Rate limited: 3 attempts per hour per IP
    """
    if request.method == 'GET':
        return render_template('auth/register_request.html')
    
    try:
        # Get form data with input sanitization
        username = escape(request.form.get('username', '').strip())
        email = escape(request.form.get('email', '').strip())
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = escape(request.form.get('full_name', '').strip())
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('Semua field wajib diisi', 'error')
            return render_template('auth/register_request.html')
        
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok', 'error')
            return render_template('auth/register_request.html')
        
        if len(password) < 8:
            flash('Password minimal 8 karakter', 'error')
            return render_template('auth/register_request.html')
        
        # Enhanced password validation
        if not any(c.isupper() for c in password):
            flash('Password harus mengandung minimal 1 huruf besar', 'error')
            return render_template('auth/register_request.html')
        
        if not any(c.islower() for c in password):
            flash('Password harus mengandung minimal 1 huruf kecil', 'error')
            return render_template('auth/register_request.html')
        
        if not any(c.isdigit() for c in password):
            flash('Password harus mengandung minimal 1 angka', 'error')
            return render_template('auth/register_request.html')
        
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Username atau email sudah terdaftar', 'error')
            return render_template('auth/register_request.html')
        
        # Check if there's pending request
        pending_request = RegistrationRequest.query.filter(
            (RegistrationRequest.username == username) | 
            (RegistrationRequest.email == email)
        ).filter_by(status='pending').first()
        
        if pending_request:
            flash('Sudah ada permintaan registrasi yang sedang menunggu persetujuan untuk username atau email ini', 'warning')
            return render_template('auth/register_request.html')
        
        # Create registration request (OTP akan di-generate otomatis di model)
        registration_request = RegistrationRequest(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name if full_name else None
        )
        
        # Set status ke pending
        registration_request.status = 'pending'
        
        db.session.add(registration_request)
        db.session.commit()
        
        # Log registration attempt
        log_registration_attempt(username, email, request.remote_addr)
        
        # Send OTP to admin
        success, message = email_service.send_otp_to_admin(registration_request)
        
        if success:
            flash(f'Permintaan registrasi berhasil dikirim! {message}. Admin akan meninjau dan mengirim konfirmasi melalui email.', 'success')
            return redirect(url_for('otp.registration_status', request_id=registration_request.id))
        else:
            flash(f'Permintaan registrasi tersimpan, tetapi gagal mengirim email ke admin: {message}', 'warning')
            return redirect(url_for('otp.registration_status', request_id=registration_request.id))
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in register_request: {str(e)}")
        flash('Terjadi kesalahan sistem. Silakan coba lagi.', 'error')
        return render_template('auth/register_request.html')

@otp_bp.route('/registration-status/<int:request_id>')
def registration_status(request_id):
    """
    Halaman status permintaan registrasi
    """
    registration_request = RegistrationRequest.query.get_or_404(request_id)
    
    # Get email logs for this request
    email_logs = OTPEmailLog.query.filter_by(
        registration_request_id=request_id
    ).order_by(OTPEmailLog.created_at.desc()).all()
    
    return render_template('auth/registration_status.html', 
                         request=registration_request, 
                         email_logs=email_logs)

@otp_bp.route('/admin/pending-registrations')
@login_required
@admin_required
def pending_registrations():
    """
    Halaman admin untuk melihat permintaan registrasi yang pending
    """
    pending_requests = RegistrationRequest.query.filter_by(
        status='pending'
    ).order_by(RegistrationRequest.created_at.desc()).all()
    
    # Get notifications for current admin
    notifications = AdminNotification.query.join(RegistrationRequest).filter(
        RegistrationRequest.status == 'pending'
    ).order_by(AdminNotification.created_at.desc()).all()
    
    return render_template('admin/pending_registrations.html', 
                         pending_requests=pending_requests,
                         notifications=notifications,
                         datetime=datetime)

@otp_bp.route('/admin/approve-registration/<int:request_id>', methods=['GET', 'POST'])
def approve_registration_public(request_id):
    """
    Halaman publik untuk approve/reject registrasi dengan OTP (tanpa login)
    """
    registration_request = RegistrationRequest.query.get_or_404(request_id)
    
    if registration_request.status != 'pending':
        flash('Permintaan registrasi ini sudah diproses', 'warning')
        return render_template('admin/approve_registration_public.html', 
                             request=registration_request, 
                             already_processed=True)
    
    if request.method == 'GET':
        return render_template('admin/approve_registration_public.html', 
                             request=registration_request)
    
    try:
        # Get form data
        otp_input = request.form.get('otp_code', '').strip()
        action = request.form.get('action')  # 'approve' or 'reject'
        admin_notes = request.form.get('admin_notes', '').strip()
        admin_email = request.form.get('admin_email', '').strip()
        
        # Validate required fields
        if not otp_input:
            flash('Kode OTP wajib diisi', 'error')
            return render_template('admin/approve_registration_public.html', 
                                 request=registration_request)
        
        # Handle admin email - if 'system_admin', get the first active admin
        if admin_email == 'system_admin' or not admin_email:
            admin_user = User.query.filter_by(role='admin', is_active=True).first()
            if not admin_user:
                flash('Tidak ada admin aktif yang ditemukan', 'error')
                return render_template('admin/approve_registration_public.html', 
                                     request=registration_request)
        else:
            # Validate specific admin email
            admin_user = User.query.filter_by(email=admin_email, role='admin', is_active=True).first()
            if not admin_user:
                flash('Email admin tidak valid atau tidak aktif', 'error')
                return render_template('admin/approve_registration_public.html', 
                                     request=registration_request)
        
        # Validate OTP
        if otp_input != registration_request.otp_code:
            flash('Kode OTP tidak valid', 'error')
            return render_template('admin/approve_registration_public.html', 
                                 request=registration_request)
        
        # Check OTP expiration
        if datetime.utcnow() > registration_request.otp_expires_at:
            flash('Kode OTP sudah expired. Silakan minta OTP baru.', 'error')
            return render_template('admin/approve_registration_public.html', 
                                 request=registration_request)
        
        if action == 'approve':
            # Check if username already exists
            existing_user = User.query.filter_by(username=registration_request.username).first()
            if existing_user:
                flash('Username sudah digunakan. Registrasi tidak dapat disetujui.', 'error')
                return render_template('admin/approve_registration_public.html', 
                                     request=registration_request)
            
            # Check if email already exists
            existing_email = User.query.filter_by(email=registration_request.email).first()
            if existing_email:
                flash('Email sudah digunakan. Registrasi tidak dapat disetujui.', 'error')
                return render_template('admin/approve_registration_public.html', 
                                     request=registration_request)
            
            # Create new user
            new_user = User(
                username=registration_request.username,
                email=registration_request.email,
                full_name=registration_request.full_name,
                password_hash=registration_request.password_hash,
                role='user',
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_user)
            
            # Update registration request
            registration_request.status = 'approved'
            registration_request.approved_by = admin_user.id
            registration_request.approved_at = datetime.utcnow()
            registration_request.admin_notes = admin_notes
            
            # Log admin activity
            log_user_activity(
                user_id=admin_user.id,
                action='user_registration_approved',
                description=f'Approved registration for user: {registration_request.username} via public link'
            )
            
            db.session.commit()
            
            # Send approval notification to user
            email_service.send_approval_notification(registration_request, admin_user)
            
            flash(f'Registrasi user {registration_request.username} berhasil disetujui!', 'success')
            
        elif action == 'reject':
            # Update registration request
            registration_request.status = 'rejected'
            registration_request.approved_by = admin_user.id
            registration_request.approved_at = datetime.utcnow()
            registration_request.admin_notes = admin_notes
            
            # Log admin activity
            log_user_activity(
                user_id=admin_user.id,
                action='user_registration_rejected',
                description=f'Rejected registration for user: {registration_request.username} via public link'
            )
            
            db.session.commit()
            
            flash(f'Registrasi user {registration_request.username} ditolak.', 'info')
        
        return render_template('admin/approve_registration_public.html', 
                             request=registration_request, 
                             processed=True)
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in approve_registration_public: {str(e)}")
        flash('Terjadi kesalahan sistem. Silakan coba lagi.', 'error')
        return render_template('admin/approve_registration_public.html', 
                             request=registration_request)

@otp_bp.route('/admin/approve-registration-dashboard/<int:request_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def approve_registration(request_id):
    """
    Halaman admin untuk approve/reject registrasi dengan OTP
    """
    registration_request = RegistrationRequest.query.get_or_404(request_id)
    
    if registration_request.status != 'pending':
        flash('Permintaan registrasi ini sudah diproses', 'warning')
        return redirect(url_for('otp.pending_registrations'))
    
    if request.method == 'GET':
        return render_template('admin/approve_registration.html', 
                             request=registration_request)
    
    try:
        # Get form data
        otp_input = request.form.get('otp_code', '').strip()
        action = request.form.get('action')  # 'approve' or 'reject'
        admin_notes = request.form.get('admin_notes', '').strip()
        
        # Validate OTP
        if not otp_input:
            flash('Kode OTP wajib diisi', 'error')
            return render_template('admin/approve_registration.html', 
                                 request=registration_request)
        
        if otp_input != registration_request.otp_code:
            flash('Kode OTP tidak valid', 'error')
            return render_template('admin/approve_registration.html', 
                                 request=registration_request)
        
        # Check OTP expiration
        if datetime.utcnow() > registration_request.otp_expires_at:
            flash('Kode OTP sudah expired', 'error')
            registration_request.status = 'expired'
            db.session.commit()
            return render_template('admin/approve_registration.html', 
                                 request=registration_request)
        
        if action == 'approve':
            # Create new user
            new_user = User(
                username=registration_request.username,
                email=registration_request.email,
                password_hash=registration_request.password_hash,
                full_name=registration_request.full_name,
                role='user',
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_user)
            
            # Update registration request
            registration_request.status = 'approved'
            registration_request.approved_by = current_user.id
            registration_request.approved_at = datetime.utcnow()
            registration_request.admin_notes = admin_notes
            
            # Log admin activity
            log_user_activity(
                user_id=current_user.id,
                action='user_registration_approved',
                description=f'Approved registration for user: {registration_request.username}'
            )
            
            db.session.commit()
            
            # Send approval notification to user
            email_service.send_approval_notification(registration_request, current_user)
            
            flash(f'Registrasi user {registration_request.username} berhasil disetujui!', 'success')
            
        elif action == 'reject':
            # Update registration request
            registration_request.status = 'rejected'
            registration_request.approved_by = current_user.id
            registration_request.approved_at = datetime.utcnow()
            registration_request.admin_notes = admin_notes
            
            # Log admin activity
            log_user_activity(
                user_id=current_user.id,
                action='user_registration_rejected',
                description=f'Rejected registration for user: {registration_request.username}'
            )
            
            db.session.commit()
            
            flash(f'Registrasi user {registration_request.username} ditolak.', 'info')
        
        return redirect(url_for('otp.pending_registrations'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in approve_registration: {str(e)}")
        flash('Terjadi kesalahan sistem. Silakan coba lagi.', 'error')
        return render_template('admin/approve_registration.html', 
                             request=registration_request)

@otp_bp.route('/admin/registration-history')
@login_required
@admin_required
def registration_history():
    """
    Halaman history semua permintaan registrasi
    """
    from utils import format_datetime
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    requests = RegistrationRequest.query.order_by(
        RegistrationRequest.created_at.desc()
    ).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/registration_history.html', 
                         requests=requests, 
                         format_datetime=format_datetime)

@otp_bp.route('/api/registration-stats')
@login_required
@admin_required
def registration_stats():
    """
    API endpoint untuk statistik registrasi (untuk dashboard admin)
    """
    try:
        stats = {
            'pending': RegistrationRequest.query.filter_by(status='pending').count(),
            'approved': RegistrationRequest.query.filter_by(status='approved').count(),
            'rejected': RegistrationRequest.query.filter_by(status='rejected').count(),
            'expired': RegistrationRequest.query.filter_by(status='expired').count(),
            'total': RegistrationRequest.query.count()
        }
        
        # Recent requests (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_requests = RegistrationRequest.query.filter(
            RegistrationRequest.created_at >= seven_days_ago
        ).count()
        
        stats['recent'] = recent_requests
        
        return jsonify(stats)
        
    except Exception as e:
        current_app.logger.error(f"Error in registration_stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch stats'}), 500

@otp_bp.route('/admin/resend-otp/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def resend_otp(request_id):
    """
    Resend OTP untuk permintaan registrasi tertentu
    """
    try:
        registration_request = RegistrationRequest.query.get_or_404(request_id)
        
        if registration_request.status != 'pending':
            return jsonify({'success': False, 'message': 'Permintaan sudah diproses'}), 400
        
        # Generate new OTP
        new_otp = generate_otp()
        new_expires_at = datetime.utcnow() + timedelta(hours=24)
        
        registration_request.otp_code = new_otp
        registration_request.otp_expires_at = new_expires_at
        
        db.session.commit()
        
        # Send new OTP to admin
        success, message = email_service.send_otp_to_admin(registration_request)
        
        if success:
            return jsonify({'success': True, 'message': f'OTP baru berhasil dikirim: {message}'})
        else:
            return jsonify({'success': False, 'message': f'Gagal mengirim OTP: {message}'}), 500
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in resend_otp: {str(e)}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan sistem'}), 500

@otp_bp.route('/admin/delete-registration-request/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def delete_registration_request(request_id):
    """
    Hapus permintaan registrasi
    """
    try:
        registration_request = RegistrationRequest.query.get_or_404(request_id)
        username = registration_request.username  # Store username before deletion
        
        # First, delete all related AdminNotifications
        AdminNotification.query.filter_by(registration_request_id=request_id).delete()
        
        # Delete all related OTPEmailLogs
        OTPEmailLog.query.filter_by(registration_request_id=request_id).delete()
        
        # Log admin activity
        log_user_activity(
            user_id=current_user.id,
            action='registration_request_deleted',
            description=f'Deleted registration request for user: {username}'
        )
        
        # Finally, delete the registration request
        db.session.delete(registration_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Permintaan registrasi untuk {username} berhasil dihapus'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting registration request: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Terjadi kesalahan sistem'
        }), 500

@otp_bp.route('/admin/delete-registration-history/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def delete_registration_history(request_id):
    """
    Hapus riwayat registrasi (untuk data yang sudah diproses)
    """
    try:
        registration_request = RegistrationRequest.query.get_or_404(request_id)
        username = registration_request.username  # Store username before deletion
        
        # Pastikan hanya bisa hapus yang sudah diproses (approved/rejected)
        if registration_request.status == 'pending':
            return jsonify({
                'success': False,
                'message': 'Tidak dapat menghapus permintaan yang masih pending. Gunakan halaman Pending Registrations.'
            }), 400
        
        # First, delete all related AdminNotifications
        AdminNotification.query.filter_by(registration_request_id=request_id).delete()
        
        # Delete all related OTPEmailLogs
        OTPEmailLog.query.filter_by(registration_request_id=request_id).delete()
        
        # Log admin activity
        log_user_activity(
            user_id=current_user.id,
            action='registration_history_deleted',
            description=f'Deleted registration history for user: {username} (status: {registration_request.status})'
        )
        
        # Finally, delete the registration request
        db.session.delete(registration_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Riwayat registrasi untuk {username} berhasil dihapus'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting registration history: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Terjadi kesalahan sistem'
        }), 500