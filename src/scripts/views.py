from flask import Blueprint, render_template, request, send_file
import json
from io import BytesIO
import os
from datetime import datetime
import time

from .data_retriever import data_retriever
from .pathfinder import Pathfinder
from .gpx_export import GPX_export

views = Blueprint("views", __name__, "")
locs = []


@views.route("/", methods=["GET", "POST"])
def homepage():
    # will be post when you click on the map to put a marker
    if request.method == "POST":
        output = request.get_json()
        coords = json.loads(output)
        locs.append(coords)
        print(locs)
    return render_template("routeplanner.html")


@views.route('calculate_route/<string:markerInfo>', methods=['POST'])
def calculate_route(markerInfo):
    print(markerInfo)
    info = json.loads(markerInfo)
    # retrieve start and end nodes from info
    start = info[0]
    end = info[1]
    risk_tol = int(info[2])
    transport_type = info[3]
    error = -1
    start_time = time.time()
    print("Pathfinding has started:")
    
    # create a pathfinder object and pass in the start and end nodes
    while error == -1 and risk_tol < 5:
        pathfinder = Pathfinder(start, end, transport_type, risk_tol)
        error = pathfinder.astar()
        risk_tol += 1
        print(f"Risk tolerance updated to: {risk_tol}")
    end_time = time.time()
    delta = end_time - start_time
    if error == -1:
        print("error finding path")
        return [[],[]]
    else:
        data = []
        directions = pathfinder.return_directions()
        pathfinder.return_path()
        data.append(pathfinder.return_path())
        data.append(pathfinder.return_directions())
        print(f"{delta} Completion Time")
        return data


# make this interactive with the map instead of a button
@views.route("/get_amenities/<string:amen_type>", methods=["POST"])
def get_amenities(amen_type):
    data = json.loads(amen_type)
    d_ret = data_retriever()
    d_ret.connect()
    amens = []
    try:
        amens = d_ret.get_amenities(data)
    except:
        print("User selected nothing to find!")
    d_ret.close()
    print(f"{amens}")
    return amens


# get the gpx file from the route and return it
@views.route("/get_gpx/<string:path_list>", methods=["GET"])
def get_gpx(path_list):
    # generate gpx file

    # file = GPX_export(temp_points)
    file = GPX_export(path_list)
    file_name = file.export()

    # create binary stream in memory
    return_data = BytesIO()
    # write the file into memory
    with open(file_name, 'rb') as bin_file:
        return_data.write(bin_file.read())
    # return to beginning of file
    return_data.seek(0)
    # delete file
    os.remove(file_name)

    # add 6 hours on top of the current time to account for time zone difference
    time_stamp = datetime.fromtimestamp(time.mktime(time.localtime(time.time() - 21600))).strftime("%m-%d-%Y_%H-%M-%S")


    # send binary stream to the user
    return send_file(return_data, mimetype='application/gpx+xml', download_name=f'route_{time_stamp}.gpx')
