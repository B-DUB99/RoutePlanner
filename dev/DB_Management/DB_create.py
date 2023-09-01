#script to generate the Database to be used for CS senior design - Kzoo/Portage route planner
#WARNING!!!!!!! THIS SCRIPT WILL DELETE THE DB AND GENERATE A NEW ONE.
#don't run this script if thats not what you want


import itertools
import sqlite3
from collections import deque
from geopy import distance
from pykml import parser
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.overpass import overpassQueryBuilder

def main():
    # try to connect to the database file if it exists, otherwise create a new one
    try:
        connection = sqlite3.connect('../db/routeplanning.db')
        print("Opened database successfully")
    except:
        print("Error connecting to database")
        return

    # create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # drop the whole database and start over
    try:
        cursor.execute("DROP TABLE nodes")
        cursor.execute("DROP TABLE types")
        cursor.execute("DROP TABLE ways")
        cursor.execute("DROP TABLE links")
        cursor.execute("DROP TABLE amenity_types")
        cursor.execute("DROP TABLE amenities")
    except:
        print("Tables do not exist")

    # create tables for DB
    try:
        cursor.execute("CREATE TABLE nodes(" +
                       "node_id BIGINT UNSIGNED," +
                       "lat FLOAT," +
                       "lon FLOAT," +
                       "connector BOOLEAN," +
                       "PRIMARY KEY(node_id))")
        print(f"Table nodes created successfully")
    except:
        print(f"Table nodes already exists")

    try:
        cursor.execute("CREATE TABLE types(" +
                       "id INT," +
                       "type VARCHAR(25)," +
                       "ped_priority TINYINT," +
                       "bike_priority TINYINT," +
                       "vehicle_priority TINYINT," +
                       "comm_activity TINYINT," +
                       "max_speed_limit TINYINT," +
                       "PRIMARY KEY(id))")
        print(f"Table types created successfully")
        # road types from the map that the client gave us
        types = ["Event Festival",
                 "Urban Center",
                 "Enhanced Neighborhood",
                 "Commercial Business",
                 "Neighborhood Business",
                 "City Connector",
                 "Downtown Main",
                 "Neighborhood Network",
                 "Local Neighborhood"]

        # associated values for the road types
        ped_p = ['3', '3', '3', '3', '3', '3', '3', '3', '3']
        bike_p = ['1', '2', '3', '2', '2', '2', '2', '2', '3']
        vehicle_a = ['1', '1', '1', '2', '2', '2', '1', '2', '1']
        comm_a = ['3', '3', '1', '1', '2', '1', '3', '1', '1']
        speed_limit = ['25', '35', '25', '40', '40', '45', '25', '40', '25']

        # generate types table
        for i in range(9):
            cursor.execute(
                    f'INSERT INTO types(type, ped_priority, bike_priority, vehicle_priority, comm_activity, max_speed_limit)' +
                    ' VALUES( "{types[i]}",' + ped_p[i] + ', ' + bike_p[i] + ', ' + vehicle_a[i] + ', ' + comm_a[i] + ', ' +
                    speed_limit[i] + ')')
        print(f"Table types populated successfully")

        # commit changes to database
        connection.commit()

    except Exception as e:
        print(f"something went wrong with table types{e}")

    try:
        cursor.execute("CREATE TABLE ways(" +
                       "way_id BIGINT UNSIGNED," +
                       "name VARCHAR(40)," +
                       "highway VARCHAR(20)," +
                       "type TINYINT," +
                       "cycleway VARCHAR(20)," +
                       "oneway VARCHAR(20)," +
                       "PRIMARY KEY(way_id)," +
                       "FOREIGN KEY(type) REFERENCES types(id))")
    except Exception as e:
        print(f"something went wrong with table ways{e}")

    try:
        cursor.execute("CREATE TABLE links(" +
                       "way_id BIGINT UNSIGNED," +
                       "node_id_from BIGINT UNSIGNED," +
                       "node_id_to BIGINT UNSIGNED," +
                       "kilo_between FLOAT," +
                       "FOREIGN KEY(node_id_from) REFERENCES nodes(node_id)," +
                       "FOREIGN KEY(node_id_to) REFERENCES nodes(node_id)," +
                       "FOREIGN KEY(way_id) REFERENCES ways(way_id))")
    except Exception as e:
        print(f"something went wrong with table links{e}")

    try:
        cursor.execute("CREATE TABLE amenity_types(" +
                       "id INT," +
                       "name VARCHAR(100)," +
                       "PRIMARY KEY(id))")

        types = ["Grocery Stores",
                 "Businesses",
                 "Community Hubs",
                 "Health and Wellness",
                 "Bike Shops, Repair Stations",
                 "Bike Parking, Bathrooms, Drinking Fountains",
                 "Worlds of Wonder"]

        for i in types:
            cursor.execute('INSERT INTO amenity_types(name)' +
                           ' VALUES("' + i + '")')

    except Exception as e:
        print(f"something went wrong with table amenity_types{e}")

    try:
        cursor.execute("CREATE TABLE amenities(" +
                       "id INT," +
                       "name VARCHAR(100)," +
                       "description VARCHAR(750)," +
                       "type TINYINT," +
                       "lat FLOAT," +
                       "lon FLOAT," +
                       "pic_loc VARCHAR(1250)," +
                       "PRIMARY KEY(id)," +
                       "FOREIGN KEY(type) REFERENCES amenity_types(id))")

    except Exception as e:
        print(f"something went wrong with table amenities{e}")

    # query and get nodes then plug all those nodes into the DB
    query = overpassQueryBuilder(bbox=[42.157, -85.663, 42.333, -85.531], elementType="node")
    kalamazoo = Overpass().query(query, timeout=600)
    nodes = kalamazoo.nodes()
    nodeCount = 0

    for node in nodes:
        cursor.execute("INSERT INTO nodes(node_id, lat, lon, connector)" +
                       " VALUES(" + str(node.id()) + ", " + str(node.lat()) + ", " + str(node.lon()) + ", FALSE)")
        nodeCount = nodeCount + 1
        print("total nodes inserted into DB =", nodeCount)

    # query and get ways coordinates are a box around kzoo
    query = overpassQueryBuilder(bbox=[42.157, -85.663, 42.333, -85.531], elementType="way[highway]")
    kalamazoo = Overpass().query(query, timeout=600)
    ways = kalamazoo.ways()
    linkCount = 0

    # loop through the ways list and examine if it has a 'name' tag or not and change
    # query based on that
    for w in ways:
        mylist = w.tags()
        if 'name' in mylist:
            cursor.execute('INSERT INTO ways(way_id, name, highway, type)' +
                           ' VALUES(' + str(w.id()) + ', "' + mylist['name'] + '", "' + mylist['highway'] + '", 9)')
        else:
            cursor.execute('INSERT INTO ways(way_id, highway, type)' +
                           ' VALUES(' + str(w.id()) + ', "' + mylist['highway'] + '", 9)')

        if 'oneway' in mylist:
            cursor.execute('UPDATE ways' +
                           ' SET oneway = "' + mylist['oneway'] +
                           '" WHERE way_id = ' + str(w.id()))

        if 'cycleway' in mylist:
            cursor.execute('UPDATE ways' +
                           ' SET cycleway = "' + mylist['cycleway'] +
                           '" WHERE way_id = ' + str(w.id()))

        # get the nodes associated with the current way and loop
        firstNodes = deque(w.nodes())
        firstNodes.pop()
        lastNodes = deque(w.nodes())
        lastNodes.popleft()
        for node_one, node_two in zip(firstNodes, lastNodes):
            # check if node is in nodes table and if not add it
            cursor.execute("SELECT *" +
                           " FROM nodes" +
                           " WHERE node_id = " + str(node_one.id()))
            result_one = cursor.fetchone()
            if (result_one == None):
                cursor.execute("INSERT INTO nodes(node_id, lat, lon)" +
                               " VALUES(" + str(node_one.id()) + ", " +
                               str(node_one.lat()) + ", " + str(node_one.lon()) + ")")
                nodeCount = nodeCount + 1
                print("total nodes inserted into DB =", nodeCount)
                print(f"{node_one.id()}, {w.id()}")
                cursor.execute("SELECT *" +
                               " FROM nodes" +
                               " WHERE node_id = " + str(node_one.id()))
                result_one = cursor.fetchone()

            cursor.execute("SELECT *" +
                           " FROM nodes" +
                           f" WHERE node_id = {node_two.id()}")
            result_two = cursor.fetchone()
            if (result_two == None):
                cursor.execute("INSERT INTO nodes(node_id, lat, lon)" +
                               " VALUES(" + str(node_two.id()) + ", " +
                               str(node_two.lat()) + ", " + str(node_two.lon()) + ")")
                nodeCount = nodeCount + 1
                print("total nodes inserted into DB =", nodeCount)
                print(f"{node_two.id()}, {w.id()}")
                cursor.execute("SELECT *" +
                               " FROM nodes" +
                               f" WHERE node_id = {node_two.id()}")
                result_two = cursor.fetchone()

            kilos = distance.distance((result_one[1], result_one[2]),
                                      (result_two[1], result_two[2])).km
            # link current node with current way
            cursor.execute('INSERT INTO links(way_id, node_id_from, node_id_to,' +
                           ' kilo_between)' +
                           ' VALUES(' + str(w.id()) + ', ' + str(result_one[0]) +
                           ', ' + str(result_two[0]) + ', ' + str(kilos) + ')')
            linkCount = linkCount + 1
            print("links inserted =", linkCount)

    # remove ways that are a part of I 94  and US 131
    cursor.execute("SELECT w.way_id, n.node_id" +
                   " FROM nodes n, links l, ways w" +
                   " WHERE (n.node_id = l.node_id_from OR l.node_id_to = " +
                   " n.node_id) AND w.way_id = l.way_id AND w.highway = 'motorway'")
    motorInfo = cursor.fetchall()
    wayDel = 0

    for i in motorInfo:
        if (wayDel != i[0]):
            cursor.execute('DELETE FROM links' +
                           ' WHERE way_id = ' + str(i[0]))
            cursor.execute('DELETE FROM ways' +
                           ' WHERE way_id = ' + str(i[0]))
            wayDel = i[0]

    connection.commit()

    # remove any nodes that are not linked to any way
    nodes_removed = 0
    for n in nodes:
        # search for the current node in links table
        cursor.execute("SELECT node_id_from " +
                       " FROM links" +
                       " WHERE node_id_from = " + str(n.id()) + " OR node_id_to = " +
                       str(n.id()))
        results = cursor.fetchall()
        # if it's not there remove it from the nodes table
        if (len(results) == 0):
            cursor.execute("DELETE FROM nodes" +
                           " WHERE node_id = " + str(n.id()))
            nodes_removed = nodes_removed + 1
            print("nodes not linked and have been deleted =", nodes_removed)

