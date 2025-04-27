from dataclasses import dataclass


@dataclass
class ValidateFieldsForDb:
    category_id: int = 0
    sub_category_id: int = 0
    title: str = ''
    brand: str = ''
    description: str = ''
    image_url: str = ''
    created_at: str = ''
    id_1c: str = ''
    image_1c: str = ''
    id_type_1c: str = ''

    def convert_class_to_tuple_for_update(self) -> tuple:
        return (self.category_id, self.sub_category_id, self.title, self.brand, self.description,
                self.created_at, self.image_1c, self.id_type_1c, self.id_1c)


@dataclass
class StoragesFields:
    id_1c: str = ""
    title: str = ""
    address: str = ""

    def convert_class_to_tuple_for_update(self) -> tuple:
        return self.title, self.address, self.id_1c


@dataclass
class BaseProductsForStorages:
    counts: int = 0
    costs_for_pce: float = 0.0
    date_of_change: str = ""


@dataclass
class ProductsForStoragesDB(BaseProductsForStorages):
    id_products: int = 0
    storage_id: int = 0

    def convert_class_to_tuple_for_update(self) -> tuple:
        return self.counts, self.costs_for_pce, self.date_of_change, self.id_products, self.storage_id


@dataclass
class ProductsForStoragesCompare(BaseProductsForStorages):
    key: str = ""
