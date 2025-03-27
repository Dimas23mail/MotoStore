__all__ = ("router", )

from aiogram import Router

from .change_contact_menu_handlers import router as changing_contact_menu_router
from .adding_contact_handlers import router as adding_contact_router
from .deleting_contact_handlers import router as deleting_contact_router

router = Router()

router.include_routers(
    changing_contact_menu_router,
    adding_contact_router,
    deleting_contact_router
)
