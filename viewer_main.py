import os
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/<profile>")
def list_images(profile):
    if profile not in os.listdir(app.static_folder):
        return redirect("/", code=302)
    return render_template("gallery.html", profile=profile, images=os.listdir(app.static_folder + "/" + profile))


@app.route("/")
def index():
    return render_template("index.html", profiles=os.listdir(app.static_folder))