from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.students.router import get_all_students_for_front


router = APIRouter(prefix="/pages", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/students")
async def get_students_html(request: Request, students=Depends(get_all_students_for_front)):
    return templates.TemplateResponse(
        name="students.html",
        context={
            "request": request,
            "students": students,
        },
    )
