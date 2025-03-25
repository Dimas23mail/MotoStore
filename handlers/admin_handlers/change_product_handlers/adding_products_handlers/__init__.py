__all__ = ("router", )

from aiogram import Router

from .adding_products_handlers import router as adding_product_router

router = Router()

router.include_routers(adding_product_router, )
