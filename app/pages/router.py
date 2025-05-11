from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.students.router import get_all_students_for_front
from app.students.router import get_student_by_id


router = APIRouter(prefix="/pages", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")

@router.get('/register')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='register_form.html', context={'request': request})


@router.get('/login')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='login_form.html', context={'request': request})


@router.get("/students")
async def get_students_html(
    request: Request, students=Depends(get_all_students_for_front)
):
    return templates.TemplateResponse(
        name="students.html",
        context={
            "request": request,
            "students": students,
        },
    )


@router.get("/students/{student_id}")
async def get_students_html(request: Request, student=Depends(get_student_by_id)):
    return templates.TemplateResponse(
        name="student.html", context={"request": request, "student": student}
    )
