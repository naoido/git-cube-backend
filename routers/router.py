from fastapi import APIRouter

from routers import user, cube, memo, todo

router = APIRouter()

router.include_router(user.user_router, prefix="/user")
router.include_router(cube.cube_router, prefix="/cube")
router.include_router(memo.memo_router, prefix="/memo")
router.include_router(todo.todo_router, prefix="/todo")
