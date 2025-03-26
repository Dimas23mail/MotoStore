__all__ = ("router", )

from aiogram import Router

from .change_contact_menu_handlers import router as adding_contact_router

router = Router()

router.include_routers(
    adding_contact_router,
)
