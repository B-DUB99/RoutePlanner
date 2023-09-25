# import dataretriever
from .data_retriever import data_retriever



class Pathfinder:
    def __init__(self, start, end):
        self.start_node = start
        self.end_node = end
        self.current_node = start
        self.data_retriever = data_retriever()

        # list of lists of lat and lng
        self.lat_lng = [[]]

    def find_path(self):            # returns a list of coordinates in the order of the path
        # finds the path from start to end calls the other functions
        print(f'Start:  {self.start_node}')
        print(f'End:    {self.end_node}')
        # extract the lat and lng from the start and end dictionaries
        self.lat_lng[0] = [self.start_node['lat'], self.start_node['lng']]
        self.lat_lng.append([self.end_node['lat'], self.end_node['lng']])

        # while the current node is not close to the end node (within 100 m) keep finding the next node by calling get_node_neighbors
        while self.current_node != self.end_node:
            # get the neighbors of the current node
            neighbors = self.data_retriever.get_node_neighbors(self.current_node['node_id'])
            # find the closest neighbor to the end node
            closest_neighbor = self.find_closest_neighbor(neighbors)
            # add the closest neighbor to the path
            self.lat_lng.append([closest_neighbor['lat'], closest_neighbor['lng']])
            # set the current node to the closest neighbor
            self.current_node = closest_neighbor

        # Path is a list of lists of lat and lng coordinates saved in self.lat_lng
        print(f'Path:   {self.lat_lng}')

    def find_closest_neighbor(self, neighbors):    # returns the closest neighbor to the end node
        # finds the closest neighbor to the end node
        # neighbors is a list of dictionaries
        # end node is a dictionary
        # return the closest neighbor
        closest_neighbor = neighbors[0]
        closest_distance = self.data_retriever.get_distance(self.end_node['lat'], self.end_node['lng'], closest_neighbor['lat'], closest_neighbor['lng'])
        for neighbor in neighbors:
            distance = self.data_retriever.get_distance(self.end_node['lat'], self.end_node['lng'], neighbor['lat'], neighbor['lng'])
            if distance < closest_distance:
                closest_neighbor = neighbor
                closest_distance = distance
        return closest_neighbor

    def return_path(self):          # returns a list of coordinates in the order of the path
        # returns the path
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


