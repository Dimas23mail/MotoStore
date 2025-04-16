from aiogram.filters.callback_data import CallbackData


class StorageForDeletingCategory(CallbackData, prefix="cb"):
    category_id: int
    reaction: str


class StorageForDeletingContacts(CallbackData, prefix="cb"):
    contact_id: int
    reaction: str


class StorageForChangingContacts(CallbackData, prefix="cb"):
    contact_id: int
    reaction: str


class StorageForChangePlaceData(CallbackData, prefix="cb"):
    place_id: int
    user_id: int
    reaction: str


class StorageForChangeImageData(CallbackData, prefix="cb"):
    place_id: int
    photo_id: int
    reaction: str


class StorageForAddingPromoProducts(CallbackData, prefix="cb"):
    product_id: int
    reaction: str
