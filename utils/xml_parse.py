from lxml import etree


def xml_to_dict(element):
    if len(element) == 0:  # Если элемент не имеет дочерних элементов
        if "Склад" in element.tag:
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
        return {root.tag.split("}")[-1]: xml_to_dict(root)}
