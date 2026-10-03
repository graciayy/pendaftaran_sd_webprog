from models.database import Database
import hashlib


class User:
    """Class untuk mengelola data user/admin"""
    
    def __init__(self):
        """Constructor"""
        self.db = Database()
        self.db.connect()
        self.table = "users"
    
    def hash_password(self, password):
        """
        Hash password menggunakan SHA256
        
        Args:
            password: Password plain text
            
        Returns:
            Password yang sudah di-hash
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create(self, data):
        """
        Tambah user baru
        
        Args:
            data: Dictionary berisi username, password, role
            
        Returns:
            user_id jika berhasil, False jika gagal
        """
        query = f"""
            INSERT INTO {self.table} 
            (username, password_hash, role)
            VALUES (%s, %s, %s)
        """
        
        password_hash = self.hash_password(data.get('password'))
        
        params = (
            data.get('username'),
            password_hash,
            data.get('role', 'operator')
        )
        
        return self.db.execute_query(query, params)
    
    def read_all(self):
        """
        Ambil semua user
        
        Returns:
            List of dictionaries
        """
        query = f"SELECT user_id, username, role, created_at FROM {self.table} ORDER BY created_at DESC"
        return self.db.fetch_all(query)
    
    def read_one(self, user_id):
        """
        Ambil satu user berdasarkan ID
        
        Args:
            user_id: ID user
            
        Returns:
            Dictionary atau None
        """
        query = f"SELECT user_id, username, role, created_at FROM {self.table} WHERE user_id = %s"
        return self.db.fetch_one(query, (user_id,))
    
    def find_by_username(self, username):
        """
        Cari user berdasarkan username
        
        Args:
            username: Username
            
        Returns:
            Dictionary atau None
        """
        query = f"SELECT * FROM {self.table} WHERE username = %s"
        return self.db.fetch_one(query, (username,))
    
    def verify_login(self, username, password):
        """
        Verifikasi login user
        
        Args:
            username: Username
            password: Password plain text
            
        Returns:
            Dictionary user jika berhasil, None jika gagal
        """
        user = self.find_by_username(username)
        
        if user:
            password_hash = self.hash_password(password)
            if user['password_hash'] == password_hash:
                # Hapus password_hash dari response
                del user['password_hash']
                return user
        
        return None
    
    def update(self, user_id, data):
        """
        Update data user
        
        Args:
            user_id: ID user
            data: Dictionary berisi data baru
            
        Returns:
            True jika berhasil, False jika gagal
        """
        # Jika ada password baru, hash dulu
        if 'password' in data and data['password']:
            password_hash = self.hash_password(data['password'])
            query = f"""
                UPDATE {self.table} 
                SET username = %s, password_hash = %s, role = %s
                WHERE user_id = %s
            """
            params = (data.get('username'), password_hash, data.get('role'), user_id)
        else:
            query = f"""
                UPDATE {self.table} 
                SET username = %s, role = %s
                WHERE user_id = %s
            """
            params = (data.get('username'), data.get('role'), user_id)
        
        return self.db.execute_query(query, params)
    
    def delete(self, user_id):
        """
        Hapus user
        
        Args:
            user_id: ID user
            
        Returns:
            True jika berhasil, False jika gagal
        """
        query = f"DELETE FROM {self.table} WHERE user_id = %s"
        return self.db.execute_query(query, (user_id,))
    
    def __del__(self):
        """Destructor - tutup koneksi database"""
        if hasattr(self, 'db'):
            self.db.disconnect()