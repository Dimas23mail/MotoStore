from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from storage import AdminToolsModule

from config import moto_db


router = Router()


@router.message(AdminToolsModule.adding_products, F.text)
async def adding_product_category_handler(message: types.Message, state: FSMContext):
    pass


@router.message(AdminToolsModule.adding_products)
async def wrong_adding_product_category_handler(message: types.Message, state: FSMContext):
    await message.answer(text="Error! Category product handler!")
