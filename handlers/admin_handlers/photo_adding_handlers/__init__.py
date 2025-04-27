__all__ = ("router", )

from aiogram import Router

from .photo_adding_handlers import router as photo_adding_router

router = Router()

router.include_router(photo_adding_router)
