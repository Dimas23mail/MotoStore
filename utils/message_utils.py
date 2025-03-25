from aiogram.types.input_media_photo import InputMediaPhoto


def make_output_album(image: str, output_string: str) -> list:
    photos = image.split()
    media = []
    count = 0
    for i in photos:
        if count == 0:
            photo = InputMediaPhoto(type="photo",
                                    media=i,
                                    caption=output_string)
        else:
            photo = InputMediaPhoto(type="photo",
                                    media=i)
        media.append(photo)
        count += 1
    return media
