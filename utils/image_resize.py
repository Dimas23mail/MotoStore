import os
from PIL import Image
import io


def reduce_image_size(input_path: str, output_path: str, target_size_kb: int = 300, max_attempts=10):
    """
    Уменьшает размер изображения до указанного размера в килобайтах.

    Args:
        input_path (str): Путь к исходному изображению
        output_path (str): Путь для сохранения уменьшенного изображения
        target_size_kb (int): Целевой размер в килобайтах
        max_attempts (int): Максимальное количество попыток изменения размера

    Returns:
        bool: True, если уменьшение успешно, False в противном случае
    """
    target_size_bytes = target_size_kb * 1024

    # Открываем изображение
    try:
        img = Image.open(input_path)

        # Получаем исходный формат
        img_format = img.format
        if not img_format:
            img_format = 'JPEG'  # Формат по умолчанию, если не удалось определить

        # Если формат PNG, конвертируем в RGB (если есть альфа-канал)
        if img_format == 'PNG' and img.mode == 'RGBA':
            # Создаем новый белый фон
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 - это альфа-канал
            img = background
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}")
        return False

    # Исходные размеры
    width, height = img.size

    # Проверяем исходный размер файла
    temp_buffer = io.BytesIO()
    img.save(temp_buffer, format=img_format)
    original_size = temp_buffer.tell()
    temp_buffer.close()

    print(f"Исходный размер: {original_size / 1024:.2f} кБ")

    # Если исходный размер уже меньше целевого, просто копируем файл
    if original_size <= target_size_bytes:
        img.save(output_path, format=img_format)
        print(f"Изображение уже меньше целевого размера, сохранено без изменений")
        return True

    # Начальное качество для JPEG
    quality = 100

    # Коэффициент масштабирования
    scale_factor = 1.0
    resized_img = None
    # Итеративно уменьшаем размер и/или качество
    for attempt in range(max_attempts):
        # Масштабируем изображение, если это не первая попытка
        if attempt > 0:
            scale_factor *= 0.9  # Уменьшаем на 10% с каждой попыткой
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            resized_img = img

        # Сохраняем во временный буфер для проверки размера
        temp_buffer = io.BytesIO()

        # Для JPEG используем параметр качества
        if img_format == 'JPEG':
            resized_img.save(temp_buffer, format='JPEG', quality=quality)
            quality = max(quality - 10, 10)  # Уменьшаем качество, но не ниже 10

        # Для PNG используем optimize и другие параметры
        elif img_format == 'PNG':
            resized_img.save(temp_buffer, format='PNG', optimize=True, compress_level=9)

        # Для других форматов просто сохраняем
        else:
            resized_img.save(temp_buffer, format=img_format)

        # Проверяем размер
        current_size = temp_buffer.tell()
        temp_buffer.close()

        print(
            f"Попытка {attempt + 1}: Размер = {current_size / 1024:.2f} кБ, Масштаб = {scale_factor:.2f}, "
            f"Качество = {quality}")

        # Если достигли целевого размера, сохраняем и завершаем
        if current_size <= target_size_bytes:
            # Сохраняем финальное изображение
            if img_format == 'JPEG':
                resized_img.save(output_path, format='JPEG', quality=quality + 10)  # Немного повышаем качество
            elif img_format == 'PNG':
                resized_img.save(output_path, format='PNG', optimize=True, compress_level=9)
            else:
                resized_img.save(output_path, format=img_format)

            final_size = os.path.getsize(output_path)
            print(f"Успешно! Финальный размер: {final_size / 1024:.2f} кБ")
            return True

    # Если после всех попыток не удалось достичь целевого размера,
    # сохраняем последнюю версию

    if img_format == 'JPEG':
        resized_img.save(output_path, format='JPEG', quality=10)
    elif img_format == 'PNG':
        resized_img.save(output_path, format='PNG', optimize=True, compress_level=9)
    else:
        resized_img.save(output_path, format=img_format)

    final_size = os.path.getsize(output_path)
    print(f"Не удалось достичь целевого размера. Финальный размер: {final_size / 1024:.2f} кБ")
    return False


# Пример использования
def resizer():
    input_file = "../xml_base/123.png"  # Путь к исходному файлу
    output_file = "../xml_base/123_reduced.png"  # Путь для сохранения уменьшенного файла
    target_kb = 510  # Целевой размер в килобайтах

    success = reduce_image_size(input_file, output_file, target_kb)

    if success:
        print(f"Изображение успешно уменьшено до {target_kb} кБ или меньше")
    else:
        print("Не удалось уменьшить изображение до целевого размера")


resizer()
