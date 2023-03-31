from flask import Blueprint, render_template, request, session, redirect, url_for
import json
import subprocess
import threading


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

<<<<<<< HEAD
    def run_bash():
        subprocess.call(['bash', './update_start.sh'])

        thread = threading.Thread(target=run_bash)
        thread.start()
=======
    # def run_bash():
    #     subprocess.call(['bash', './update_start.sh'])
    #
    #     thread = threading.Thread(target=run_bash)
    #     thread.start()
>>>>>>> 2a848810e0ae3e920b59c192035e4b86ac5488da



    #print("updating...")
    # run bash script to pull the latest changes from the repo and restart the server (will be done automatically)
    #subprocess.run(["./update_start.sh"])


    #return redirect(url_for("views.test"))
