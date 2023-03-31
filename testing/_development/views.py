from flask import Blueprint, render_template, request, session, redirect, url_for
import json
import subprocess


views = Blueprint(__name__, "")
locs = []


@views.route("/", methods=["GET", "POST"])
def test():
    # will be post when you click on the map to put a marker
    if request.method == "POST":
        output = request.get_json()
        coords = json.loads(output)
        locs.append(coords)
        print(locs)
    return render_template("testingwithmenu.html")

@views.route("/update/")
def update():
    print("updating...")
    # run bash script to pull the latest changes from the repo and restart the server (will be done automatically)
    subprocess.run(["./update.sh"])


    return redirect(url_for("views.test"))
