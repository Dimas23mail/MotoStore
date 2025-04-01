__all__ = ("router")

from aiogram import Router

from .change_promo_menu_handlers import router as menu_promo_router
from .adding_promo_handlers import router as adding_promo_router

router = Router()

router.include_routers(menu_promo_router,
                       adding_promo_router,
                       )
