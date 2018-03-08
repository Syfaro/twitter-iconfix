"""Simple way to add a transparent pixel to an icon or other picture so Twitter does not resize it."""

from typing import Union

from io import BytesIO
from PIL import Image


class InvalidImageException(Exception):
    """Exception raised when the image provided is invalid."""
    def __init__(self, message: str):
        """Create a new InvalidImageException.

        :param message: message to include in the exception
        """
        self.message = message


def process_image(image: Union[BytesIO, str], write_to_file: str=None, icon=True) -> Union[BytesIO, None]:
    """Take in an image and add a small partially transparent pixel to prevent Twitter from converting it to a JPEG.

    :param image: the image to use, either a BytesIO (or really anything PIL can open), or a string to the image path
    :param write_to_file: if the output should be written to a file, and if so, what the name of the file is
    :param icon: if the output should be resized for an icon (Twitter will resize anything greater than 400x400).
    :return: the BytesIO if not writing to a file, else None
    """
    img = Image.open(image)
    if img.mode != 'RGBA':  # don't convert if it already is
        img = img.convert('RGBA')  # need channel for transparency

    width, height = img.size  # find resolution of image, to ensure it's big enough and to find pixels to use

    if width < 2 or height < 2:  # check if image is too small to be worthwhile
        raise InvalidImageException('Image is too small')

    if icon and (width > 400 or height > 400):  # if we want to resize to max image resolution and we need to
        img.thumbnail((400, 400), Image.ANTIALIAS)
        width, height = img.size  # recalculate image size

    data = img.load()  # get pixels

    pixel = data[width - 1, height - 1]  # get the pixel to modify
    data[width - 1, height - 1] = (pixel[0], pixel[1], pixel[2], pixel[3] // 3)  # only a bit of transparency required

    if write_to_file:  # if we need to save it to a file, save it as a PNG
        img.save(write_to_file, 'PNG')
    else:  # if we want to get the bytes of the image for further use, still 'saving' it as a PNG
        out = BytesIO()
        img.save(out, 'PNG')

        return out
