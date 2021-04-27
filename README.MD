A simple media downloader and viewer for Twitter without account.
Currently, only download is supported via twint.
A basic (and very naive) viewer is available, but it is not optimized.

---

If issue with twint (https://github.com/twintproject/twint/issues/384) :
```shell script
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

---

A file users.txt must be placed at the root of the project.
It contains usernames, one per line.

Notes
* Issues may occur with youtube-dl, have to see if something can be done.
* Duplicates can occur due to the renaming of the image by Twitter.

If any error occurs when downloading a video, it's reported in the `errors` file.
`downloader_errors.py` is a script that will try to download failed urls via the `errors` file.
Due to youtube_dl and website limitations, you may have to run multiple times the downloader_errors
script in order to get all videos.
