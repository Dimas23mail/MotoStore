__all__ = ("router", )

from aiogram import Router

from .adding_spare_types_handlers import router as adding_spare_types_router
from .change_spare_types_menu_handlers import router as change_spare_types_menu_router
from .deleting_spare_types_handlers import router as deleting_spare_types_router


router = Router()

router.include_routers(change_spare_types_menu_router,
                       adding_spare_types_router,
                       deleting_spare_types_router
                       )