#need to revamp this because nodes are represented differently
    cursor.execute("SELECT node_id_from FROM links GROUP BY node_id_from HAVING " +
                   "COUNT(node_id_from) > 2;")
    connectors = cursor.fetchall()
    updated = 0

    for i in connectors:
        cursor.execute("UPDATE nodes SET connector = TRUE WHERE node_id = " + str(i[0]))
        updated = updated + 1
        print("nodes updated as a connector =", updated)

    # parse and plug kml into the database
    kml_file = 'ModeShift Kalamazoo.kml'

    with open(kml_file) as f:
        doc = parser.parse(f).getroot().Document

    amen_type = ""
    name = ""
    long = 0.0
    lat = 0.0
    desc = ""
    pic = ""
    ind = 0

    for i in doc.Folder:
        amen_type = i.name.text
        for j in i.Placemark:
            try:
                name = j.name.text
            except:
                name = j.name.text

            try:
                coords = j.Point.coordinates.text.split(',')
                long = float(coords[0])
                lat = float(coords[1])

            except:
                long = 0.0
                lat = 0.0

            try:
                parse = j.description.text.split('>')
                parsed = parse[3].split('<')
                desc = parsed[0]
            except:
                desc = ""

            try:
                pic = j.ExtendedData.Data.value.text
            except:
                pic = ""

            try:
                if (lat != 0):
                    cursor.execute('INSERT INTO amenities(name, description, lat, lon, pic_loc) VALUES("' + name + '", "' + desc + '", ' + str(lat) + 
                                   ', ' + str(long) + ', "' + pic + '")')
                    cursor.execute('SELECT rowid, * FROM amenity_types WHERE name = "' + amen_type + '"')
                    a_type = cursor.fetchone()
                    if (a_type != None):
                        cursor.execute(
                                'UPDATE amenities SET type = ' + str(a_type[0]) + ' WHERE name = "' + amen_type + '"')
                        print(f"{name} added successfully to amenities as {amen_type}")
            except Exception as err:
                print("Something went wrong: {}".format(err))


    # commit and close
    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()
