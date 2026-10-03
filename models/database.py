import mysql.connector
from mysql.connector import Error
from config import Config


class Database:
    """Class untuk koneksi dan operasi database"""
    
    def __init__(self):
        """Constructor - inisialisasi properti"""
        self.host = Config.DB_HOST
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.database = Config.DB_NAME
        self.connection = None
    
    def connect(self):
        """Membuat koneksi ke database MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print("✅ Database connected successfully")
                return self.connection
                
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query, params=None):
        """
        Eksekusi query (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query string
            params: Tuple parameter untuk query
            
        Returns:
            last_insert_id jika INSERT, True jika berhasil, False jika gagal
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            
            # Return last insert id untuk INSERT query
            if cursor.lastrowid:
                return cursor.lastrowid
            
            return True
            
        except Error as e:
            print(f"❌ Error executing query: {e}")
            self.connection.rollback()
            return False
            
        finally:
            if cursor:
                cursor.close()
    
    def fetch_all(self, query, params=None):
        """
        Mengambil semua data (SELECT)
        
        Args:
            query: SQL query string
            params: Tuple parameter untuk query
            
        Returns:
            List of dictionaries
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            return result
            
        except Error as e:
            print(f"❌ Error fetching data: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
    
    def fetch_one(self, query, params=None):
        """
        Mengambil satu data (SELECT)
        
        Args:
            query: SQL query string
            params: Tuple parameter untuk query
            
        Returns:
            Dictionary atau None
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchone()
            return result
            
        except Error as e:
            print(f"❌ Error fetching data: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()
    
    def get_connection_info(self):
        """Mendapatkan informasi koneksi database"""
        if self.connection and self.connection.is_connected():
            db_info = self.connection.get_server_info()
            return {
                'server_version': db_info,
                'database': self.database,
                'host': self.host,
                'user': self.user
            }
        return None