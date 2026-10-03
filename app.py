from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Import class yang sudah dibuat
from models.student import Student
from models.registration import Registration
from models.user import User
from validators.validator import Validator
from config import Config

# Inisialisasi Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Pastikan folder upload ada
os.makedirs(Config.UPLOAD_PHOTO_FOLDER, exist_ok=True)
os.makedirs(Config.UPLOAD_DOCUMENT_FOLDER, exist_ok=True)


def allowed_file(filename, file_type='photo'):
    """
    Cek apakah ekstensi file diperbolehkan
    
    Args:
        filename: Nama file
        file_type: 'photo' atau 'document'
        
    Returns:
        True jika diperbolehkan, False jika tidak
    """
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'photo':
        return ext in Config.ALLOWED_PHOTO_EXTENSIONS
    elif file_type == 'document':
        return ext in Config.ALLOWED_DOCUMENT_EXTENSIONS
    
    return False


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')


@app.route('/pendaftaran', methods=['GET', 'POST'])
def pendaftaran():
    """Halaman form pendaftaran siswa"""
    
    if request.method == 'POST':
        # Ambil data dari form
        data = {
            'full_name': request.form.get('full_name'),
            'birth_date': request.form.get('birth_date'),
            'gender': request.form.get('gender'),
            'parent_name': request.form.get('parent_name'),
            'parent_phone': request.form.get('parent_phone'),
            'parent_address': request.form.get('parent_address')
        }
        
        # Validasi input
        validator = Validator()
        
        validator.validate_required('full_name', data['full_name'], 'Nama Lengkap')
        validator.validate_length('full_name', data['full_name'], 3, 150, 'Nama Lengkap')
        
        validator.validate_required('birth_date', data['birth_date'], 'Tanggal Lahir')
        validator.validate_date('birth_date', data['birth_date'], 'Tanggal Lahir')
        validator.validate_age('birth_date', data['birth_date'], min_age=5, max_age=8)
        
        validator.validate_required('gender', data['gender'], 'Jenis Kelamin')
        validator.validate_gender('gender', data['gender'])
        
        validator.validate_required('parent_name', data['parent_name'], 'Nama Orang Tua')
        validator.validate_length('parent_name', data['parent_name'], 3, 150, 'Nama Orang Tua')
        
        validator.validate_required('parent_phone', data['parent_phone'], 'Nomor Telepon')
        validator.validate_phone('parent_phone', data['parent_phone'], 'Nomor Telepon')
        
        validator.validate_required('parent_address', data['parent_address'], 'Alamat')
        validator.validate_length('parent_address', data['parent_address'], 10, 500, 'Alamat')
        
        # Upload foto (opsional)
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                if allowed_file(file.filename, 'photo'):
                    # Generate nama file unik
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    original_filename = secure_filename(file.filename)
                    photo_filename = f"{timestamp}_{original_filename}"
                    
                    # Simpan file
                    file_path = os.path.join(Config.UPLOAD_PHOTO_FOLDER, photo_filename)
                    file.save(file_path)
                    data['photo'] = photo_filename
                else:
                    validator.errors['photo'] = "Format foto harus JPG, PNG, atau JPEG"
        
        # Jika ada error validasi
        if validator.has_errors():
            for error in validator.get_errors().values():
                flash(error, 'danger')
            return render_template('form_pendaftaran.html', data=data)
        
        # Simpan data siswa
        try:
            student = Student()
            student_id = student.create(data)
            
            if student_id:
                # Buat pendaftaran
                registration = Registration()
                reg_data = {
                    'student_id': student_id,
                    'status': 'pending'
                }
                reg_id = registration.create(reg_data)
                
                if reg_id:
                    flash('✅ Pendaftaran berhasil! Silakan tunggu konfirmasi dari admin.', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('⚠️ Data siswa tersimpan, tetapi gagal membuat pendaftaran.', 'warning')
            else:
                flash('❌ Gagal menyimpan data. Silakan coba lagi.', 'danger')
                
        except Exception as e:
            flash(f'❌ Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('form_pendaftaran.html')


@app.route('/siswa')
def daftar_siswa():
    """Halaman daftar siswa"""
    try:
        student = Student()
        students = student.read_all()
        return render_template('daftar_siswa.html', students=students)
    except Exception as e:
        flash(f'❌ Gagal memuat data siswa: {str(e)}', 'danger')
        return render_template('daftar_siswa.html', students=[])


@app.route('/siswa/<int:student_id>')
def detail_siswa(student_id):
    """Halaman detail siswa"""
    try:
        student = Student()
        student_data = student.read_one(student_id)
        
        if student_data:
            return render_template('detail_siswa.html', student=student_data)
        else:
            flash('❌ Siswa tidak ditemukan', 'danger')
            return redirect(url_for('daftar_siswa'))
            
    except Exception as e:
        flash(f'❌ Gagal memuat detail siswa: {str(e)}', 'danger')
        return redirect(url_for('daftar_siswa'))


@app.route('/dashboard')
def dashboard():
    """Halaman dashboard admin"""
    try:
        registration = Registration()
        
        # Hitung statistik
        pending = registration.count_by_status('pending')
        accepted = registration.count_by_status('accepted')
        rejected = registration.count_by_status('rejected')
        total = registration.count_all()
        
        # Ambil semua pendaftaran
        all_registrations = registration.read_all()
        
        return render_template('dashboard.html',
                             pending=pending,
                             accepted=accepted,
                             rejected=rejected,
                             total=total,
                             registrations=all_registrations)
                             
    except Exception as e:
        flash(f'❌ Gagal memuat dashboard: {str(e)}', 'danger')
        return render_template('dashboard.html',
                             pending=0,
                             accepted=0,
                             rejected=0,
                             total=0,
                             registrations=[])


@app.route('/dashboard/update-status/<int:registration_id>', methods=['POST'])
def update_status(registration_id):
    """Update status pendaftaran"""
    try:
        new_status = request.form.get('status')
        
        # Validasi status
        validator = Validator()
        validator.validate_status('status', new_status)
        
        if validator.has_errors():
            flash(validator.get_first_error(), 'danger')
            return redirect(url_for('dashboard'))
        
        # Update status
        registration = Registration()
        result = registration.update_status(registration_id, new_status, processed_by=1)
        
        if result:
            flash(f'✅ Status berhasil diubah menjadi {new_status}', 'success')
        else:
            flash('❌ Gagal mengubah status', 'danger')
            
    except Exception as e:
        flash(f'❌ Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))


@app.route('/search')
def search():
    """Pencarian siswa"""
    keyword = request.args.get('q', '')
    
    if keyword:
        try:
            student = Student()
            results = student.search(keyword)
            return render_template('daftar_siswa.html', students=results, keyword=keyword)
        except Exception as e:
            flash(f'❌ Gagal melakukan pencarian: {str(e)}', 'danger')
            return render_template('daftar_siswa.html', students=[], keyword=keyword)
    else:
        return redirect(url_for('daftar_siswa'))


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Halaman 404"""
    return "<h1>404 - Halaman Tidak Ditemukan</h1>", 404


@app.errorhandler(500)
def internal_error(error):
    """Halaman 500"""
    return "<h1>500 - Internal Server Error</h1>", 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting Aplikasi Pendaftaran SD")
    print("=" * 50)
    print("📍 URL: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)