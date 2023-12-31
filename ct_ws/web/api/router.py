from fastapi.routing import APIRouter

from ct_ws.web.api import meal, monitoring, user

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(
    meal.router,
    prefix="/meal",
    tags=["meal"],
)
api_router.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)
