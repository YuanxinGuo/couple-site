from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, password: str = Form(...)):
    if password == settings.site_password:
        request.session["authed"] = True
        return RedirectResponse("/", status_code=303)
    if password == settings.site_password + "_admin":
        request.session["authed"] = True
        request.session["is_admin"] = True
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse("login.html", {
        "request": request, "error": "暗号不对哦"
    })


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
