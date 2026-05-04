from fastapi import Request, HTTPException


def require_auth(request: Request):
    if not request.session.get("authed"):
        raise HTTPException(
            status_code=302, headers={"Location": "/login"}
        )
    return True


def require_admin(request: Request):
    if not request.session.get("is_admin"):
        raise HTTPException(403, "需要管理员权限")
    return True
