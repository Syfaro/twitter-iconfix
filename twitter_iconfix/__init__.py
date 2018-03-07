from typing import Union

from io import BytesIO
from PIL import Image

def process_image(image: Union[BytesIO, str], writeToFile=None) -> Union[BytesIO, None]:
    img = Image.open(image)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    data = img.load()

    width, height = img.size

    if width < 2 or height < 2:
        print('Invalid image size.')

    if width > 400 or height > 400:
        img.thumbnail((400, 400), Image.ANTIALIAS)
        data = img.load()

    width, height = img.size

    pixel = data[width - 1, height - 1]
    data[width - 1, height - 1] = (pixel[0], pixel[1], pixel[2], pixel[3] // 3)

    if writeToFile:
        img.save(writeToFile, 'PNG')
        return

    out = BytesIO()
    img.save(out, 'PNG')

    return out
