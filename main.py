import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from starlette.responses import RedirectResponse
import httpx

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router, prefix="/api")

github_client_id = 'Ov23litv1YfmKcW4TyaT'
github_client_secret = "ee65c1971e77279767e44b7cd503ca260e19f0c6"

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code = 302)

@app.get("/github-code")
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
    return response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)