import re
from datetime import datetime, date


class Validator:
    """Class untuk validasi input data"""
    
    def __init__(self):
        """Constructor"""
        self.errors = {}
    
    def validate_required(self, field, value, field_name):
        """
        Validasi field wajib diisi
        
        Args:
            field: Nama field
            value: Nilai field
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        if not value or str(value).strip() == '':
            self.errors[field] = f"{field_name} wajib diisi"
            return False
        return True
    
    def validate_date(self, field, value, field_name):
        """
        Validasi format tanggal (YYYY-MM-DD)
        
        Args:
            field: Nama field
            value: Nilai tanggal
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            self.errors[field] = f"{field_name} tidak valid (format: YYYY-MM-DD)"
            return False
    
    def validate_age(self, field, birth_date_str, min_age=5, max_age=8):
        """
        Validasi usia siswa
        
        Args:
            field: Nama field
            birth_date_str: Tanggal lahir (string)
            min_age: Usia minimum
            max_age: Usia maksimum
            
        Returns:
            True jika valid, False jika tidak
        """
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            today = date.today()
            
            # Hitung usia
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
            
            if age < min_age or age > max_age:
                self.errors[field] = f"Usia siswa harus antara {min_age}-{max_age} tahun (usia saat ini: {age} tahun)"
                return False
            
            return True
            
        except ValueError:
            self.errors[field] = "Format tanggal lahir tidak valid"
            return False
    
    def validate_phone(self, field, value, field_name):
        """
        Validasi nomor telepon (10-15 digit angka)
        
        Args:
            field: Nama field
            value: Nomor telepon
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        pattern = r'^[0-9]{10,15}$'
        if not re.match(pattern, str(value)):
            self.errors[field] = f"{field_name} harus berisi 10-15 digit angka"
            return False
        return True
    
    def validate_length(self, field, value, min_length, max_length, field_name):
        """
        Validasi panjang karakter
        
        Args:
            field: Nama field
            value: Nilai field
            min_length: Panjang minimum
            max_length: Panjang maksimum
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        length = len(str(value))
        if length < min_length or length > max_length:
            self.errors[field] = f"{field_name} harus antara {min_length}-{max_length} karakter"
            return False
        return True
    
    def validate_gender(self, field, value):
        """
        Validasi jenis kelamin (M atau F)
        
        Args:
            field: Nama field
            value: Nilai jenis kelamin
            
        Returns:
            True jika valid, False jika tidak
        """
        if value not in ['M', 'F']:
            self.errors[field] = "Jenis kelamin harus M atau F"
            return False
        return True
    
    def validate_email(self, field, value, field_name):
        """
        Validasi format email
        
        Args:
            field: Nama field
            value: Email
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, str(value)):
            self.errors[field] = f"{field_name} tidak valid"
            return False
        return True
    
    def validate_file_extension(self, field, filename, allowed_extensions):
        """
        Validasi ekstensi file
        
        Args:
            field: Nama field
            filename: Nama file
            allowed_extensions: Set ekstensi yang diperbolehkan
            
        Returns:
            True jika valid, False jika tidak
        """
        if '.' not in filename:
            self.errors[field] = "File harus memiliki ekstensi"
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            self.errors[field] = f"Ekstensi file harus: {', '.join(allowed_extensions)}"
            return False
        
        return True
    
    def validate_file_size(self, field, file_size, max_size, field_name):
        """
        Validasi ukuran file
        
        Args:
            field: Nama field
            file_size: Ukuran file dalam bytes
            max_size: Ukuran maksimum dalam bytes
            field_name: Nama field yang ditampilkan
            
        Returns:
            True jika valid, False jika tidak
        """
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            self.errors[field] = f"{field_name} maksimal {max_mb}MB"
            return False
        return True
    
    def validate_status(self, field, value):
        """
        Validasi status pendaftaran
        
        Args:
            field: Nama field
            value: Status
            
        Returns:
            True jika valid, False jika tidak
        """
        valid_statuses = ['pending', 'accepted', 'rejected']
        if value not in valid_statuses:
            self.errors[field] = f"Status harus: {', '.join(valid_statuses)}"
            return False
        return True
    
    def get_errors(self):
        """
        Ambil semua error
        
        Returns:
            Dictionary errors
        """
        return self.errors
    
    def has_errors(self):
        """
        Cek apakah ada error
        
        Returns:
            True jika ada error, False jika tidak
        """
        return len(self.errors) > 0
    
    def clear_errors(self):
        """Hapus semua error"""
        self.errors = {}
    
    def get_first_error(self):
        """
        Ambil error pertama
        
        Returns:
            String error pertama atau None
        """
        if self.errors:
            return list(self.errors.values())[0]
        return None