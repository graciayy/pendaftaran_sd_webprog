# File ini membuat folder models menjadi package Python
# Biarkan kosong atau isi dengan:

from .database import Database
from .student import Student
from .registration import Registration
from .user import User

__all__ = ['Database', 'Student', 'Registration', 'User']