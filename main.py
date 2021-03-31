import twint
import json
import csv
import ast
import requests
import os
import youtube_dl
from pathlib import Path


try:
    Path("./images").mkdir(exist_ok=False)
except FileExistsError: pass

try:
    Path("./config.json").touch(exist_ok=False)
    with open("config.json", mode="w", encoding="utf-8") as f:
        f.write("{}")
except FileExistsError: pass

# users.txt : contains twitter usernames, one per line.
with open("users.txt", encoding="utf-8") as f:
    users = f.read().splitlines()

with open("config.json", encoding="utf-8") as f:
    data = json.load(f)

tweets = []

for user in users:
    try:
        Path("./images/" + user).mkdir(exist_ok=False)
    except FileExistsError: pass
    print(user)

    tconfig = twint.Config()

    tconfig.Hide_output = True
    tconfig.Username = user
    # If only images
    # tconfig.Images = True
    # If only videos
    # tconfig.Videos = True
    tconfig.Media = True
    tconfig.Store_csv = True
    tconfig.Output = "cache_" + user + ".csv"
    if user in data and data[user]:
        tconfig.Since = data[user]

    twint.run.Search(tconfig)

    with open("cache_" + user + ".csv", encoding="utf-8") as f:
        cache = csv.reader(f)

        next(cache)
        c = next(cache)
        data[user] = c[3] + " " + c[4]

with open("config.json", mode="w", encoding="utf-8") as f:
    json.dump(data, f)


for user in users:
    print(user)

    options = {
        'outtmpl': "images/" + user + "/" + '%(id)s.%(ext)s'
    }

    with open("cache_" + user + ".csv", encoding="utf-8") as f:
        cache = csv.reader(f)

        next(cache)

        for row in cache:
            photos = ast.literal_eval(row[14])

            for photo in photos:
                name = os.path.basename(photo)
                if os.path.exists("images/" + user + "/" + name):
                    print("Skipping " + photo)
                    continue

                print("Downloading " + photo + "...")
                r = requests.get(photo)

                open("images/" + user + "/" + name, "wb").write(r.content)

            url, thumb = row[20], row[24]
            if "ext_tw_video_thumb" in thumb:
                with youtube_dl.YoutubeDL(options) as ydl:
                    ydl.download([url])

    os.remove("cache_" + user + ".csv")
