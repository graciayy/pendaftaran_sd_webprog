from models.database import Database


class Student:
    """Class untuk mengelola data siswa"""
    
    def __init__(self):
        """Constructor"""
        self.db = Database()
        self.db.connect()
        self.table = "students"
    
    def create(self, data):
        """
        Tambah siswa baru
        
        Args:
            data: Dictionary berisi data siswa
            
        Returns:
            student_id jika berhasil, False jika gagal
        """
        query = f"""
            INSERT INTO {self.table} 
            (full_name, birth_date, gender, parent_name, parent_phone, parent_address, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data.get('full_name'),
            data.get('birth_date'),
            data.get('gender'),
            data.get('parent_name'),
            data.get('parent_phone'),
            data.get('parent_address'),
            data.get('photo', None)
        )
        
        result = self.db.execute_query(query, params)
        return result
    
    def read_all(self):
        """
        Ambil semua data siswa
        
        Returns:
            List of dictionaries
        """
        query = f"SELECT * FROM {self.table} ORDER BY created_at DESC"
        return self.db.fetch_all(query)
    
    def read_one(self, student_id):
        """
        Ambil satu siswa berdasarkan ID
        
        Args:
            student_id: ID siswa
            
        Returns:
            Dictionary atau None
        """
        query = f"SELECT * FROM {self.table} WHERE student_id = %s"
        return self.db.fetch_one(query, (student_id,))
    
    def update(self, student_id, data):
        """
        Update data siswa
        
        Args:
            student_id: ID siswa
            data: Dictionary berisi data baru
            
        Returns:
            True jika berhasil, False jika gagal
        """
        query = f"""
            UPDATE {self.table} 
            SET full_name = %s,
                birth_date = %s,
                gender = %s,
                parent_name = %s,
                parent_phone = %s,
                parent_address = %s,
                photo = %s
            WHERE student_id = %s
        """
        
        params = (
            data.get('full_name'),
            data.get('birth_date'),
            data.get('gender'),
            data.get('parent_name'),
            data.get('parent_phone'),
            data.get('parent_address'),
            data.get('photo'),
            student_id
        )
        
        return self.db.execute_query(query, params)
    
    def delete(self, student_id):
        """
        Hapus siswa
        
        Args:
            student_id: ID siswa
            
        Returns:
            True jika berhasil, False jika gagal
        """
        query = f"DELETE FROM {self.table} WHERE student_id = %s"
        return self.db.execute_query(query, (student_id,))
    
    def search(self, keyword):
        """
        Cari siswa berdasarkan nama
        
        Args:
            keyword: Kata kunci pencarian
            
        Returns:
            List of dictionaries
        """
        query = f"""
            SELECT * FROM {self.table} 
            WHERE full_name LIKE %s OR parent_name LIKE %s
            ORDER BY created_at DESC
        """
        search_term = f"%{keyword}%"
        return self.db.fetch_all(query, (search_term, search_term))
    
    def count_all(self):
        """
        Hitung total siswa
        
        Returns:
            Integer jumlah siswa
        """
        query = f"SELECT COUNT(*) as total FROM {self.table}"
        result = self.db.fetch_one(query)
        return result['total'] if result else 0
    
    def get_by_gender(self, gender):
        """
        Ambil siswa berdasarkan jenis kelamin
        
        Args:
            gender: 'M' atau 'F'
            
        Returns:
            List of dictionaries
        """
        query = f"SELECT * FROM {self.table} WHERE gender = %s ORDER BY full_name ASC"
        return self.db.fetch_all(query, (gender,))
    
    def __del__(self):
        """Destructor - tutup koneksi database"""
        if hasattr(self, 'db'):
            self.db.disconnect()