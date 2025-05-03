from app.students.models import Student
from app.dao.base import BaseDAO

class StudentDAO(BaseDAO):
    model = Student
