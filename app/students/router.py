from fastapi import APIRouter
from sqlalchemy import select
from app.database import async_session_maker
from app.students.models import Student

router = APIRouter(
    prefix="/students",
    tags=["Работа со студентами"],
)


@router.get("/", summary="Получить всех студентов")
async def get_all_students():
    async with async_session_maker() as session:
        query = select(Student)
        result = await session.execute(query)
        return result.scalars().all()
