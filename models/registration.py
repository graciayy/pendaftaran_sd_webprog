from models.database import Database


class Registration:
    """Class untuk mengelola data pendaftaran"""
    
    def __init__(self):
        """Constructor"""
        self.db = Database()
        self.db.connect()
        self.table = "registrations"
    
    def create(self, data):
        """
        Buat pendaftaran baru
        
        Args:
            data: Dictionary berisi data pendaftaran
            
        Returns:
            registration_id jika berhasil, False jika gagal
        """
        query = f"""
            INSERT INTO {self.table} 
            (student_id, registration_date, status, document_path)
            VALUES (%s, %s, %s, %s)
        """
        
        params = (
            data.get('student_id'),
            data.get('registration_date', None),
            data.get('status', 'pending'),
            data.get('document_path', None)
        )
        
        return self.db.execute_query(query, params)
    
    def read_all(self):
        """
        Ambil semua pendaftaran dengan join ke table students
        
        Returns:
            List of dictionaries
        """
        query = f"""
            SELECT r.*, s.full_name, s.birth_date, s.gender, 
                   s.parent_name, s.parent_phone, s.parent_address, s.photo
            FROM {self.table} r
            LEFT JOIN students s ON r.student_id = s.student_id
            ORDER BY r.registration_date DESC
        """
        return self.db.fetch_all(query)
    
    def read_one(self, registration_id):
        """
        Ambil satu pendaftaran berdasarkan ID
        
        Args:
            registration_id: ID pendaftaran
            
        Returns:
            Dictionary atau None
        """
        query = f"""
            SELECT r.*, s.full_name, s.birth_date, s.gender,
                   s.parent_name, s.parent_phone, s.parent_address, s.photo
            FROM {self.table} r
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE r.registration_id = %s
        """
        return self.db.fetch_one(query, (registration_id,))
    
    def get_by_status(self, status):
        """
        Ambil pendaftaran berdasarkan status
        
        Args:
            status: 'pending', 'accepted', atau 'rejected'
            
        Returns:
            List of dictionaries
        """
        query = f"""
            SELECT r.*, s.full_name, s.birth_date, s.parent_name
            FROM {self.table} r
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE r.status = %s
            ORDER BY r.registration_date DESC
        """
        return self.db.fetch_all(query, (status,))
    
    def update_status(self, registration_id, status, processed_by=None):
        """
        Update status pendaftaran
        
        Args:
            registration_id: ID pendaftaran
            status: Status baru
            processed_by: ID user yang memproses (optional)
            
        Returns:
            True jika berhasil, False jika gagal
        """
        query = f"""
            UPDATE {self.table}
            SET status = %s,
                processed_by = %s,
                processed_at = NOW()
            WHERE registration_id = %s
        """
        return self.db.execute_query(query, (status, processed_by, registration_id))
    
    def count_by_status(self, status):
        """
        Hitung jumlah pendaftaran berdasarkan status
        
        Args:
            status: 'pending', 'accepted', atau 'rejected'
            
        Returns:
            Integer jumlah pendaftaran
        """
        query = f"SELECT COUNT(*) as total FROM {self.table} WHERE status = %s"
        result = self.db.fetch_one(query, (status,))
        return result['total'] if result else 0
    
    def count_all(self):
        """
        Hitung total semua pendaftaran
        
        Returns:
            Integer jumlah pendaftaran
        """
        query = f"SELECT COUNT(*) as total FROM {self.table}"
        result = self.db.fetch_one(query)
        return result['total'] if result else 0
    
    def delete(self, registration_id):
        """
        Hapus pendaftaran
        
        Args:
            registration_id: ID pendaftaran
            
        Returns:
            True jika berhasil, False jika gagal
        """
        query = f"DELETE FROM {self.table} WHERE registration_id = %s"
        return self.db.execute_query(query, (registration_id,))
    
    def get_recent(self, limit=10):
        """
        Ambil pendaftaran terbaru
        
        Args:
            limit: Jumlah data yang diambil
            
        Returns:
            List of dictionaries
        """
        query = f"""
            SELECT r.*, s.full_name, s.parent_name
            FROM {self.table} r
            LEFT JOIN students s ON r.student_id = s.student_id
            ORDER BY r.registration_date DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))
    
    def __del__(self):
        """Destructor - tutup koneksi database"""
        if hasattr(self, 'db'):
            self.db.disconnect()