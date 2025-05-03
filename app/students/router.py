from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.database import async_session_maker
from app.students.models import Student
from app.students.dao import StudentDAO
from app.students.schemas import SStudent
from app.students.rb import RBStudent


router = APIRouter(
    prefix="/students",
    tags=["Обработка студентов"],
)


@router.get("/", summary="Список всех стуSнтов", response_model=list[SStudent])
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())
