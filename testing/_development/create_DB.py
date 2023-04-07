#Script to generate the Database to be used for CS senior design - Kzoo/Portage route planner
#WARNING!!!!!!! THIS SCRIPT WILL DELETE THE DB AND GENERATE A NEW ONE.
#don't run this script if thats not what you want

from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.api import Api
import mysql.connector

#basic for now want to change to custom login or .env and checking if DB exists later
try:
	mydb = mysql.connector.connect(
        	host="localhost",
        	user="admin",
        	password="admin",
	)
except:
	print("change login info in script or add 'admin' as a user")
	exit()

#cursor to send mysql queries
cursor = mydb.cursor()

try:
	cursor.execute("CREATE DATABASE routeplanning")
	print("routeplanning DB created")
except:
    cursor.execute("DROP DATABASE routeplanning")
    cursor.execute("CREATE DATABASE routeplanning")
    print("routeplanning has been recreated")
finally:    
	mydb.database = "routeplanning"

#create tables for DB
try:
	cursor.execute("CREATE TABLE nodes(" + 
	       "node_id BIGINT UNSIGNED," + 
	       "lat FLOAT," +
	       "lon FLOAT," + 
           "connector BOOLEAN," +
           "PRIMARY KEY(node_id))")
except:
	print("nodes Table already exists")

try:	       
    cursor.execute("CREATE TABLE types(" + 
	       "id TINYINT AUTO_INCREMENT," +
	       "type VARCHAR(25)," +
           "ped_priority TINYINT," +
           "bike_priority TINYINT," +
           "vehicle_priority TINYINT," +
           "comm_activity TINYINT," +
           "max_speed_limit TINYINT," +
	       "PRIMARY KEY(id))")
	#road types from the map that the client gave us
    types = ["Event Festival", 
	 "Urban Center",
	 "Enhanced Neighborhood",
	 "Commercial Business",
	 "Neighborhood Business",
	 "City Connector",
	 "Downtown Main",
	 "Neighborhood Network",
	 "Local Neighborhood"]

    #associated values for the road types
    pedP = [3, 3, 3, 3, 3, 3, 3, 3, 3]
    bikeP = [1, 2, 3, 2, 2, 2, 2, 2, 3]
    vehicleP = [1, 1, 1, 2, 2, 2, 1, 2, 1]
    commA = [3, 3, 1, 1, 2, 1, 3, 1, 1]
    speedLimit = [25, 35, 25, 40, 40, 45, 25, 40, 25]

	#generate types table
    for i in range(9):
        cursor.execute('INSERT INTO types(type, ped_priority, bike_priority, vehicle_priority, comm_activity, max_speed_limit)' +  
    	           ' VALUES("' + types[i] + '", ' + str(pedP[i]) + ', ' + str(bikeP[i]) + ', ' + str(vehicleP[i]) + ', ' + str(commA[i]) + ', ' + str(speedLimit[i]) + ')')
    mydb.commit()
except:
	print("types table already exists")

try:
	cursor.execute("CREATE TABLE ways(" +
           "way_id BIGINT UNSIGNED," +
	       "name VARCHAR(40)," +
	       "highway VARCHAR(20)," +
	       "type TINYINT," +
           "PRIMARY KEY(way_id)," + 
	       "FOREIGN KEY(type) REFERENCES types(id))")
except:
	print("ways table already exists")

try:
	cursor.execute("CREATE TABLE links(" + 
	       "node_id BIGINT UNSIGNED," +
	       "way_id BIGINT UNSIGNED," +
	       "FOREIGN KEY(node_id) REFERENCES nodes(node_id)," +
	       "FOREIGN KEY(way_id) REFERENCES ways(way_id))")
except:
	print("links table already exists")

try:
    cursor.execute("CREATE TABLE amenity_types(" + 
            "id TINYINT AUTO_INCREMENT," +
            "name VARCHAR(100)," +
            "PRIMARY KEY(id))")

    types = ["Grocery Store",
            "Restrooms",
            "Bike Racks",
            "Drinking Fountains",
            "Repair Stations",
            "Bike Shops",
            "Pharmacies",
            "Cafe",
            "Restaurants/Bars",
            "Treat/Ice Cream Shops",
            "Libraries/Book Stores"]
    
    for i in types:
        cursor.execute('INSERT INTO amenity_types(name)' +
                ' VALUES("' + i + '")')
