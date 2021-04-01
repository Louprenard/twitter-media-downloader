import youtube_dl

with open("errors", encoding="utf-8") as f:
    errors = f.read().splitlines()

for error in errors:
    user, url = error.split(' ')

    options = {
        'outtmpl': "images/" + user + "/" + '%(id)s.%(ext)s'
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

