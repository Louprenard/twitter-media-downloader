import os
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/<profile>")
def list_images(profile):
    if profile not in os.listdir(app.static_folder):
        return redirect("/", code=302)
    files = os.listdir(app.static_folder + "/" + profile)
    images = [f for f in files if f.lower().endswith(".jpg") or f.lower().endswith(".png") or f.lower().endswith("jpeg")]
    videos = [f for f in files if f.lower().endswith(".mp4")]
    return render_template("gallery.html", profile=profile, images=images, videos=videos)


@app.route("/")
def index():
    return render_template("index.html", profiles=os.listdir(app.static_folder))
