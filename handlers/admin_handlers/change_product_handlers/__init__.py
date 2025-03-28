__all__ = ("router", )

from aiogram import Router

from .adding_products_handlers import router as adding_products_router
from .change_products_menu_handlers import router as change_products_menu_router
from .common_change_products_handlers import router as common_change_products_router
from .change_category_handlers import router as change_category_router
from .change_spare_types_handlers import router as change_spare_types_router

router = Router()

router.include_routers(common_change_products_router,
                       adding_products_router,
                       change_products_menu_router,
                       change_category_router,
                       change_spare_types_router
                       )