except:
    print("amenity_types table already created")

try:
    cursor.execute("CREATE TABLE amenities(" +
            "id INT AUTO_INCREMENT," +
            "name VARCHAR(100)," +
            "description VARCHAR(200)," +
            "type TINYINT," +
            "lat FLOAT," +
            "lon FLOAT," +
            "pic VARCHAR(200)," +
            "PRIMARY KEY(id)," +
            "FOREIGN KEY(type) REFERENCES amenity_types(id))")
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

#query and get nodes then plug all those nodes into the DB
query = overpassQueryBuilder(bbox=[42.157,-85.663,42.333,-85.531], elementType="node")
kalamazoo = Overpass().query(query, timeout=600)
nodes = kalamazoo.nodes()
nodeCount = 0
for n in nodes:
    cursor.execute("INSERT INTO nodes(node_id, lat, lon, connector)" + 
    		   " VALUES(" + str(n.id()) + ", " + str(n.lat()) + ", " + str(n.lon()) + ", FALSE)")
    nodeCount = nodeCount + 1
    print("total nodes inserted into DB =", nodeCount)

#query and get ways coordinates are a box around kzoo
query = overpassQueryBuilder(bbox=[42.157,-85.663,42.333,-85.531], elementType="way[highway]")
kalamazoo = Overpass().query(query, timeout=600)
ways = kalamazoo.ways()
linkCount = 0

#loop through the ways list and examine if it has a 'name' tag or not and change
#query based on that
for w in ways:
    mylist = w.tags()
    if 'name' in mylist:
        cursor.execute('INSERT INTO ways(way_id, name, highway, type)' + 
        	       ' VALUES(' + str(w.id()) + ', "' + mylist['name'] + '", "' + mylist['highway'] + '", 9)')
    else:
        cursor.execute('INSERT INTO ways(way_id, highway, type)' +
        	       ' VALUES(' + str(w.id()) + ', "' + mylist['highway'] + '", 9)')
    
    #get the nodes associated with the current way and loop
    wayNodes = w.nodes()
    for n in wayNodes:
        #check if node is in nodes table and if not add it
        cursor.execute("SELECT node_id" +
        	       " FROM nodes" + 
        	       " WHERE node_id = " + str(n.id()))
        result = cursor.fetchone()
        if(result == None):
            cursor.execute("INSERT INTO nodes(node_id, lat, lon)" +
            		   " VALUES(" + str(n.id()) + ", " + str(n.lat()) + ", " + str(n.lon()) + ")")
            nodeCount = nodeCount + 1
            print("total nodes inserted into DB =", nodeCount)

        #link current node with current way
        cursor.execute('INSERT INTO links(node_id, way_id)' + 
                ' VALUES(' + str(n.id()) + ', ' + str(w.id())+ ')')
        linkCount = linkCount + 1
        print("links inserted =", linkCount)

#remove any nodes that are not linked to any way
nodesRemoved = 0
for n in nodes:
    #search for the current node in links table
    cursor.execute("SELECT node_id" + 
               " FROM links" +
    		   " WHERE node_id = " + str(n.id()))
    results = cursor.fetchall()
    #if it's not there remove it from the nodes table
    if (len(results) == 0):
        cursor.execute("DELETE FROM nodes" +
        	       " WHERE node_id = " + str(n.id()))
        nodesRemoved = nodesRemoved + 1
        print("nodes not linked and have been deleted =", nodesRemoved)

cursor.execute("SELECT node_id FROM links GROUP BY node_id HAVING COUNT(node_id) > 1;")
connectors = cursor.fetchall()
updated = 0

for i in connectors:
    cursor.execute("UPDATE nodes SET connector = TRUE WHERE node_id = " + str(i[0]))
    updated = updated + 1
    print("nodes updated as a connector =", updated)

#commit and close
mydb.commit()
cursor.close()
