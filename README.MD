A simple media downloader for Twitter without account.

---

If issue with twint (https://github.com/twintproject/twint/issues/384) :
```shell script
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

---

A file called `users.txt` must be placed at the root of the project.
It contains Twitter usernames, one per line, without the @.

Notes
* Duplicates can occur due to the renaming of the image by Twitter.

If any error occurs when downloading a video, it's reported in the `errors` file.
`downloader_errors.py` is a script that will try to download failed urls via the `errors` file.
Due to youtube_dl and website limitations, you may have to run multiple times the downloader_errors
script in order to get all videos.
