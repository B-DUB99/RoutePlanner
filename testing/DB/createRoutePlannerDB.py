#This is a script that will create the routeplanning database 
#Right now it just generates the database as long as you have the admin user already in your MySQL.
#I Plan on having the user provide the login data so others can 
#play around with the data or we can switch over to an environment file

#The script first generates all the tables for the DB, then takes all the node
#data from overpass of a box around the kzoo area and plugs those nodes' ids
#, lats, and lons into nodes table. We do the same with ways but we then get
#which nodes are apart of each way and link them together. The final step
#is going through and deleting any node not a part of a way because the ways
#in this DB make up the roadways and footpaths.

#Plan on making this a seemless file that first checks for the DB, then checks
#for the tables, and then plugs in all the data or goes to a menu screen where
#nodes/ways can be searched or altered

#running this script will take 30-60 minutes because of the 2800 nodes it
#has to download because they weren't included in the original node query.
#side note: this is better than the projected 2+ days of the original script

#DO NOT RUN!!!(it should just throw an error) unless you have time to spare and 
#have added admin as a user, of course you could just change user and password 
#in connect down below to 'cs4430'.
# I plan on getting this script fully fleshed out by next Monday 3/5 (Spring Break BABY!),
# so you won't have to do this set up. Plan on cleaning up code as well, as I 
#learn more python, right now it kind of messy

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
	print("routeplanning DB already exists.")
finally:    
	mydb.database = "routeplanning"

#create tables for DB
try:
	cursor.execute("CREATE TABLE nodes(" + 
	       "id BIGINT UNSIGNED PRIMARY KEY," + 
	       "lat FLOAT," +
	       "lon FLOAT)")
except:
	print("nodes Table already exists")

try:	       
	cursor.execute("CREATE TABLE types(" + 
	       "id TINYINT AUTO_INCREMENT," +
	       "type CHAR(25)," +
	       "PRIMARY KEY(id))")
except:
	print("types table already exists")

try:
	cursor.execute("CREATE TABLE ways(" +
	       "id BIGINT UNSIGNED PRIMARY KEY," +
	       "name CHAR(40)," +
	       "highway CHAR(20)," +
	       "typology TINYINT," +
	       "FOREIGN KEY(typology) REFERENCES types(id))")
except:
	print("ways table already exists")

try:
	cursor.execute("CREATE TABLE links(" + 
	       "node_id BIGINT UNSIGNED," +
	       "way_id BIGINT UNSIGNED," +
	       "FOREIGN KEY(node_id) REFERENCES nodes(id)," +
	       "FOREIGN KEY(way_id) REFERENCES ways(id))")
except:
	print("links table already exists")

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

#generate types table
for i in types:
    cursor.execute('INSERT INTO types(type)' +  
    	           ' VALUES("' + i + '")')

#query and get nodes then plug all those nodes into the DB
query = overpassQueryBuilder(bbox=[42.216,-85.663,42.333,-85.531], elementType="node")
kalamazoo = Overpass().query(query, timeout=600)
nodes = kalamazoo.nodes()
nodeCount = 0
for n in nodes:
    cursor.execute("INSERT INTO nodes(id, lat, lon)" + 
    		   " VALUES(" + str(n.id()) + ", " + str(n.lat()) + ", " + str(n.lon()) + ")")
    nodeCount = nodeCount + 1
    print("total nodes inserted into DB =", nodeCount)

#query and get ways coordinates are a box around kzoo
query = overpassQueryBuilder(bbox=[42.216,-85.663,42.333,-85.531], elementType="way[highway]")
kalamazoo = Overpass().query(query, timeout=600)
ways = kalamazoo.ways()
linkCount = 0

#loop through the ways list and examine if it has a 'name' tag or not and change
#query based on that
for w in ways:
    mylist = w.tags()
    if 'name' in mylist:
        cursor.execute('INSERT INTO ways(id, name, highway, typology)' + 
        	       ' VALUES(' + str(w.id()) + ', "' + mylist['name'] + '", "' + mylist['highway'] + '", 9)')
    else:
        cursor.execute('INSERT INTO ways(id, highway, typology)' +
        	       ' VALUES(' + str(w.id()) + ', "' + mylist['highway'] + '", 9)')
    
    #get the nodes associated with the current way and loop
    wayNodes = w.nodes()
    for n in wayNodes:
        #check if node is in nodes table and if not add it
        cursor.execute("SELECT id" +
        	       " FROM nodes" + 
        	       " WHERE id = " + str(n.id()))
        result = cursor.fetchone()
        if(result == None):
            cursor.execute("INSERT INTO nodes(id, lat, lon)" +
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
        	       " WHERE id = " + str(n.id()))
        nodesRemoved = nodesRemoved + 1
        print("nodes not linked and have been deleted =", nodesRemoved)

#commit and close
mydb.commit()
cursor.close()

