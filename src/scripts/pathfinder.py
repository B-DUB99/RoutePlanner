# import dataretriever
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

    def __init__(self, start, end, transportation_type):
        # conversion of dict to list
        self.user_start = [0, start['lat'], start['lng'], 0]
        self.user_end = [0, end['lat'], end['lng'], 0]

        # rest of variables
        self.start_node = []
        self.end_node = []
        self.current_node = []
        self.data_retriever = data_retriever()
        self.data_retriever.connect()
        self.transportation_type = transportation_type
        self.lat_lng = []
        self.path = []

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
        self.path.reverse()
        
    def astar(self):
        # find closest node to where user dropped pin
        self.start_node = self.find_next_best_user_node(self.user_start)
        self.end_node = self.find_next_best_user_node(self.user_end)
        # initialize open/closed lists
        open_list, closed_list = [], []
        open_list.append(Node(self.start_node))
        # the algorithm
        found = False
        last_node = None
        while len(open_list) != 0:
            # pop q from the open list
            q = self.get_q(open_list)
            # get q's neighbors
            neighbors = self.data_retriever.get_node_neighbors(q.data[0])
            neighbors = self.nodify(neighbors, q)
            # for each neighbor
            for neighbor in neighbors:
                # is this the target
                if neighbor.data == self.end_node:
                    found = True
                    last_node = neighbor
                    break
                # calculate g and h for neighbor
                neighbor.set_g(q.get_g() + self.calculate_distance_between_nodes(q.data, neighbor.data))
                # h is what will be updated once we figure out how to better tell which one is good
                # currently its just the distance from neighbor to end node
                neighbor.set_h(self.calculate_distance_between_nodes(neighbor.data, self.end_node))
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
        self.denodify(last_node)
        self.assemble_lat_lng()
            
            
            

    def swap(self, arr, i, j):
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp

    def sort_neighbors(self, neighbors):
        # no neighbors idk if I need this 
        if len(neighbors) == 0:
            return neighbors
        
        # get distances of nodes
        distances = []
        for neighbor in neighbors:
            distances.append(self.calculate_distance_between_nodes(neighbor, self.end_node))

        # sort (maybe change sorting algorithm)
        going = True
        while going:
            going = False
            for i in range(len(distances) - 1):
                # would add more checks to see which one is best here
                if distances[i] > distances[i + 1]:
                    going = True
                    self.swap(distances, i, i + 1)
                    self.swap(neighbors, i, i + 1)

    def recursive_path(self, curr):
        print(curr)
        # base case
        if curr == self.end_node:
            print("found")
            self.found = True
            self.path.append(curr)
            return 
        
        neighbors = self.data_retriever.get_node_neighbors(curr[0])
        self.sort_neighbors(neighbors)  # best -> worst

        # check all the neighbors
        for neighbor in neighbors:
            # if the neighbor is in the path already don't pick it
            if neighbor in self.path:
                continue
            # add check to make sure way is valid if not continue (idk how to do this yet)
            self.path.append(curr)
            self.recursive_path(neighbor)
            if self.found:
                return
            self.path.pop()

    def mike_path(self):
        print(f'Start:  {self.user_start}')
        print(f'End:    {self.user_end}')
        self.path.append(self.user_start)

        # set the start and end nodes to the closest nodes around our (user) start and end points
        self.start_node = self.find_next_best_user_node(self.user_start)
        self.current_node = self.start_node
        self.end_node = self.find_next_best_user_node(self.user_end)

        # append the start node to the path
        self.path.append(self.start_node)

        self.recursive_path(self.current_node)
        self.assemble_lat_lng()

    # function that loops, going through a graph made in a database, determining
    # the best path in the process. Algorithm does a depth first search looking
    # for the end node that is found around the user end node
    def find_path(self):
        
        print(f'Start:  {self.user_start}')
        print(f'End:    {self.user_end}')
        self.path.append(self.user_start)

        # set the start and end nodes to the closest nodes around our (user) start and end points
        self.start_node = self.find_next_best_user_node(self.user_start)
        self.current_node = self.start_node
        self.end_node = self.find_next_best_user_node(self.user_end)


        # append the start node to the path
        self.path.append(self.start_node)
        best_path = []
        dead_ends = []
        best_distance = 0
        # look for new nodes until we reach the end node
        while self.current_node[0] != self.end_node[0]:
            
            # way to see if way is correct for transport or not
            way = self.data_retriever.get_way(self.current_node[0])
            way_info = None
            if len(way) == 1:
                way_info = self.data_retriever.get_way_info(way[0])

            neighbors = self.data_retriever.get_node_neighbors(self.current_node[0])
            # size 1 represents dead end path
            if len(neighbors) == 1 and len(self.path) > 1:
                ind = self.find_last_connector()
                if ind != -1:
                    dead_end_node = self.rollback(ind)
                    dead_ends.append(dead_end_node)
                    self.current_node = self.path[ind]
                    neighbors = self.data_retriever.get_node_neighbors(self.current_node[0])

            best_node = None
            best_node_distance = None
            for n in neighbors:
                index = self.find_node_in_path(n[0])
                dead_end_node = self.find_node_in_dead_ends(n[0], dead_ends)
                if index == -1 and dead_end_node == -1:
                    if best_node is None:
                        best_node = n
                    best_node_distance = self.calculate_distance_between_nodes(best_node, self.end_node)
                    n_distance = self.calculate_distance_between_nodes(n, self.end_node)
                    if n_distance < best_node_distance:
                        best_node = n
                        best_node_distance = n_distance

            if best_node is None:
                ind = self.find_last_connector()
                dead_end_node = self.rollback(ind)
                dead_ends.append(dead_end_node)
                print(f"{ind} {len(self.path)} {self.path}")
                self.current_node = self.path[ind]
            else:
                self.current_node = best_node
                self.path.append(self.current_node)

        self.path.append(self.user_end)
        self.assemble_lat_lng()
        print(f'Path:   {self.lat_lng}')

        
    # assembles lats and longs to return to flask
    def assemble_lat_lng(self):
        for n in self.path:
            self.lat_lng.append([n[1], n[2]])
    
    # returns the best node around user nodes
    # this is defined as the closest node to start node and target node
    def find_next_best_user_node(self, user_node):
        list_of_nodes = self.data_retriever.get_closest_nodes(user_node)
        best_distance_node = list_of_nodes[0]
        # for each item check if it's the closest to start and end, and transportation type
        for node in list_of_nodes:
            #if node[0] == self.end_node[0]:
            #    return node
            if self.calculate_distance_between_nodes(user_node, node) < self.calculate_distance_between_nodes(best_distance_node, node):
                best_distance_node = node
        return self.data_retriever.get_node_info(best_distance_node[0])

    def calculate_distance_between_nodes(self, node1, node2):
        return distance.distance((node1[1], node1[2]), (node2[1], node2[2])).meters

    # starts at the end of the path and rolls backwards until it finds a
    # connector node. Then returns that index. Returns -1 if connector node not
    # found
    def find_last_connector(self):
        length = len(self.path)
        index = length - 1
        while index >= 0:
            if self.path[index][3] == 1 and index != length - 1:
                return index
            index -= 1
        return index

    # Finds a node in the path list
    def find_node_in_path(self, node_id):
        for n in self.path:
            print(f"{n} {node_id}")
            if n[0] == node_id:
                return 0
        return -1

    def find_node_in_dead_ends(self, node_id, dead_ends):
        for n in dead_ends:
            if n == node_id:
                return 0
        return -1

    # closes db connection and returns an list of latitudes and longitudes
    def return_path(self):
        self.data_retriever.close()
        return self.lat_lng

    def rollback(self, target):
        dead_end_node = None
        index = len(self.path) - 1
        while index > target:
            dead_end_node = self.path.pop(index)
            index -= 1
            print(f"{dead_end_node}")
        return dead_end_node[0]
