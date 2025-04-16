from lxml import etree
from dict_parse import product_group_dict_parse, products_dict_parse, storages_parse, products_in_storages_parse


def xml_to_dict(element):
    if len(element) == 0:  # Если элемент не имеет дочерних элементов
        if "Склад" in element.tag:
            #  print(f"find storage: {element.tag.split('}')[-1]}--- {element.attrib}")
            result_element = element.attrib
        else:
            result_element = element.text.strip() if (element.text and element.text.strip()) else None
        return result_element

    result = {}
    for child in element:
        tag = child.tag.split('}')[-1]
        child_dict = xml_to_dict(child)
        if tag not in result:
            result[tag] = child_dict
        else:
            if isinstance(result[tag], list):
                result[tag].append(child_dict)
            else:
                result[tag] = [result[tag], child_dict]
    return result


def parse_xml(file_path):
    with open(file_path, 'rb') as file:
        tree = etree.parse(file)
        root = tree.getroot()
        return {str(root.tag)[str(root.tag).find("}")+1:]: xml_to_dict(root)}


file_name = "../xml_base/13/webdata/import0_1.xml"
result_dict = parse_xml(file_name)

result_list_category = product_group_dict_parse(source=result_dict)
result_list_products = products_dict_parse(source=result_dict)

file_name = "../xml_base/13/webdata/offers0_1.xml"
result_dict = parse_xml(file_name)

result_storage_list = storages_parse(result_dict)
# print(result_dict)
result_products_in_storages = products_in_storages_parse(result_dict)

print(f"products in storages:")
for i in result_products_in_storages:
    print(f"{i}")
