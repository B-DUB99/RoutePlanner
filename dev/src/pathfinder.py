# import dataretriever
from .data_retriever import data_retriever
from geopy import distance

class Pathfinder:
    def __init__(self, start, end, transportation_type):
        self.user_start = start
        self.user_end = end
        self.start_node = None
        self.end_node = None
        self.current_node = None
        self.data_retriever = data_retriever()
        self.data_retriever.connect()
        self.transportation_type = transportation_type

        # list of lists of lat and lng
        self.lat_lng = [[]]

    def find_path(self):            # returns a list of coordinates in the order of the path
        # finds the path from start to end calls the other functions
        print(f'Start:  {self.user_start}')
        print(f'End:    {self.user_end}')
        # extract the lat and lng from the start and end dictionaries
        self.lat_lng[0] = [self.user_start['lat'], self.user_start['lng']]

        # set the start and end nodes to the closest nodes around our (user) start and end points
        self.start_node = self.find_next_best_user_node(self.user_start)
        self.current_node = self.start_node
        self.end_node = self.find_next_best_user_node(self.user_end)


        # append the start node to the path
        self.lat_lng.append([self.start_node['lat'], self.start_node['lng']])
        best_path = [[]]
        best_distance = 0
        # look for new nodes until we reach the end node
        while self.current_node != self.end_node:
            break
            # base case distance between next node and end node


        # append the end node to the path
        self.lat_lng.append([self.user_end['lat'], self.user_end['lng']])
        # Path is a list of lists of lat and lng coordinates saved in self.lat_lng
        print(f'Path:   {self.lat_lng}')



    # function already exists in the data_retriever
    def find_next_best_user_node(self, user_node):    # returns the closest neighbor to the end node
        list_of_nodes = self.data_retriever.get_closest_nodes(user_node)
        best_distance_node = list_of_nodes[0]
        # for each item check if it's the closest to start and end, and transportation type
        for node in list_of_nodes:
            if node['node_id'] == self.end_node['node_id']:
                return node
            if self.calculate_distance_between_nodes(user_node, node) < self.calculate_distance_between_nodes(best_distance_node, node):
                best_distance_node = node
        return best_distance_node


    def calculate_distance_between_nodes(self, node1, node2):
        # calculate the distance between two nodes
        return distance.distance((node1['lat'], node1['lng']), (node2['lat'], node2['lng'])).kilometers


    def return_path(self):          # returns a list of coordinates in the order of the path
        # returns the path
        self.data_retriever.close()
        return self.lat_lng


    # retrieve the lat and lng from website ( user ) ( start and end )
    # start node lat lng goes to dataretriever, get_closest_node
    # retrieve is a list of nodes ( node_id, lat, lng )
    # decide what node to go to next (closest node to end node)
        # send new node to the dataretriever, get_node_neighbors to get the next node (node_id)
        # retrieve the neighbors of the node ( node_id, lat, lng )
        # compare the neighbors to the end node (lat, lng)
        # if the neighbor is the end node or within 100 m, then we are done
        # if the neighbor is not the end node, then we need to find the next node to go to


