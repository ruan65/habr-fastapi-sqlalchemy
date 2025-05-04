from app.students.models import Student, Major
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import joinedload

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
            # Запрос для получения информации о студенте вместе с информацией о факультете
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name
            return student_data
