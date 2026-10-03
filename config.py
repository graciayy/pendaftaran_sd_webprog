class Config:
    """Konfigurasi aplikasi"""
    
    # Database Configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''  # Kosongkan jika pakai XAMPP default
    DB_NAME = 'pendaftaran_sd'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    UPLOAD_PHOTO_FOLDER = 'static/uploads/photos'
    UPLOAD_DOCUMENT_FOLDER = 'static/uploads/documents'
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # Secret Key untuk session
    SECRET_KEY = 'ganti-dengan-kode-rahasia-anda-12345'
    
    # Pagination
    ITEMS_PER_PAGE = 10