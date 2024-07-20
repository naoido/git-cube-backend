from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)