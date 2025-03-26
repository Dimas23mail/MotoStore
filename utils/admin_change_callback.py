from aiogram.filters.callback_data import CallbackData


class StorageForDeletingCategory(CallbackData, prefix="cb"):
    category_id: int
    reaction: str


class StorageForChangePlaceData(CallbackData, prefix="cb"):
    place_id: int
    user_id: int
    reaction: str


class StorageForChangeImageData(CallbackData, prefix="cb"):
    place_id: int
    photo_id: int
    reaction: str
