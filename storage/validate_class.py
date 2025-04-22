from dataclasses import dataclass, fields


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
        return (self.category_id, self.sub_category_id, self.title, self.brand, self.description, self.image_url,
                self.created_at, self.image_1c, self.id_type_1c, self.id_1c)
"""
    def __eq__(self, other: "ValidateFieldsForDb"):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Можно сравнивать только с объектами класса {self.__class__.__name__}")

        if other.__class__ is self.__class__:
            return ((self.category_id, self.sub_category_id, self.title, self.brand, self.description, self.image_url,
                    self.id_1c, self.image_1c, self.id_type_1c) ==
                    (other.category_id, other.sub_category_id, other.title, other.brand, other.description,
                     other.image_url, other.id_1c, other.image_1c, other.id_type_1c))
        return NotImplemented

    def __hash__(self):
        return hash((self.category_id, self.sub_category_id, self.title, self.brand, self.description, self.image_url,
                    self.id_1c, self.image_1c, self.id_type_1c))

    def get_different_fields(self, other: "ValidateFieldsForDb"):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Можно сравнивать только с объектами класса {self.__class__.__name__}")

        different_fields = []
        for field in fields(self):
            field_name = field.name

            if field_name != "created_at" and getattr(self, field_name) != getattr(other, field_name):
                different_fields.append(field_name)

        return different_fields
"""
