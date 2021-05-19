import base64
import os
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/<profile>")
def list_images(profile):
    if profile not in os.listdir(app.static_folder):
        return redirect("/", code=302)
    files = os.listdir(app.static_folder + "/" + profile)
    ii = [f for f in files if f.lower().endswith(".jpg") or f.lower().endswith(".png") or f.lower().endswith("jpeg")]
    videos = [f for f in files if f.lower().endswith(".mp4")]

    images = []
    for i in ii:
        with open(app.static_folder + "/" + profile + "/" + i, "rb") as f:
            images.append({"name": i, "data": base64.b64encode(f.read()).decode("ascii")})

    return render_template("gallery.html", root="static", profile=profile, images=images, videos=videos)


@app.route("/")
def index():
    return render_template("index.html", profiles=os.listdir(app.static_folder))

if __name__ == "__main__":
    app.run()