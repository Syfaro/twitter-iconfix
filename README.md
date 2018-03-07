# twitter-iconfix

Utility and library to fix Twitter icons (and other images).

Installs a binary twitter_iconfix you can use from the command line.

```bash
twitter_iconfix path/to/image.png # automatically uploads
twitter_iconfix path/to/image.png output.png
```

Also available as a library with `process_image`.

Uses a `BytesIO` or `str` to load, optionally writes to file with `writeToFile` or doesn't resize for icons if `icon` is False.
