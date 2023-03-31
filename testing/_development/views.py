import os

from flask import Blueprint, render_template, request, session, redirect, url_for
import json
import subprocess
import threading

def get_env():
    # get the update.sh script path
    update_script = os.getenv("UPDATE_SCRIPT")
    return update_script

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
    update_script = get_env()
    print({"update_script": update_script}, "update_script from views.py")
    # run bash script to pull the latest changes from the repo and restart the server (will be done automatically)
    def run_cmd():
        subprocess.call(["screen", "-dmS", "bash", "-c", update_script])

    thread = threading.Thread(target=run_cmd)
    thread.start()

    return redirect(url_for("views.test"))
