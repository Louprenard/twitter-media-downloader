import youtube_dl
import os
import argparse

parser = argparse.ArgumentParser(description="A simple tool to download videos and picture directly from Twitter, without an account.")
parser.add_argument("--path", dest="path", type=str, help="Specify the output path to download files", default="images")
parser.add_argument("--verbose", dest="verbose", type=bool, help="Specify if the program must outputs logs while downloading", nargs="?", default=False, const=True)

args = parser.parse_args()

with open("errors", encoding="utf-8") as f:
    errors = f.read().splitlines()

new_errors = []

total = len(errors)
for idx, error in enumerate(errors):
    user, url = error.split(' ')

    options = {
        'outtmpl': f"{args.path}/{user}/" + '%(id)s.%(ext)s'
    }

    name = url.split("/")[-1]
    if os.path.exists(f"{args.path}/{user}/{name}.mp4"):
        if args.verbose: print(f"{idx + 1}/{total} Skipping video from {url}")
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
