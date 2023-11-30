#script to generate the Database to be used for CS senior design - Kzoo/Portage route planner
#WARNING!!!!!!! THIS SCRIPT WILL DELETE THE DB AND GENERATE A NEW ONE.
#don't run this script if thats not what you want


import itertools
import sqlite3
import csv
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
        cursor.execute("DROP TABLE ways")
        cursor.execute("DROP TABLE links")
        cursor.execute("DROP TABLE connector_links")
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
        cursor.execute("CREATE TABLE ways(" +
                       "way_id BIGINT UNSIGNED," +
                       "name VARCHAR(40)," +
                       "highway VARCHAR(20)," +
                       "risk TINYINT," +
                       "cycleway VARCHAR(20)," +
                       "oneway VARCHAR(20)," +
                       "PRIMARY KEY(way_id))")
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
        cursor.execute("CREATE TABLE connector_links(" +
                       "way_id BIGINT UNSIGNED," +
                       "node_id_from BIGINT UNSIGNED," +
                       "node_id_to BIGINT UNSIGNED," +
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

        types = ["Grocery",
                 "Books",
                 "Cafe",
                 "Drink",
                 "Food",
                 "Treats",
                 "Businesses",
                 "Community_Hubs",
                 "Pharmacy",
                 "Bike_Repair",
                 "Bike_Shops",
                 "Bathrooms,_Drinking_Fountains",
                 "Bike_Parking",
                 "Worlds_of_Wonder",
                 "Art",
                 "Sculptures"]

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
    query = overpassQueryBuilder(bbox=[42.157, -85.6995747, 42.369062, -85.531], elementType="node")
    kalamazoo = Overpass().query(query, timeout=600)
    nodes = kalamazoo.nodes()
    nodeCount = 0

    for node in nodes:
        cursor.execute("INSERT INTO nodes(node_id, lat, lon, connector)" +
                       " VALUES(" + str(node.id()) + ", " + str(node.lat()) + ", " + str(node.lon()) + ", FALSE)")
        nodeCount = nodeCount + 1
        print("total nodes inserted into DB =", nodeCount)

    # query and get ways coordinates are a box around kzoo
    query = overpassQueryBuilder(bbox=[42.157, -85.6995747, 42.369062, -85.531], elementType="way[highway]")
    kalamazoo = Overpass().query(query, timeout=600)
    ways = kalamazoo.ways()
    linkCount = 0

    # loop through the ways list and examine if it has a 'name' tag or not and change
    # query based on that
    for w in ways:
        mylist = w.tags()
        if 'name' in mylist:
            cursor.execute('INSERT INTO ways(way_id, name, highway, risk)' +
                           ' VALUES(' + str(w.id()) + ', "' + mylist['name'] +
                           '", "' + mylist['highway'] + '", 1)')
        else:
            cursor.execute('INSERT INTO ways(way_id, highway, risk)' +
                           ' VALUES(' + str(w.id()) + ', "' + mylist['highway'] + '", 1)')

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
                   " n.node_id) AND w.way_id = l.way_id AND (w.highway = " +
                   "'motorway' OR w.highway = 'motorway_link' OR w.highway " +
                   "= 'raceway' OR w.highway = 'rest_area' OR w.highway " +
                   "= 'proposed' OR w.highway = 'construction')")
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

    #remove nodes from nodes table that are not in 
    cursor.execute("DELETE FROM nodes WHERE node_id NOT IN " +
                   "(SELECT DISTINCT n.node_id from nodes n, links WHERE " +
                   "n.node_id = node_id_from OR n.node_id = node_id_to)");

    print(f"{cursor.rowcount} nodes not linked and deleted from DB")
    connection.commit()
    
    # not correct will try to fix later
    '''
    try:
        cursor.execute("UPDATE nodes " +
                       "SET connector = TRUE " +
                       "FROM (SELECT f.n_id AS id, (c1 + c2) AS c3 " +
                             "FROM (SELECT node_id_from as n_id, COUNT(way_id) as c1 " +
                                   "FROM links " +
                                   "GROUP BY node_id_from) AS f, " +
                                   "(SELECT node_id_to AS n_id, COUNT(way_id) AS c2 " +
                                   "FROM links " +
                                   "GROUP BY node_id_to) AS t " +
                             "WHERE t.n_id = f.n_id) AS a " +
                       "WHERE node_id = a.id AND a.c3 > 1")

        print(f"{cursor.rowcount} nodes set as intersections")
        connection.commit()
    except:
    '''
    cursor.execute("SELECT node_id " +
                    "FROM nodes")

    node_ids = cursor.fetchall()

    for n in node_ids:
        cursor.execute("SELECT COUNT(*) FROM (" +
                       "SELECT DISTINCT way_id " +
                       "FROM links " +
                       f"WHERE node_id_from = {n[0]} " +
                       f"OR node_id_to = {n[0]})")

        count = cursor.fetchone()

        if count[0] > 1:
            cursor.execute("UPDATE nodes " +
                           "SET connector = TRUE " +
                           f"WHERE node_id = {n[0]}")
        else:
            cursor.execute("UPDATE nodes " +
                           "SET connector = FALSE "
                           f"WHERE node_id = {n[0]}")

        print(f"{n} set as a connector node")

    connection.commit()

    cursor.execute("SELECT DISTINCT way_id FROM links")
    ways = cursor.fetchall()
    for way in ways:
        cursor.execute("SELECT node_id_from FROM nodes, links WHERE node_id = "
                       + f"node_id_from AND connector = 1 AND way_id = {way[0]}")
        from_nodes = cursor.fetchall()
        cursor.execute("SELECT node_id_to FROM nodes, links WHERE node_id = "
                       + f"node_id_to AND connector = 1 AND way_id = {way[0]}")
        to_nodes = cursor.fetchall()
        length = None
        if len(from_nodes) < len(to_nodes):
            length = len(from_nodes)
        else:
            length = len(to_nodes)

        for i in range(length):
            cursor.execute("INSERT INTO connector_links VALUES("
                           + f"{way[0]}, {from_nodes[i][0]}, {to_nodes[i][0]})")
            print(f"{from_nodes[i][0]}, {to_nodes[i][0]} connectors linked")

    # update risk levels for certain roads and ways
    portage_csv = 'Road_Risk_Levels_Portage.csv'
    kzoo_csv = 'Road_Risk_Levels_Kzoo.csv'

    with open(portage_csv, mode ='r') as p_file:
        portage = csv.reader(p_file)
        next(portage) #skip header
        for line in portage:
            cursor.execute("UPDATE ways " +
                           f"SET risk = {line[1]} " +
                           f"WHERE name = '{line[0]}'")
            print(f"{line[0]} updated risk level to {line[1]}")

    with open(kzoo_csv, mode = 'r') as k_file:
        kzoo = csv.reader(k_file)
        next(kzoo) #skip header
        for line in kzoo:
            if line[0] == "-1":
                cursor.execute("UPDATE ways " +
                               f"SET risk = {line[2]} " +
                               f"WHERE name = '{line[1]}'")
            else:
                cursor.execute("UPDATE ways " +
                               f"SET risk = {line[2]} " +
                               f"WHERE way_id = {line[0]}")
            print(f"{line[0]}, {line[1]} updated to risk level {line[2]}")
                    
    cursor.execute("CREATE INDEX ind_1 ON links(node_id_from)")
    cursor.execute("CREATE INDEX ind_2 ON links(node_id_to)")

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
                split_name = name.split("-")
                if len(split_name) == 2:
                    amen_type = split_name[0].strip()
                    name = split_name[1].strip()
                else:
                    amen_type = i.name.text
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
            
            if amen_type == "Worlds of Wonder":
                if j.styleUrl.text == "#icon-1509-9C27B0":
                    amen_type = "Art"
                elif j.styleUrl.text == "#icon-1509-9C27B0-nodesc":
                    amen_type = "Art"
                elif j.styleUrl.text == "#icon-1599-880E4F":
                    amen_type = "Sculptures"
                else:
                    amen_type = "Worlds_of_Wonder"
            if amen_type == "Bike Shops, Repair Stations":
                if j.styleUrl.text == "#icon-1590-9C27B0":
                    amen_type = "Bike_Repair"
                elif j.styleUrl.text == "#icon-1522-E65100":
                    amen_type = "Bike_Shops"

            if amen_type == "Bike Parking, Bathrooms, Drinking Fountains":
                amen_type = "Bathrooms,_Drinking_Fountains"
            if name == "Bike Parking":
                amen_type = "Bike Parking"
            amen_type = amen_type.replace(' ', '_')
            try:
                if (lat != 0):
                    cursor.execute('INSERT INTO amenities(name, description, lat, lon, pic_loc) VALUES("' + name + '", "' + desc + '", ' + str(lat) + 
                                   ', ' + str(long) + ', "' + pic + '")')
                    cursor.execute('SELECT rowid, * FROM amenity_types WHERE name = "' + amen_type + '"')
                    a_type = cursor.fetchone()
                    if a_type is None:
                        cursor.execute('UPDATE amenities ' +
                                       'SET type = 7 ' +
                                       'WHERE name = "' + name + '"')
                        print(f"{name} updated as a 7: Businesses")
                    else:
                        cursor.execute('Update amenities ' +
                                       f'SET type = {a_type[0]} ' +
                                       'WHERE name = "' + name + '"')
                        print(f"{name} updated as a {a_type[0]}: {amen_type}")
                    
            except Exception as err:
                print("Something went wrong: {}".format(err))


    # commit and close
    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()
