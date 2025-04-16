from pathlib import Path


def find_files_in_directory(root_directory: str = '../xml_base') -> tuple[list, list] | None:
    root_path = Path(root_directory)

    # Проверяем, что указанный путь является директорией
    if not root_path.is_dir():
        print(f"{root_directory} не является директорией.")
        return None
    file_list = []
    file_xml = []
    # Проходим по всем файлам и папкам в директории рекурсивно
    for file_name in root_path.rglob('*'):
        if file_name.is_file():
            relative_path = file_name.relative_to(root_path)
            if file_name.suffix == ".xml":
                file_xml.append(str(relative_path).replace("\\", "/"))
            elif file_name.suffix == ".jpg" or file_name.suffix == ".png":
                file_list.append(str(relative_path).replace("\\", "/"))
    return file_list, file_xml


def update_products_db() -> tuple | None:
    tuple_of_files = find_files_in_directory()
    if tuple_of_files:
        print(f"xml:\n{tuple_of_files[1]}\npict:\n{tuple_of_files[0]}")
        return tuple_of_files
    else:
        print("Directory is wrong!")
        return None


update_products_db()
