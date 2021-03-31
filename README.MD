A simple media downloader and viewer for Twitter without account.
Currently, only download is supported via twint. 

---

If issue with twint (https://github.com/twintproject/twint/issues/384) :
```shell script
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

---

A file users.txt must be placed at the root of the project.
It contains usernames, one per line.