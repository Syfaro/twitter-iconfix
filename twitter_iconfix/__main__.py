"""Command line utility version to upload icons to Twitter as PNG."""

from base64 import b64encode
from io import BytesIO
from PIL import Image
from webbrowser import open
import sys
from birdy.twitter import UserClient

from twitter_iconfix import process_image

CONSUMER_KEY = 'ygIfUqHEkFr57AsVgnI3ik0xw'
CONSUMER_SECRET = 'ckY4irPjw3p9PnqHVtR9wqpEzJLSLPRhBpYZjPCN2XXiJATFp2'  # not ideal to include, but makes things easier


def _show_trans_pixels(image: BytesIO) -> None:
    """Print out all the transparent pixels in an image.

    :param image: the image to evaluate
    """
    img = Image.open(image)  # open image
    data = img.load()  # get pixels

    width, height = img.size  # calculate size to iterate through

    for y in range(height):
        for x in range(width):
            pixel = data[x, y]
            if pixel[3] != 255:  # if we have transparency
                print(x, y, pixel)  # x, y pos of the pixel and its value


def _upload_to_twitter(image: BytesIO) -> None:
    """Upload an icon to Twitter.

    :param image: the image to upload
    """
    client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
    verifier = client.get_authorize_token('oob')  # get auth URL
    open(verifier.auth_url)  # open auth URL so user can get PIN

    pin = input('PIN: ')  # get PIN from user

    client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                        verifier.oauth_token, verifier.oauth_token_secret)

    client.get_access_token(pin.strip())  # authorize with Twitter, after making sure no stray characters got in
    encoded = b64encode(image.getvalue())  # read bytes from image and encode for Twitter
    client.api.account.update_profile_image.post(image=encoded)  # upload the icon


def main():
    """Simple command line tool to upload an icon to Twitter keeping it as a PNG."""
    args = len(sys.argv)
    if args < 2:
        print('Must include filename to twitterfix.')
        sys.exit(2)

    file_name = sys.argv[1]  # get the name of the file to open
    image = process_image(file_name)  # add the transparent pixel
    _show_trans_pixels(image)  # show all transparent pixels (for debug reasons)

    if args == 3:  # if we passed a third argument we want to just save it as a file
        with open(sys.argv[2], 'wb') as f:
            f.write(image.read())
    else:  # else we want to upload it directly to Twitter
        _upload_to_twitter(image)


if __name__ == '__main__':
    main()  # if script is directly executed, run the main function
