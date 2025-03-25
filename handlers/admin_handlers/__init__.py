__all__ = ("router", )

from aiogram import Router

from .change_category_handlers import router as change_category_router
from .change_product_handlers import router as change_product_router
from .main_admin_handlers import router as main_router

router = Router()

router.include_routers(main_router,
                       change_category_router,
                       change_product_router, )
