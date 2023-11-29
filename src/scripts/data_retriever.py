# Python modules
import sqlite3
import time

class data_retriever:
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._mag = 50 # magnitude
        self._offset = 0.0000001
        self._walking_routes = ['residential',
                                'service',
                                'path',
                                'track',
                                'footway',
                                'pedestrian',
                                'steps',
                                'corridor',
                                'living_street']
        self._biking_routes = ['residential',
                               'service',
                               'path',
                               'track',
                               'trunk_link',
                               'cycleway',
                               'tertiary',
                               'unclassified',
                               'secondary',
                               'primary',
                               'trunk',
                               'secondary_link',
                               'living_street']

    # use to connect to the database and create a cursor object
    def connect(self):
        try:
            self.connection = sqlite3.connect('db/routeplanning.db')
            self.cursor = self.connection.cursor()
            print('Successful connection, cursor created\n')
        except Exception as e:
            print(f'Error: {e}')
            # other path to try for connection
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
    def get_closest_nodes(self, user_marker, transport, risk):
        while True:
            east_lon = user_marker[2] + (self._offset * self._mag)
            west_lon = user_marker[2] - (self._offset * self._mag)
            north_lat = user_marker[1] + (self._offset * self._mag)
            south_lat = user_marker[1] - (self._offset * self._mag)

            self.cursor.execute("SELECT node_id, lat, lon FROM nodes WHERE lon < "
                                + f"{east_lon} AND lon > {west_lon} AND lat < "
                                + f"{north_lat} AND lat > {south_lat}")
            nodes = self.cursor.fetchall()
            num_of_nodes = len(nodes)
            for i in range(num_of_nodes):
                index = num_of_nodes - i - 1
                if transport == 'walk':
                    if not self._is_node_walkable(nodes[index][0]):
                        nodes.pop(index)
                elif transport == 'bike':
                    if not self._is_node_bikable(nodes[index][0], risk):
                        nodes.pop(index)
            if len(nodes) != 0:
                return nodes
            else:
                self._mag += 50

    def get_connector_nodes(self, way_id):
        nodes = self.get_nodes(way_id)
        connectors = []
        for n in nodes:
            temp_data = self.get_node_info(n[0])
            if temp_data[3] == 1:
                connectors.append(temp_data)
        return connectors

    # returns all info attached to node:
    # (node_id, lat, lon, connector)
    # lat and lon are latitude and longitude
    # connector signifies if the node is a part of 2 or more ways
    def get_node_info(self, node_id):
        self.cursor.execute("SELECT node_id, lat, lon, connector FROM nodes WHERE node_id "
                            + f"= {node_id}")
        return self.cursor.fetchone()

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
            nodes.append(self.get_node_info(t[0]))
        return nodes

    # Returns all ways attached to provided node_id
    def get_way(self, n_id: int):
        self.cursor.execute("SELECT DISTINCT way_id FROM links WHERE "
                            + f"node_id_from = {n_id} OR node_id_to "
                            + f"= {n_id}")
        temp = self.cursor.fetchall()
        ways = []
        for t in temp:
            ways.append(t[0])
        return ways

    # returns all data in the way data will look like this:
    # [name, highway, type, cycleway, oneway]
    # name - name of road
    # highway - way type ex. residential = residential road
    # risk - stress level
    # cycleway - type of bike lane is attached to way
    # oneway - is the road a oneway

    def get_way_info(self, way_id):
        self.cursor.execute("SELECT way_id, name, highway, risk, cycleway, oneway "
                            + f"FROM ways WHERE way_id = {way_id}")
        return self.cursor.fetchone()

    #returns the neighboring node ids of the provided id
    def get_node_neighbors(self, n_id):
        start = time.time()
        self.cursor.execute("SELECT node_id FROM nodes n, (SELECT node_id_from, "
                            + f"node_id_to FROM links WHERE node_id_from = {n_id} OR "
                            + f"node_id_to = {n_id}) a WHERE (n.node_id = "
                            + "a.node_id_from OR n.node_id = a.node_id_to) AND " 
                            + f"n.node_id != {n_id}")
        temp = self.cursor.fetchall()
        neighbors = []
        for t in temp:
            neighbors.append(self.get_node_info(t[0]))
        end = time.time()
        delta = end - start
        print(f"{delta}")
        return neighbors

    # returns the provided node_id's lat and lon
    def get_node_coords(self, n_id):
        self.cursor.execute("SELECT lat, lon FROM nodes WHERE node_id = {n_id}")
        return self.cursor.fetchone()

    def get_walking_neighbors(self, n_id):
        walking_neighbors = []
        neighbors = self.get_node_neighbors(n_id)
        start_ways = self.get_way(n_id)
        start_len = len(start_ways)
        for node in neighbors:
            end_ways = self.get_way(node[0])
            end_len = len(end_ways)
            way_id = None
            if start_len > 1 or end_len > 1:
                for start in start_ways:
                    for end in end_ways:
                        if start == end:
                            way_id = end
            else:
                way_id = end_ways[0]
            end_way_info = self.get_way_info(way_id)
            if end_way_info[2] in self._walking_routes:
                print(end_way_info[2])
                walking_neighbors.append(node)
        
        return walking_neighbors
    
    def get_biking_neighbors(self, n_id, risk):
        biking_neighbors = []
        neighbors = self.get_node_neighbors(n_id)
        start_ways = self.get_way(n_id)
        start_len = len(start_ways)
        for node in neighbors:
            end_ways = self.get_way(node[0])
            end_len = len(end_ways)
            way_id = None
            if start_len > 1 or end_len > 1:
                for start in start_ways:
                    for end in end_ways:
                        if start == end:
                            way_id = end
            else:
                way_id = end_ways[0]
            end_way_info = self.get_way_info(way_id)
            if end_way_info[2] in self._biking_routes and end_way_info[3] <= risk:
                biking_neighbors.append(node)

        return biking_neighbors

    def _is_node_walkable(self, n_id):
        
        ways = self.get_way(n_id)
        for way in ways:
            way_info = self.get_way_info(way)
            if way_info[2] in self._walking_routes:
                return True
        return False

    def _is_node_bikable(self, n_id, risk):
        
        ways = self.get_way(n_id)
        for way in ways:
            way_info = self.get_way_info(way)
            if way_info[2] in self._biking_routes and way_info[3] <= risk:
                return True
        return False

    def reset_mag(self):
        self.mag = 1

