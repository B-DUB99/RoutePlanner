# Python modules
import sqlite3


class data_retriever:
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.mag = 1
        self.offset = 0.00001

    # use to connect to the database and create a cursor object
    def connect(self):
        try:
            self.connection = sqlite3.connect('db/routeplanning.db')
            self.cursor = self.connection.cursor()
            print('Successful connection, cursor created\n')
        except Exception as e:
            print(f'Error: {e}')
            self.connection = sqlite3.connect('../db/routeplanning.db')
            self.cursor = self.connection.cursor()
    
    def close(self):
        try:
            self.connection.close()
        except:
            print("Close Failed")

    def get_amenities(self, amen_type):
        self.cursor.execute("SELECT * FROM amenities a1, amenity_types a2 WHERE"
                            + f" a1.type = a2.rowid AND a2.name = '{amen_type}'")
        
        amens = self.cursor.fetchall()
        amens_dict = []
        
        for a in amens:
            temp_dict = [{'name': a[1],
                          'desc': a[2],
                          'lat': a[4],
                          'lon': a[5],
                          'pic_loc': a[6]}]
            amens_dict.append(temp_dict)

        return amens_dict

    # gets the closest nodes to the users start node
    # it's up to pathfinder to determine if the node is a corrct start
    def get_closest_nodes(self, user_marker):
        
        while True:
            
            east_lon = user_marker[1] + (self.offset * self.mag)
            west_lon = user_marker[1] - (self.offset * self.mag)
            north_lat = user_marker[0] + (self.offset * self.mag)
            south_lat = user_marker[0] - (self.offset * self.mag)

            self.cursor.execute("SELECT node_id, lat, lon FROM nodes WHERE lon < "
                                + f"{east_lon} AND lon > {west_lon} AND lat < "
                                + f"{north_lat} AND lat > {south_lat}")
            nodes = self.cursor.fetchall()
            if len(nodes) != 0:
                return nodes
            else:
                self.mag += 1
                print(f"{self.mag}")


    def get_exit_nodes(self, way_id):
        return

    # Returns all nodes attached to provided way_id
    def get_nodes(self, way_id):
        self.cursor.execute("SELECT DISTINCT node_id FROM nodes n, (SELECT "
                            + "node_id_from, node_id_to FROM links l, ways w"
                            + f" WHERE w.way_id = l.way_id AND l.way_id = {way_id}"
                            + ") a WHERE n.node_id = a.node_id_from OR n.node_id "
                            + "= a.node_id_to")

        temp = self.cursor.fetchall()
        nodes = []
        for t in temp:
            nodes.append(t[0])

        return nodes

    # Returns all ways attached to provided node_id
    def get_way(self, node_id):
        self.cursor.execute("SELECT DISTINCT way_id FROM links WHERE "
                            + f"node_id_from = {node_id} OR node_id_to "
                            + f"= {node_id}")

        temp = self.cursor.fetchall()
        ways = []
        for t in temp:
            ways.append(t[0])

        return ways

    def get_way_info(self, way_id):

        return

    #returns the neighboring node ids of the provided id
    def get_node_neighbors(self, n_id):
        
        self.cursor.execute("SELECT node_id FROM nodes n, (SELECT node_id_from, "
                            + f"node_id_to FROM links WHERE node_id_from = {n_id} OR "
                            + f"node_id_to = {n_id}) a WHERE (n.node_id = "
                            + "a.node_id_from OR n.node_id = a.node_id_to) AND " 
                            + f"n.node_id != {n_id}")

        temp = self.cursor.fetchall()
        neighbors = []

        for t in temp:
            neighbors.append(t[0])
        
        return neighbors

    # TODO: implement
    # distance is already stored in the DB between connected nodes - Matt
    def get_distance(self, lat1, lon1, lat2, lon2):
        # returns the distance between two coordinates in meters
        # lat1, lon1, lat2, lon2 are floats
        # returns a float
        return

    def get_node_coords(self, n_id):

        self.cursor.execute("SELECT lat, lon FROM nodes WHERE node_id = {n_id}")

        return self.cursor.fetchone()
