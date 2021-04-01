import youtube_dl

with open("errors", encoding="utf-8") as f:
    errors = f.read().splitlines()

new_errors = []

for error in errors:
    user, url = error.split(' ')

    options = {
        'outtmpl': "images/" + user + "/" + '%(id)s.%(ext)s'
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception:
        new_errors.append(f"{user} {url}")

with open("errors", mode="w", encoding="utf-8") as f:
    for new_error in new_errors:
        f.write(f"{new_error}\n")
