from app.students.models import Student, Major
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select

class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            # Первый запрос для получения информации о студенте
            query_student = select(cls.model).filter_by(id=student_id)
            result_student = await session.execute(query_student)
            student_info = result_student.scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not student_info:
                return None

            # Второй запрос для получения информации о специальности
            query_major = select(Major).filter_by(id=student_info.major_id)
            result_major = await session.execute(query_major)
            major_info = result_major.scalar_one()

            student_data = student_info.to_dict()
            student_data['major'] = major_info.major_name

            return student_data


from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.students.models import Student

class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
