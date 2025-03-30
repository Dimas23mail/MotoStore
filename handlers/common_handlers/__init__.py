__all__ = ("router", )

from aiogram import Router

from .contact_handlers import router as contact_router

router = Router()

router.include_routers(contact_router, )