from flask import Blueprint, render_template, request, session, redirect, url_for
import json


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

@views.route('/<string:markerInfo>', methods=['POST'])
def getMarkers(markerInfo):
    info = json.loads(markerInfo)
    print(info)
    return info

@views.route("/calculate/<string:userinfo>", methods=["POST"])
def calculate(userinfo):
    data = json.loads(userinfo)
    print(data)
    return redirect(url_for("views.test"))

@views.route("/update/")
def update():
    print("update")
    # does not Work yet , may has to be manually only .. ~BDUB
    return redirect(url_for("views.test"))
