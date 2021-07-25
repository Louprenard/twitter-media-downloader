import youtube_dl
import os
import sys

VERBOSE = False

if "-v" in sys.argv:
    VERBOSE = True

with open("errors", encoding="utf-8") as f:
    errors = f.read().splitlines()

new_errors = []

total = len(errors)
for idx, error in enumerate(errors):
    user, url = error.split(' ')

    options = {
        'outtmpl': f"images/{user}/" + '%(id)s.%(ext)s'
    }

    name = url.split("/")[-1]
    if os.path.exists(f"images/{user}/{name}.mp4"):
        if VERBOSE: print(f"{idx + 1}/{total} Skipping video from {url}")
        continue

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            print(f"{idx + 1}/{total}")
            ydl.download([url])
    except Exception:
        new_errors.append(f"{user} {url}")

with open("errors", mode="w", encoding="utf-8") as f:
    for new_error in new_errors:
        f.write(f"{new_error}\n")
