import twint
import json
import csv
import ast
import requests
import os
import youtube_dl
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="A simple tool to download videos and picture directly from Twitter, without an account.")
parser.add_argument("--path", dest="path", type=str, help="Specify the output path to download files", default="images")
parser.add_argument("--verbose", dest="verbose", type=bool, help="Specify if the program must outputs logs while downloading", nargs="?", default=False, const=True)

args = parser.parse_args()

# print(args)

try:
    Path(args.path).mkdir(exist_ok=False)
except FileExistsError: pass

try:
    Path("./errors").touch(exist_ok=False)
except FileExistsError: pass

try:
    Path("./config.json").touch(exist_ok=False)
    with open("config.json", mode="w", encoding="utf-8") as f:
        f.write("{}")
except FileExistsError: pass



def create_cache():
    users = []
    # users.txt : contains twitter usernames, one per line.
    with open("users.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            if line.startswith("# "): continue
            users.append(line)


    with open("config.json", encoding="utf-8") as f:
        data = json.load(f)

    tweets = []

    for user in users:
        try:
            Path(f"{args.path}/{user}").mkdir(exist_ok=False)
        except FileExistsError: pass
        print(user)

        tconfig = twint.Config()

        tconfig.Hide_output = not args.verbose
        tconfig.Username = user
        # If only static
        # tconfig.Images = True
        # If only videos
        # tconfig.Videos = True
        tconfig.Media = True
        tconfig.Store_csv = True
        tconfig.Output = f"cache_{user}.csv"
        if user in data and data[user]:
            tconfig.Since = data[user]

        try:
            twint.run.Search(tconfig)
        except Exception as e:
            # print(e)
            print("Issue with Twitter scrapping, retry later")

        try: 
            with open(f"cache_{user}.csv", encoding="utf-8") as f:
                cache = csv.reader(f)

                next(cache)
                c = next(cache)
                data[user] = c[3] + " " + c[4]
        except Exception as e:
            # print(e)
            print("Nothing found, creating blank csv.")
            Path(f"cache_{user}.csv").touch()

    with open("config.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f)

def download_cache(delete=True):
    users = []
    # users.txt : contains twitter usernames, one per line.
    with open("users.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            if line.startswith("# "): continue
            users.append(line)

    for user in users:
        print(user)
        if not Path(f"cache_{user}.csv").exists():
            print("Cache not found, skipping.")
            continue

        options = {
            'outtmpl': f"{args.path}/{user}/" + '%(id)s.%(ext)s'
        }

        correct = True

        with open(f"cache_{user}.csv", encoding="utf-8") as f:
            if len(f.read()) == 0:
                correct = False

        if not correct:
            print("Blank csv, skipping.")
            if delete: os.remove(f"cache_{user}.csv")
            continue
        
        total = 0
        with open(f"cache_{user}.csv", encoding="utf-8") as f:
            total = len(f.readlines()) - 1

        with open(f"cache_{user}.csv", encoding="utf-8") as f:

            cache = csv.reader(f)

            next(cache)

            current = 1
            for row in cache:
                photos = ast.literal_eval(row[14])

                photos_len = len(photos)
                for idx, photo in enumerate(photos):
                    print(f"{current}/{total} ", end="")
                    if photos_len > 1:
                        print(f"{idx + 1}/{photos_len} ", end="")
                    name = os.path.basename(photo)
                    if os.path.exists(f"{args.path}/{user}/{name}"):
                        if args.verbose: print(f"Skipping {photo}")
                        continue

                    if args.verbose: print(f"Downloading {photo}...")
                    r = requests.get(photo)

                    open(f"{args.path}/{user}/{name}", "wb").write(r.content)

                url, thumb = row[20], row[24]
                if "video_thumb" in thumb:
                    name = url.split("/")[-1]
                    if os.path.exists(f"{args.path}/{user}/{name}.mp4"):
                        if args.verbose: print(f"{current}/{total} Skipping video from {url}")
                        continue

                    print(f"{current}/{total} Downloading {url}...")
                    try:
                        with youtube_dl.YoutubeDL(options) as ydl:
                            ydl.download([url])
                    except Exception:
                        with open("errors", mode="a", encoding="utf-8") as f:
                            f.write(f"{user} {url}\n")
            
                current += 1

        if delete:
            os.remove(f"cache_{user}.csv")

create_cache()
download_cache()
