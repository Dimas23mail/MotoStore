__all__ = ("router", )

from aiogram import Router

from .base_handlers import router as base_router
#  from .common_handlers import router as client_routers
from .admin_handlers import router as admin_routers

router = Router()

router.include_routers(
    base_router,
    #  client_routers,
    admin_routers,
                       )
