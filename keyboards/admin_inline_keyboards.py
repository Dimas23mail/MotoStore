from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import (StorageForChangePlaceData, StorageForChangeImageData, StorageForDeletingCategory,
                   StorageForAddingPromoProducts)


def action_with_record_ikb(record_id: int, reaction: str, button_text: str = "Удалить") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    cb_data = StorageForDeletingCategory(category_id=record_id, reaction=reaction)
    builder.button(
        text=button_text,
        callback_data=cb_data.pack()
    )
    builder.adjust(1, )
    return builder.as_markup()


def build_change_record_kb(place_id: int, user_id: int, reaction: str) -> InlineKeyboardMarkup:
    change_button_text = "Изменить информацию..."
    builder = InlineKeyboardBuilder()

    cb_data = StorageForChangePlaceData(place_id=place_id, user_id=user_id, reaction=reaction)
    builder.button(
        text=change_button_text,
        callback_data=cb_data.pack()
    )
    builder.adjust(1,)
    return builder.as_markup()


def build_delete_photo_record_kb(place_id: int, photo_id: int, reaction: str, text: str = "Удалить фото") \
        -> InlineKeyboardMarkup:
    del_button_text = text
    builder = InlineKeyboardBuilder()

    cb_data = StorageForChangeImageData(place_id=place_id, photo_id=photo_id, reaction=reaction)
    builder.button(
        text=del_button_text,
        callback_data=cb_data.pack()
    )
    builder.adjust(1,)
    return builder.as_markup()


def build_choice_product_for_promo(product_id: int, reaction: str, text: str = "Добавить товар") \
        -> InlineKeyboardMarkup:
    add_button_text = text
    builder = InlineKeyboardBuilder()

    cb_data = StorageForAddingPromoProducts(product_id=product_id, reaction=reaction)
    builder.button(
        text=add_button_text,
        callback_data=cb_data.pack()
    )
    builder.adjust(1, )
    return builder.as_markup()
