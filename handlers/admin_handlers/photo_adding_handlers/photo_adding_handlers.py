from aiogram import F, types
from aiogram import Router

from config import moto_db


router = Router(name=__name__)


@router.channel_post(F.photo)
async def get_photo_channel_message(message: types.Message):
    print(f"В канале получены фото: {message.caption}")
    caption = message.caption
    if caption.split()[0].isdigit():
        caption = int(caption.split()[0])
    photo_url = message.photo[-1].file_id
    photo_url_data = (photo_url, caption)

    async with moto_db:
        await moto_db.update_photo_url_products_db(photo_url_data=photo_url_data)
    #  print(f"mark in adm_hand = {mark}")

