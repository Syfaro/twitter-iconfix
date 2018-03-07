from typing import Union

from base64 import b64encode
from io import BytesIO
from PIL import Image
from webbrowser import open
import sys
from birdy.twitter import UserClient

from twitter_iconfix import process_image

def _show_trans_pixels(image: Union[BytesIO, str]) -> None:
    img = Image.open(image)
    data = img.load()

    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = data[x, y]
            if pixel[3] != 255:
                print(x, y, pixel)

def _upload_to_twitter(image: Union[BytesIO, str]) -> None:
    client = UserClient('ygIfUqHEkFr57AsVgnI3ik0xw',
                        'ckY4irPjw3p9PnqHVtR9wqpEzJLSLPRhBpYZjPCN2XXiJATFp2')
    verifier = client.get_authorize_token('oob')
    open(verifier.auth_url)

    print('PIN: ', end='')
    pin = input()

    client = UserClient('ygIfUqHEkFr57AsVgnI3ik0xw',
                        'ckY4irPjw3p9PnqHVtR9wqpEzJLSLPRhBpYZjPCN2XXiJATFp2',
                        verifier.oauth_token,
                        verifier.oauth_token_secret)

    client.get_access_token(pin.strip())
    encoded = b64encode(image.getvalue())
    client.api.account.update_profile_image.post(image=encoded)

def main():
    args = len(sys.argv)
    if args < 2:
        print('Must include filename to twitterfix.')
        sys.exit(2)

    fileName = sys.argv[1]
    image = process_image(fileName)
    _show_trans_pixels(image)

    if args == 3:
        with open(sys.argv[2], 'wb') as f:
            f.write(image.read())
    else:
        _upload_to_twitter(image)

if __name__ == '__main__':
    main()


