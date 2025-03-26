__all__ = ("router", )

from aiogram import Router

from .adding_category_handlers import router as adding_category_router
from .change_category_menu_handlers import router as change_category_menu_router
from .deleting_category_handlers import router as deleting_category_router


router = Router()

router.include_routers(change_category_menu_router,
                       adding_category_router,
                       deleting_category_router
                       )
