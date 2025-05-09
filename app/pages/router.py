from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/pages", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/students")
async def get_students_html(request: Request):
    return templates.TemplateResponse(
        name="students.html", context={"request": request}
    )
