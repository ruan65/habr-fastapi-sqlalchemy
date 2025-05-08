from app.students.models import Student
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select, insert, delete, update, event
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.majors.models import Major  # Also need to import Major model


class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.major))
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.major))
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            # Запрос для получения информации о студенте вместе с информацией о факультете
            query = (
                select(cls.model)
                .options(joinedload(cls.model.major))
                .filter_by(id=student_id)
            )
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data["major"] = student_info.major.major_name
            return student_data

    @event.listens_for(Student, "after_insert")
    def receive_after_insert(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students + 1)
        )

    @event.listens_for(Student, "after_delete")
    def receive_after_delete(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students - 1)
        )

    @classmethod
    async def add_student(cls, **student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id

    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()

                if not student_to_delete:
                    return None

                # Удаляем студента
                await session.execute(delete(cls.model).filter_by(id=student_id))

                await session.commit()
                return student_id
