__all__ = ("router", )

from aiogram import Router

from .contact_handlers import router as contact_router
from .promo_handlers import router as promo_router

router = Router()

router.include_routers(contact_router,
                       promo_router,
                       )
