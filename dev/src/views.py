from flask import Blueprint, render_template, request, session, redirect, url_for
import json

from .data_retriever import data_retriever

views = Blueprint("views", __name__, "")
locs = []


@views.route("/", methods=["GET", "POST"])
def test():
    # will be post when you click on the map to put a marker
    if request.method == "POST":
        output = request.get_json()
        coords = json.loads(output)
        locs.append(coords)
        print(locs)
    temp_points = [
        [42.29127852746485, -85.5919075012207],
        [42.30918068099292, -85.6549072265625],
        [42.26790919743789, -85.65319061279297],
        [42.291532494305976, -85.58795928955078]
    ]
    return render_template("testingwithmenu.html", temp_points=temp_points, length=len(temp_points))

@views.route('/<string:markerInfo>', methods=['POST'])
def getMarkers(markerInfo):
    info = json.loads(markerInfo)
    print(info)
    return info

@views.route("/calculate/<string:userinfo>", methods=["POST"])
def calculate(userinfo):
    data = json.loads(userinfo)
    print(data)
    d_ret = data_retriever()
    d_ret.connect()
    amens = []
    try:
        amens = d_ret.get_amenities(data[2][0])
    except:
        print("User selected nothing to find!")
    d_ret.close()
    print(amens)
    return amens

@views.route("/update/")
def update():
    print("update")
    # does not Work yet , may has to be manually only .. ~BDUB
    return redirect(url_for("views.test"))
