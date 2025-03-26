__all__ = ("router", )

from aiogram import Router

from .change_product_handlers import router as change_product_router
from .main_admin_handlers import router as main_router
from .change_contacts_handlers import router as change_contact_router

router = Router()

router.include_routers(main_router,
                       change_product_router,
                       change_contact_router
                       )
