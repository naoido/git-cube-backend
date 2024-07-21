from fastapi import APIRouter
import requests
from routers import user, cube, memo, todo
from starlette.responses import RedirectResponse
import httpx


router = APIRouter()

github_client_id = 'Ov23litv1YfmKcW4TyaT'
github_client_secret = "ee65c1971e77279767e44b7cd503ca260e19f0c6"

router.include_router(user.user_router, prefix="/user")
router.include_router(cube.cube_router, prefix="/cube")
router.include_router(memo.memo_router, prefix="/memo")
router.include_router(todo.todo_router, prefix="/todo")

@router.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code = 302)

@router.get("/github-code")
async def github_code(code: str):
    params = {
        'client_id' : github_client_id,
        'client_secret' : github_client_secret,
        'code' : code
    }
    headers = {'Accept' : 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers = headers)
    response_json = response.json()
    access_token = response_json['access_token']
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization':f'Bearer {access_token}'})
        response = await client.get('https://api.github.com/user', headers=headers)
    text = response.json()
    github_id = text["login"]
    user_id = text["id"]
    url = text["url"]
    requests.post(f"http://localhost:8000/api/user?github_id={github_id}&user_id={user_id}&repo_url={url}")
    requests.post(f"http://localhost:8000/api/user/sessions?user_id={user_id}")
    return RedirectResponse("http://localhost:3000/")
 