import twint
import json
import csv
import ast
import requests
import os

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
    tconfig.Images = True
    tconfig.Media = True
    tconfig.Store_csv = True
    tconfig.Output = "cache_" + user + ".csv"
    if user in data and data[user]:
        print(data[user])
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
    with open("cache_" + user + ".csv", encoding="utf-8") as f:
        cache = csv.reader(f)

        next(cache)

        for row in cache:
            urls = ast.literal_eval(row[13])
            photos = ast.literal_eval(row[14])

            for photo in photos:
                print("Downloading " + photo + "...")
                r = requests.get(photo)
                name = os.path.basename(photo)

                open("images/" + user + "/" + name, "wb").write(r.content)

    os.remove("cache_" + user + ".csv")