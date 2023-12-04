from .data_retriever import data_retriever
from geopy import distance

class Node:
    # g: movement cost from starting point to this node following current path
    # h: estimated cost to get from this node to target node 
    # data: node from the database class 
    def __init__(self, data):
        self.parent = None
        self.data = data
        self.g = 0
        self.h = 0
    
    def set_g(self, g):
        self.g = g
        
    def set_h(self, h):
        self.h = h
        
    def set_parent(self, parent):
        self.parent = parent
    
    def get_f(self):
        return self.g + self.h

    def get_g(self):
        return self.g
    
class Pathfinder:
    # indeces are in this order [0: id, 1: lat, 2: lon, 3: connector]
    # id - id of the node
    # lat - latitude of the node
    # lon - longitude of the node
    # connector - connector status 1 = connector or another 'way' to go 
    #                              0 = only on set path or 'way'
    def __init__(self, start, end, transportation_type, risk):
        # conversion of dict to list
        self.user_start = [0, start['lat'], start['lng'], 0]
        self.user_end = [0, end['lat'], end['lng'], 0]

        # rest of variables
        self.start_node = []
        self.end_node = []
        self.end_connector_node = []
        self.start_connector_node = []
        self.data = []
        self.data_retriever = data_retriever()
        self.data_retriever.connect()
        self.directions = []
        self.transportation_type = transportation_type
        self.lat_lng = []
        self.path = []
        self.risk_tol = risk
        self.found = False
    
    # returns the node with the smallest f
    def get_q(self, node_list):
        small_ind = 0
        small_val = 999999999
        for i, node in enumerate(node_list):
            if node.get_f() < small_val:
                small_val = node.get_f()
                small_ind = i
        return node_list.pop(small_ind)
    
    # turns list of database nodes into nodes for astar
    def nodify(self, node_list, parent):
        ret = []
        for node in node_list:
            temp = Node(node)
            temp.set_parent(parent)
            ret.append(temp)
        return ret
    
    # if node is in node_list with bigger f value
    def is_in(self, node, node_list):
        for n in node_list:
            if node.data == n.data and node.get_f() > n.get_f():
                return True
        return False
    
    # takes the last node gets path from its parent and adds the data to self.path
    def denodify(self, node):
        while True:
            self.path.append(node.data)
            node = node.parent
            if node == None:
                break
        if self.start_connector_node[0] != self.start_node[0]:
            self.path.append(self.start_node)
        self.path.append(self.user_start)
        self.path.reverse()
        
    def astar(self):
        # find closest node to where user dropped pin
        self.start_node = self._find_next_best_user_node(self.user_start)
        self.end_node = self._find_next_best_user_node(self.user_end)

        # find the closest connector to streamline pathfinding
        self.start_connector_node = self._find_closest_connector(self.start_node)
        self.end_connector_node = self._find_closest_connector(self.end_node)
        
        # append end nodes to path
        self.path.append(self.user_end)
        if self.end_node[0] != self.end_connector_node[0]:
            self.path.append(self.end_node)
        
        # initialize open/closed lists
        open_list, closed_list = [], []
        open_list.append(Node(self.start_connector_node))
        
        # the algorithm
        found = False
        last_node = None
        while len(open_list) != 0:
            # pop q from the open list
            q = self.get_q(open_list)
            neighbors = []
            # get q's neighbors based on selected user transport type
            if self.transportation_type == 'walk':
                neighbors = self.data_retriever.get_walking_neighbors(q.data[0],
                                                                      self.risk_tol)
            elif self.transportation_type == 'bike':
                neighbors = self.data_retriever.get_biking_neighbors(q.data[0],
                                                                     self.risk_tol)
            else:
                neighbors = self.data_retriever.get_node_neighbors(q.data[0])
            neighbors = self.nodify(neighbors, q)
            # for each neighbor
            for neighbor in neighbors:
                # is this the target
                if neighbor.data == self.end_connector_node:
                    found = True
                    last_node = neighbor
                    break
                # calculate g and h for neighbor
                neighbor.set_g(q.get_g() + self._calculate_distance_between_nodes(q.data, neighbor.data))
                # h is what will be updated once we figure out how to better tell which one is good
                # currently its just the distance from neighbor to end node
                neighbor.set_h(self._calculate_distance_between_nodes(neighbor.data,
                                                                     self.end_connector_node))
                # if node with same pos is in open list and has lower f skip
                if self.is_in(neighbor, open_list):
                    continue
                # f node with same pos is in closed list and has lower f skip
                if self.is_in(neighbor, closed_list):
                    continue
                open_list.append(neighbor)
            closed_list.append(q)
            if found:
                break
        # no path found -1 displays error message on host
        if last_node == None:
            return -1
        self.denodify(last_node)
        self._assemble_lat_lng()
        self._assemble_directions()
        return 1

    def _assemble_directions(self):
        path_len = len(self.path)
        previous_dir = ""
        previous_path_name = ""
        distance = 0
        for i in range(path_len - 2):
            lat_diff = abs(self.path[i][1] - self.path[i+1][1])
            lng_diff = abs(self.path[i][2] - self.path[i+1][2])
            distance += self._calculate_distance_between_nodes(self.path[i], self.path[i+1])
            card_dir = self._get_cardinal_direction(lat_diff, lng_diff, i)
            if i == 1 or i == (path_len - 3):
                if i == 1 and (self.start_connector_node[0] != self.start_node[0]):
                    path_name_risk = self.data_retriever.get_path_name_risk(self.path[i][0],
                                                                            self.path[i+1][0],
                                                                            0)
                elif i == (path_len - 3) and (self.end_connector_node[0] != self.end_node[0]):
                    path_name_risk = self.data_retriever.get_path_name_risk(self.path[i][0],
                                                                            self.path[i+1][0],
                                                                            0)
                else:
                    path_name_risk = self.data_retriever.get_path_name_risk(self.path[i][0],
                                                                            self.path[i+1][0],
                                                                            1)
                if (self.path[i][0] == self.start_node[0]) or (self.path[i+1][0] == self.end_node[0]):
                    if i == 1:
                        self.directions.append(["Proceed " + card_dir + " on " + path_name_risk[0], path_name_risk[1], 0])
                    elif i == (path_len - 3):
                        self.directions[len(self.directions)-1][2] = round(distance)
                    previous_dir = card_dir
                    previous_path_name = path_name_risk[0]
                    distance = 0
            elif i > 1:
                path_name_risk = self.data_retriever.get_path_name_risk(self.path[i][0],
                                                                        self.path[i+1][0],
                                                                        1)
                if previous_dir != card_dir or path_name_risk[0] != previous_path_name:
                    self.directions[len(self.directions)-1][2] = round(distance)
                    self.directions.append(["Proceed " + card_dir + " on " + path_name_risk[0], path_name_risk[1], 0])
                    previous_dir = card_dir
                    previous_path_name = path_name_risk[0]
                    distance = 0


    # assembles lats and longs to return to flask
    def _assemble_lat_lng(self):
        for n in self.path:
            self.lat_lng.append([n[1], n[2]])
    
    def _calculate_distance_between_nodes(self, node1, node2):
        return distance.distance((node1[1], node1[2]), (node2[1], node2[2])).meters

    def _find_closest_connector(self, node):
        # node is already a connector
        if self.data_retriever.get_node_info(node[0])[3] == 1:
            return node
        
        ways = self.data_retriever.get_way(node[0])
        connector_nodes = self.data_retriever.get_connector_nodes(ways[0])
        if len(connector_nodes) == 1:
            return connector_nodes[0]

        closest_ind = 0
        shortest_dist = None
        for i in range(len(connector_nodes)):
            curr_dist = self._calculate_distance_between_nodes(node,
                                                              connector_nodes[i])
            if shortest_dist == None:
                shortest_dist = self._calculate_distance_between_nodes(node,
                                                                      connector_nodes[i])
                closest_ind = i
            elif shortest_dist > curr_dist:
                shortest_dist = self._calculate_distance_between_nodes(node,
                                                                      connector_nodes[i])
                closest_ind = i

        return connector_nodes[closest_ind]
    # returns the best node around user nodes
    # this is defined as the closest node to start node and target node
    def _find_next_best_user_node(self, user_node):
        list_of_nodes = self.data_retriever.get_closest_nodes(user_node,
                                                              self.transportation_type,
                                                              self.risk_tol)
        best_distance_node = list_of_nodes[0]
        # for each item check if it's the closest to start and end, and transportation type
        for node in list_of_nodes:
            #if node[0] == self.end_node[0]:
            #    return node
            if self._calculate_distance_between_nodes(user_node, node) < self._calculate_distance_between_nodes(best_distance_node, node):
                best_distance_node = node
        return self.data_retriever.get_node_info(best_distance_node[0])

    def _get_cardinal_direction(self, lat_diff, lng_diff, ind):
        if lat_diff > lng_diff:
            if self.path[ind][1] < self.path[ind+1][1]:
                return "North"
            else:
                return "South"
        else: 
            if self.path[ind][2] < self.path[ind+1][2]:
                return "East"
            else:
                return "West"

    def return_directions(self):
        return self.directions

    # closes db connection and returns an list of latitudes and longitudes
    def return_path(self):
        self.data_retriever.close()
        return self.lat_lng

