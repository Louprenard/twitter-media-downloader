import twint
import json
import csv
import ast
import requests
import os
import youtube_dl
import sys
from pathlib import Path

VERBOSE = False

if "-v" in sys.argv:
    VERBOSE = True

try:
    Path("static").mkdir(exist_ok=False)
except FileExistsError: pass

try:
    Path("./errors").touch(exist_ok=False)
except FileExistsError: pass

try:
    Path("./config.json").touch(exist_ok=False)
    with open("config.json", mode="w", encoding="utf-8") as f:
        f.write("{}")
except FileExistsError: pass

# users.txt : contains twitter usernames, one per line.
users = []
with open("users.txt", encoding="utf-8") as f:
    for line in f.read().splitlines():
        if line.startswith("# "): continue
        users.append(line)


with open("config.json", encoding="utf-8") as f:
    data = json.load(f)

tweets = []

for user in users:
    try:
        Path("./static/" + user).mkdir(exist_ok=False)
    except FileExistsError: pass
    print(user)

    tconfig = twint.Config()

    tconfig.Hide_output = not VERBOSE
    tconfig.Username = user
    # If only static
    # tconfig.Images = True
    # If only videos
    # tconfig.Videos = True
    tconfig.Media = True
    tconfig.Store_csv = True
    tconfig.Output = "cache_" + user + ".csv"
    if user in data and data[user]:
        tconfig.Since = data[user]

    try:
        twint.run.Search(tconfig)
    except Exception as e:
        # print(e)
        print("Issue with Twitter scrapping, retry later")

    try: 
        with open("cache_" + user + ".csv", encoding="utf-8") as f:
            cache = csv.reader(f)

            next(cache)
            c = next(cache)
            data[user] = c[3] + " " + c[4]
    except Exception as e:
        # print(e)
        print("Nothing found, creating blank csv.")
        Path("cache_" + user + ".csv").touch()

with open("config.json", mode="w", encoding="utf-8") as f:
    json.dump(data, f)


for user in users:
    print(user)

    options = {
        'outtmpl': "static/" + user + "/" + '%(id)s.%(ext)s'
    }

    correct = True

    with open("cache_" + user + ".csv", encoding="utf-8") as f:
        if len(f.read()) == 0:
            correct = False

    if not correct:
        print("Blank csv, skipping.")
        os.remove("cache_" + user + ".csv")
        continue
    
    with open("cache_" + user + ".csv", encoding="utf-8") as f:

        cache = csv.reader(f)

        next(cache)

        for row in cache:
            photos = ast.literal_eval(row[14])

            for photo in photos:
                name = os.path.basename(photo)
                if os.path.exists("static/" + user + "/" + name):
                    if VERBOSE: print("Skipping " + photo)
                    continue

                if VERBOSE: print("Downloading " + photo + "...")
                r = requests.get(photo)

                open("static/" + user + "/" + name, "wb").write(r.content)

            url, thumb = row[20], row[24]
            if "video_thumb" in thumb:
                try:
                    with youtube_dl.YoutubeDL(options) as ydl:
                        ydl.download([url])
                except Exception:
                    with open("errors", mode="a", encoding="utf-8") as f:
                        f.write(f"{user} {url}\n")

    os.remove("cache_" + user + ".csv")
